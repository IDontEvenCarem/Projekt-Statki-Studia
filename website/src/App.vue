<script setup lang="ts">
import BaseButton from './components/BaseButton.vue';
import TheHeader from './components/TheHeader.vue';

</script>

<template>
  <div class="main-layout">
    <TheHeader></TheHeader>
    <div class="content">
      <BaseButton>
        Rozpocznij nową grę
      </BaseButton>
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  display: grid;
  grid-template: auto 1fr / 1fr;
  padding: 1em;
  box-sizing: border-box;
  flex-direction: column;
  min-height: 100vh;
  gap: 1em;
}
</style>
