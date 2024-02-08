<template>
    <button class="ft-button">
        <div class="btn-conatiner">
        <img :src="`src/assets/images/${url}`" alt="upload" width="20">
        {{text}}
        </div>
    </button>
</template>

<script>
export default {
    name:"Button",
    props:["text","url"],
}
</script>

<style scoped>
.btn-conatiner{
  display: flex;
  align-items: center;
}
button {
  background-color: #f3f7fe;
  color: #3b82f6;
  border: none;
  border-radius: 8px;
  width: 150px;
  height: 45px;
  transition: .3s;
  margin:1.5rem 1rem;
  font-size:1.2rem;
}   
img{
  margin:0 .6rem;
}
/* button:hover {
  background-color: #3b82f6;
  box-shadow: 0 0 0 5px #3b83f65f;
  color: #fff;
} */

</style>