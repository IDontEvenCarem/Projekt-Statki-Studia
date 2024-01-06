<script setup lang="ts">
import { CommunicationApi } from './comms';
import GamePlayboard from './components/GamePlayboard.vue';
import MainMenu from './components/MainMenu.vue';
import { onMounted, ref } from 'vue';

const whichFieldActive = ref<'player' | 'enemy'>('player');

const gameIdentifier = ref<string | null>(null);

const comms = ref<CommunicationApi | null>(null);
const waiting = ref(false);
const error = ref<string | null>(null);

onMounted(() => { 
  comms.value = new CommunicationApi("ws://localhost:5001"); 

  comms.value?.addEventListener('message', (event) => {
    console.log(event);
  });

  comms.value?.addEventListener('error', (event) => {
    const details = (event as CustomEvent).detail;
    console.dir(details)
    error.value = `Wystąpił błąd: ${details.toString()}`
  });

  return () => { comms.value?.close(); }
});

async function joinGame (gameCode: string) {
  waiting.value = true;
  await comms.value?.joinGame(gameCode);
  waiting.value = false;
}

async function createGame () {
  waiting.value = true;
  const response = await comms.value?.createNewGame();
  if (response && response.game_id) {
    gameIdentifier.value = response.game_id;
  }
  waiting.value = false;
}


</script>

<template>
  <div class="main-layout">
    <div class="loading-overlay" :class="{ active: waiting || error }">
      <div class="loading-inner-box" v-if="waiting && !error">
        <div class="loading-spinner"></div>
        <div class="loading-text">Oczekiwanie na odpowiedź serwera...</div>
      </div>
      <div class="loading-inner-box" v-if="error">
        <div class="loading-text">{{ error }}</div>
      </div>
    </div>
    <MainMenu 
      v-if="!gameIdentifier" 
      @joinExistingGame="joinGame($event)"
      @createNewGame="createGame()"
    />
    <div class="content" v-else>
      <div class="game-identifier">Kod gry: {{ gameIdentifier }}</div>
      <GamePlayboard 
        id="enemy-field" 
        :class="{ active: whichFieldActive === 'enemy', 'field': true }"
        title="Plansza wroga" 
        @clickCell="() => whichFieldActive = 'player'"
        :ships="[{
          x: 1,
          y: 1,
          size: 4,
          direction: 'horizontal',
        }, {
          x: 3,
          y: 3,
          size: 3,
          direction: 'vertical',
        }]"
        :cellStatuses="[{
          x: 1,
          y: 1,
          status: 'hit',
        }, {
          x: 2,
          y: 1,
          status: 'miss',
        }]"
      />
      <GamePlayboard 
        id="player-field" 
        :class="{ active: whichFieldActive === 'player', 'field': true }"
        title="Twoja plansza" 
        @clickCell="() => whichFieldActive = 'enemy'"
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

.loading-overlay {
  position: fixed;
  display: grid;
  place-items: center;
  place-content: center;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 100;
  transition: opacity 0.4s ease;
}

.loading-overlay .loading-inner-box {
  display: grid;
  place-items: center;
  place-content: center;
  gap: 1em;
  background-color: var(--background-color);
  border-radius: var(--border-radius);
  padding: 1em;
  width: fit-content;
  height: fit-content;
  box-sizing: border-box;
}

.loading-overlay .loading-spinner {
  border: 16px solid #f3f3f3;
  border-radius: 50%;
  border-top: 16px solid var(--main-color);
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.loading-overlay .loading-text {
  font-size: 2em;
  font-weight: bold;
  color: var(--main-color);
}

.loading-overlay:not(.active) {
  opacity: 0;
  pointer-events: none;
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
