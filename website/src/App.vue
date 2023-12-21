<script setup lang="ts">
// import BaseButton from './components/BaseButton.vue';
import TheHeader from './components/TheHeader.vue';
import GamePlayboard from './components/GamePlayboard.vue';
import { ref } from 'vue';

const whichFieldActive = ref<'player' | 'enemy'>('player');

</script>

<template>
  <div class="main-layout">
    <TheHeader></TheHeader>
    <div 
      class="content"
      @click="whichFieldActive = whichFieldActive === 'player' ? 'enemy' : 'player'"
    >
      <GamePlayboard 
        id="enemy-field" 
        :class="{ active: whichFieldActive === 'enemy', 'field': true }"
        title="Plansza wroga"
      />
      <GamePlayboard 
        id="player-field" 
        :class="{ active: whichFieldActive === 'player', 'field': true }" 
        title="Twoja plansza"
      />
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  display: grid;
  grid-template: max-content 1fr / 1fr;
  padding: 1em;
  box-sizing: border-box;
  min-height: 100vh;
  gap: 1em;
}
.content {
  position: relative;
  display: grid;
  place-items: center;
  place-content: center;
  width: 100%;
  grid-template: 1fr / 1fr;
}

.field {
  width: 100%;
  max-width: 500px;
  position: absolute;
  transition: transform 0.4s ease;
  grid-area: 1/1/2/2;
  transform: translateY(-20%);
}

.field:not(.active) {
  transform: translateY(80%) scale(0.5) translateY(-40%);
}

.active {
  z-index: 1;
}

@media (min-width: 768px) {
  .field {
    width: 100%;
    max-width: 500px;
    position: static;
    transition: transform 0.4s ease;
    transform: translateX(-20%);
  }
  .field:not(.active) {
    transform: translateX(80%) scale(0.5) translateX(-40%);
  }
  .active {
    z-index: 1;
  }
}


</style>
