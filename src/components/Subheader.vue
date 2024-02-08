<template>

    <div v-if="type === 'text'" class="sub-header">
        <Button url="copy.png" @click="onCopy" text="Copy Text" />
        <Button url="speaker.png" @click="onSpeak" text="Listen" />
        <Button url="language.png" @click="onTranslate" text="Translate" />
    </div>
    <div v-if="type === 'translate'" class="sub-header">
        <Button url="copy.png" @click="onCopyTranslate" text="Copy Text" />
        <Button @click="onSpeakTranslated" url="speaker.png" text="Listen" />
    </div>
</template>

<script>
import Button from './Button.vue';


export default {
    name:"Subheader",
    components:{
        Button,
    },
    props:["type"],
    methods:{
        onTranslate(){
            this.$emit('show-translate',2);
        },
        onCopy(){
            this.$emit('copyText');
        },
        onSpeak(){
            this.$emit('speak-text')
        },
        onSpeakTranslated(){
            this.$emit('speak-translated')
        },
        onCopyTranslate(){
            this.$emit('copy-translated')
        }
    }
}
</script>