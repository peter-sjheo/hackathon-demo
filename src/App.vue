<template>
  <div class="app-container">
    <MainContainer />
  </div>
</template>

<script setup>
import MainContainer from './components/MainContainer.vue'
</script>

<style scoped>
.app-container {
  width: 100%;
  min-height: 100vh;
  /* CHUBB Dark Blue → Purple 그라데이션 */
  background: linear-gradient(135deg, #002855 0%, #7030A0 100%);
}
</style>
