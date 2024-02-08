<template>
    <div v-if="clean" class="upload">
        <div>
            <input class="upload-field" @change="onFileChange" type="file">
        </div>
        <Button url="upload.png" @click="onSubmit" text="SUBMIT" />
    </div>
    <div v-else class="upload">
        <img :src="imageData" alt="image">
    </div>
    
</template>

<script>
import Button from './Button.vue';
export default {
    name:"Upload",
    components:{
        Button
    },
    props:["selected","clean"],
    data (){
        return {
            file : null,
            imageData : null,
        }
    },
    emits:['show-uploaded','show-process'],
    methods:{
        onFileChange(event){
            this.file = event.target.files[0];
        },
        onSubmit(){
            if(!this.file.type.startsWith('image/')){
                alert("Chose image file only "+this.file.type)
                return;
            }
            this.$emit('show-process',4);
            const reader = new FileReader();
            reader.onload = () => {
                this.imageData = reader.result;
            };
            reader.readAsDataURL(this.file);

            const formData = new FormData();
            formData.append('image',this.file);
            
            try{
                // this.imageData = null;
                // this.file = null;
                
                fetch('http://127.0.0.1:8000/respond/',{
                    method:'POST',
                    body:formData,
                }).then(res => res.json()).then(data => {
                    let result_text = "";
                    for(let text of data.message){
                        result_text+=text+"\n";
                    }
                    console.log(data)
                    this.$emit("show-uploaded",1,result_text)
                }).catch(err => console.log(err));
                
                
            }catch(e){
                console.log(e);
            }
        }
    }
}
</script>

<style scoped>
.upload{
    height:60%;
    width:90%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    padding:0 10px;
    /* box-shadow:-3px -3px 10px #ffffff70,
                3px 3px 15px #00000070; */
    background-color: white;
}
img{
    height:90%;
    width:100%;
    object-fit: contain;
}
.upload-field{
    padding:.5rem;
    background-color: #f2f2f2;
    border: none;
    padding: 10px;
    font-size: 1rem;
    color: #333;
}
</style>