<template>

  <header class="navbar">
    <div class="logo">
      <h3>Azure Lens</h3> 
    </div>
    <div class="upload">
     <button class ="up-btn" @click="setDefault"><img src="./assets/images/upload.png" alt="upload" width="20"> Upload</button>
    </div>
  </header>

  <div class="main-container">
    
    <div class="upload-container">
      <!-- upload component -->
      <LanguagePicker v-if="translated" @language-change="changeView" />
      <Upload :clean="cleaned" :selected="uploaded" @show-uploaded="changeView" @show-process="changeView" />
    </div>
    <div class="display-container">
      <div class="view" v-if="defaulted">
        <Default />
      </div>
      <div class="view" v-if="translated">
        <Display2 :text="translated_data" />
      </div>
      <div class="view" v-if="uploaded">
        <Display1 :text = "text_data" @show-translate="changeView" />
      </div>
      
    </div>
  </div>
</template>

<script>
import Upload from './components/Upload.vue';
import Display1 from './components/Display1.vue';
import Display2 from './components/Display2.vue';
import Default from './components/Default.vue';
import LanguagePicker from './components/LanguagePicker.vue';
import Spinner from './components/Spinner.vue'
export default{
  name:'App',
  components: { Display1,Display2,Upload,Default,LanguagePicker,Spinner},
  data (){
    return {
      uploaded : false,
      translated:false,
      defaulted : true,
      text_data : "",
      translated_data : "",
      cleaned : true
    }
  },
  emits:['show-uploaded','show-process'],
  methods:{
    setDefault(){
      console.log("upload")
      this.changeView(3);
      this.cleaned = true;
    },
    changeView(id,txt){
      if(id === 1){
        this.uploaded = true;
        this.translated=false;
        this.defaulted = false;
        this.text_data = txt;
        this.cleaned = false;
      }
      if(id === 2){
        this.uploaded = false;
        this.translated=true;
        this.defaulted = false;

        const formData = new FormData()
        formData.append('text',this.text_data)
        formData.append('trg_lang',txt)
        fetch('http://127.0.0.1:8000/translate/',{
          method:"POST",
          body:formData,
        }).then(res => res.json()).then(data => {
          this.translated_data = data.message
        })
      }
      if(id == 3){
        this.uploaded = false;
        this.translated=false;
        this.defaulted = true;
      }
    }
  }   
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap');

*{
  padding:0;
  margin:0;
  font-family: 'Comfortaa', cursive;
  font-family: 'Raleway', sans-serif;
  font-family: 'Roboto Mono', monospace;
}
h3{
color:rgb(125, 122, 122);
}
.up-btn{
  background:none;
  font-size: 1em;
  color:rgb(125, 122, 122);
  font-weight: 400;
  border:none;
  
}
.view{
  height:100%;
}
.navbar {
  padding:1.3rem 10rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.3em;
  border-bottom:1px solid rgb(235, 233, 233);
  color:rgb(125, 122, 122);
  font-weight: 400;
}
.main-container{
    display: flex;
    align-items: center;
}
.upload-container,.display-container{
  border:1px solid black;
  width:50%;
  height:90vh;
}
.upload-container{
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex-direction: column;
  background-color: rgb(32,33,36);
}
</style>