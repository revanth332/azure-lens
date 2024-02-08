<template>
    <div class="default">
        <div class="image-container">
            <img src="../assets/images/image2.png" alt="">
        </div>
        <h3>Upload Image to show response</h3>
    </div>
</template>

<script>
export default {
    name:"Default",
}
</script>

<style scoped>
.default{
    height:100%;
    display: flex;
    justify-content: space-evenly;
    flex-direction:column;
    align-items: center;
    color:rgb(117,132,157);
}
.image-container{
    background-color: aliceblue;
    border:none;
    border-radius:50%;
    padding:20px;
    width:20rem;
    height:20rem;
    display: flex;
    justify-content: center;
    align-items: center;
}
img{
    width:10rem;
}
</style>