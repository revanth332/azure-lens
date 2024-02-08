<template>
  <div class="picker-container">
    <div class="from-language">Auto-detect</div>
    <div class="arrow"><img src="../assets/images/arrow-right.png" alt="arrow-right"></div>
    <div class="to-language">
      <input @change="changeLanguage" class="language-list" type="text" v-model="selectedLanguage" list="languages" />
      <!-- The data list -->
      <datalist  id="languages">
        <option v-for="language in languages" :value="language.lcode" v-bind:key="language.lcode">{{language.lname}}</option>
      </datalist>
    </div>
  </div>
</template>

<script>
export default{
    name: 'LanguagePicker',
    data(){
        return {
            selectedLanguage:'en',
            languages : [],
        }
    },
    created(){
        fetch('https://api.cognitive.microsofttranslator.com/languages?api-version=3.0').then(res => res.json()).then(data => {
                let languages_data = data['translation'];
                for(let language in languages_data){
                    this.languages.push({lcode:language,lname:languages_data[language].name})
                }
                //console.log(this.languages)
            })
    },
    methods:{
        changeLanguage(){
            this.$emit('language-change',2,this.selectedLanguage);
        }
    }
}
</script>

<style scoped>
.picker-container{
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    /* border:1px solid black; */
    width:20rem;
    background-color: white;
    border-radius: 25px;
    padding:7px;
}
img{
    width:1rem;
    /* border:1px solid black; */
    display: block;
}
.language-list,.from-language{
    padding:10px;
    border-radius:20px;
    background-color: rgb(210,227,252);
    width:7rem;
    border:none;
    outline:none;
    text-align: center;
    font-weight:bold;
    font-size:1.1rem;
}
</style>
