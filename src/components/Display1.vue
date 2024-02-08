<template>
    <div class="display">
        <h3>Image Text:</h3><br>
        <div ref="copyDiv" v-if="text !== ''" class="response">  
            {{text}}
        </div>
        <div class="response spin" v-if="text == ''">
            <Spinner />
        </div>
        <Subheader @speak-text="onSpeakText" @copyText="onCopyText" @show-translate="$emit('show-translate',2)" type="text" />
    </div>
</template>

<script>
import Subheader from './Subheader.vue';
import Spinner from './Spinner.vue';
export default {
    name:"Display1",
    components :{
        Subheader,
        Spinner,
    },
    data(){
        return {
            text_data : this.text,
            audio_element : null,
        }
    },
    props:["text"],
    emits:['show-translate','copyText','speak-text'],
    methods:{
        onCopyText(){
            const copyDiv = this.$refs.copyDiv;
            const range = document.createRange();
            range.selectNode(copyDiv);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand("copy");
            window.getSelection().removeAllRanges();
            alert('copied successfully')
        },
        onSpeakText(){
            const formData = new FormData();
            formData.append('text',this.text_data)
            fetch('http://127.0.0.1:8000/speak/',{
                method:'POST',
                body:formData
            }).then(response => response.json())
                .then(data => {
                    const audioBase64 = data.audio_base64;
                    const audioBlob = this.base64toBlob(audioBase64);
                    const audioURL = URL.createObjectURL(audioBlob);
                    this.audioElement = new Audio(audioURL);
                    // this.audioElement.play()
                    // if (this.audioElement.paused) {
                    // this.speaking = false;
                    // } else {
                    // this.speaking = true;
                    // }
                })
                .catch(error => console.error('Error fetching audio:', error));
                
        },
        base64toBlob(base64) {
            const byteCharacters = atob(base64);
            const byteArrays = [];
            for (let i = 0; i < byteCharacters.length; i++) {
                byteArrays.push(byteCharacters.charCodeAt(i));
            }
            return new Blob([new Uint8Array(byteArrays)], { type: 'audio/wav' });
        },
        
    }
}
</script>

<style scoped>

.response{
    margin:0 1rem;
    font-size: 20px;
    background-color: rgb(244, 245, 246);
    padding:.5rem;
    color:rgb(117,132,157)
}
h3{
    margin:1rem;
}
.spin{
    text-align: center;
    background-color: white;
}
</style>