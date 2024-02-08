from dotenv import load_dotenv
import os
import tempfile
import time
import base64
import requests,uuid,json

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import azure.cognitiveservices.speech as speechsdk


@api_view(['GET'])
def hello(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Hello!"})

@api_view(['POST'])
def my_view(request):
    response = {
        'success' : False,
        'mesage' : 'something went wrong'
    }
    if request.method == 'POST':
        global cv_client
         
        try:
            # Get Configuration Settings
            load_dotenv()
            cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
            cog_key = os.getenv('COG_SERVICE_KEY')

            # Authenticate Computer Vision client
            credential = CognitiveServicesCredentials(cog_key) 
            cv_client = ComputerVisionClient(cog_endpoint, credential)

            image_file = request.FILES.get('image')
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in image_file.chunks():
                    temp_file.write(chunk)
            text = GetTextRead(temp_file.name)
            # text = ["revanth","hello"]
            #text = ''
            response = {
                'success' : True,
                'message' : text,
            }

        except Exception as ex:
            response = {
                'success' : False,
                'mesage' : str(ex)
            }
            

def GetTextRead(image_file):
    print('Reading text in {}\n'.format(image_file))
    # Use Read API to read text in image
    with open(image_file, mode="rb") as image_data:
        read_op = cv_client.read_in_stream(image_data, raw=True)
        
        # Get the async operation ID so we can check for the results
        operation_location = read_op.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]
    
        # Wait for the asynchronous operation to complete
        while True:
            read_results = cv_client.get_read_result(operation_id)
            if read_results.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                break
            time.sleep(1)
    
        # If the operation was successfully, process the text line by line
        response_txt = []
        if read_results.status == OperationStatusCodes.succeeded:
            for page in read_results.analyze_result.read_results:
                for line in page.lines:
                    response_txt.append(line.text)
                    # print(line.text)
                    # Uncomment the following line if you'd like to see the bounding box 
                    #print(line.bounding_box)
        else:
            response_txt.append("Text fetching failed")
    os.unlink(image_file)
    return response_txt

@api_view(['POST'])
def audio(request):
    if request.method == "POST":
        response_data = {}
        load_dotenv()
        speech_config = speechsdk.SpeechConfig(os.getenv('COG_SERVICE_KEY'),os.getenv('COG_SERVICE_REG'))
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        # The language of the voice that speaks.
        speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Get text from the console and synthesize to the default speaker.
        text = request.POST.get('text')

        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
                temp_audio_file.write(speech_synthesis_result.audio_data)
                temp_audio_file.seek(0)
                temp_audio_filepath = temp_audio_file.name
            with open(temp_audio_filepath, 'rb') as audio_file:
                audio_data = audio_file.read()

            # Encode the audio data as base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            # Clean up the temporary file (optional)
            os.remove(temp_audio_filepath)

            # Create the JSON response with the base64-encoded audio data
            response_data = {
                'success': True,
                'audio_base64': audio_base64
            }

        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
            response_data = {
                'success': True,
                'message': "conversion cancelled"
            }
        return JsonResponse(response_data)

@api_view(['POST'])
def translate(request):
    if request.method == 'POST':
        load_dotenv()
        cog_end = os.getenv('TRANSLATE_END')
        cog_key = os.getenv('TRANSLATE_kEY')
        cog_reg = os.getenv('COG_SERVICE_REG')

        text = request.POST.get('text')
        target_language = request.POST.get('trg_lang')
        if target_language == None or target_language == "undefined":
            target_language ='en'
        source_language = detect(cog_end,cog_key,cog_reg,text)
        
        path = 'translate'
        url = cog_end+path

        params = {
            'api-version': '3.0',
            'from': source_language,
            'to': target_language
        }

        headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': cog_reg,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        request = requests.post(url, params=params, headers=headers, json=body)
        response = request.json()
        # translation = response[0]["translations"][0]["text"]
        response_data = {
                'success': True,
                'message': response[0]["translations"][0]["text"]
            }
        return JsonResponse(response_data)


def detect(cog_end,cog_key,cog_reg,text):
    
    # Use the Translator detect function
    path = 'detect'
    url = cog_end + path

    # Build the request
    params = {
        'api-version': '3.0'
    }

    headers = {
    'Ocp-Apim-Subscription-Key': cog_key,
    'Ocp-Apim-Subscription-Region': cog_reg,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()

    # Parse JSON array and get language
    language = response[0]["language"]
    return language