<template>
    <div class="loading-wave">
        <div class="loading-bar"></div>
        <div class="loading-bar"></div>
        <div class="loading-bar"></div>
        <div class="loading-bar"></div>
    </div>

</template>

<script>
export default {
  name:'Speaking',
}
</script>


<style scoped>
.loading-wave {
  width: 40px;
  height: 30px;
  display: inline;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin:0 auto;
}

.loading-bar {
  width: 2rem;
  height: 1rem;
  margin: 0 2px;
  background-color: #3498db;
  border-radius: 5px;
  animation: loading-wave-animation 1s ease-in-out infinite;
}

.loading-bar:nth-child(2) {
  animation-delay: 0.1s;
}

.loading-bar:nth-child(3) {
  animation-delay: 0.2s;
}

.loading-bar:nth-child(4) {
  animation-delay: 0.3s;
}

@keyframes loading-wave-animation {
  0% {
    height: 0.5rem;
  }

  50% {
    height: 1.5rem;
  }

  100% {
    height: 0.5rem;
  }
}

</style>