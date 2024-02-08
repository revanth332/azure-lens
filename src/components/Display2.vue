<template>
    <div class="display">
        <h3>Translated text</h3>
        <Subheader @copy-translated="copyTranslated" @speak-translated="speakTranslated" type="translate"/>
        <div v-if="text === ''" class="response">
            <Spinner />
        </div>
        <div ref="copyDiv" v-if="text !== ''" class="response">
            {{text}}
        </div>
    </div>
    
</template>

<script>
import Subheader from './Subheader.vue'
import Spinner from './Spinner.vue';

export default {
    name:"Display2",
    components :{
        Subheader,
        Spinner,
    },
    props:['text'],
    data(){
        return {
            text_data : this.text,
        }
    },
    methods:{
        speakTranslated(){
            const formData = new FormData();
            formData.append('text',this.text)
            fetch('http://127.0.0.1:8000/speak/',{
                method:'POST',
                body:formData
            }).then(response => response.json())
                .then(data => {
                    console.log("speech successful")
                })
                .catch(error => console.error('Error fetching audio:', error));
        },
        copyTranslated(){
            const copyDiv = this.$refs.copyDiv;
            const range = document.createRange();
            range.selectNode(copyDiv);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand("copy");
            window.getSelection().removeAllRanges();
            alert('copied successfully')
        }
    }
}
</script>

<style scoped>
h3{
    margin:1rem;
}
.response{
    margin:1rem;
    font-size: 1.2rem;
    background-color: rgb(244, 245, 246);
    padding:.5rem;
    color:rgb(117,132,157)
}
</style>