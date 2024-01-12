<script setup lang="ts">
import { CommunicationApi } from './comms';
import GamePrepView from './components/GamePrepView.vue';
import GamePlayView from './components/GamePlayView.vue';
import MainMenu from './components/MainMenu.vue';
import { computed, onMounted, ref } from 'vue';
import { useStore } from './store';

const store = useStore();
const comms = ref<CommunicationApi | null>(null);
const error = ref<string | null>(null);

onMounted(() => { 
  comms.value = new CommunicationApi("ws://localhost:5001"); 

  comms.value?.addEventListener('open', () => {
    store.setConnection(comms.value!);
  });

  comms.value?.addEventListener('message', (event) => {
    console.log(event);
  });

  comms.value?.addEventListener('error', (event) => {
    const details = (event as CustomEvent).detail;
    console.dir(details)
    error.value = `Wystąpił błąd: ${details.toString()}`
  });

  comms.value.addEventListener('enemy_joined', (_event) => {
    store.setOtherPlayerStatus("present");
  });

  return () => { comms.value?.close(); }
});

const phase = ref<'preparation' | 'gameplay'>('preparation');
const otherPlayerStatusText = computed(() => {
  switch (store.other_player_status) {
    case 'present':
      return 'Obecny';
    case 'not-present':
      return 'Nieobecny';
    case 'ready':
      return 'Gotowy';
    case 'playing':
      return 'Gra';
  }
});
</script>

<template>
  <div class="main-layout">
    <div class="loading-overlay" :class="{ active: store.showLoadingScreen }">
      <div class="loading-inner-box" v-if="store.showLoadingScreen && !error">
        <div class="loading-spinner"></div>
        <div class="loading-text">Oczekiwanie na odpowiedź serwera...</div>
      </div>
      <div class="loading-inner-box" v-if="error">
        <div class="loading-text">{{ error }}</div>
      </div>
    </div>
    <div class="toasts">
      <div class="toast" v-for="toast in store.toasts" :key="toast.text" :class="{ error: toast.type === 'error' }">
        {{ toast.text }}
      </div>
    </div>
    <MainMenu v-if="store.phase === 'main-menu'" />
    <div class="content" v-else>
      <div class="game-header">
        <div class="game-header__title">Statki</div>
        <div class="game-header__game-code">Kod gry: {{ store.game_id }}</div>
        <div class="game-header__phase" v-if="store.phase === 'placing-ships'">Faza: przygotowanie</div>
        <div class="game-header__phase" v-if="store.phase === 'waiting-for-other-player'">Faza: czekanie na przeciwnika</div>
        <div class="game-header__phase" v-else>Faza: rozgrywka</div>
        <div class="game-header__other-player-status" v-if="phase === 'preparation'">
          Status przeciwnika: {{ otherPlayerStatusText }}
        </div>
      </div>
      <GamePrepView v-if="store.phase === 'placing-ships'" />
      <div v-if="store.phase === 'waiting-for-other-player'">
        <div class="waiting-for-other-player box">
          <div class="waiting-for-other-player__title">Oczekiwanie na drugiego gracza...</div>
          <div class="waiting-for-other-player__spinner"></div>
        </div>
      </div>
      <GamePlayView v-if="store.phase === 'playing'" />
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

.loading-overlay .loading-spinner,
.waiting-for-other-player__spinner {
  border: 16px solid #f3f3f3;
  border-radius: 50%;
  border-top: 16px solid var(--main-color);
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
}

.waiting-for-other-player {
  display: grid;
  place-items: center;
  place-content: center;
  gap: 1em;
  padding: 1em;
  width: fit-content;
  height: fit-content;
  box-sizing: border-box;
}

.waiting-for-other-player__title {
  font-size: 1.2em;
  font-weight: bold;
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

.game-header {
  width: 100%;
  grid-area: 1/1/2/2;
  background-color: var(--main-color);
  border-radius: var(--border-radius);
  padding: 20px;
  margin-bottom: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  gap: 2em;
  align-items: center;
}

.game-header__title {
  font-size: 1.2em;
  font-weight: bold;
  color: var(--main-color-light);
  padding: 0;
  margin: 0;
}

.active {
  z-index: 1;
}

.toasts {
  position: fixed;
  top: 0;
  right: 0;
  padding: 2em;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 1em;
  z-index: 100;
  pointer-events: none;
}

.toast {
  padding: 1em;
  box-sizing: border-box;
  background-color: var(--main-color);
  color: var(--main-color-light);
  border-radius: var(--border-radius);
  font-size: 1.2em;
  font-weight: bold;
  min-width: 100px;
  min-height: 20px;
  filter: drop-shadow(0px 0px 5px rgba(0, 0, 0, 0.5));
  pointer-events: all;
}

.toast.error {
  background-color: rgb(141, 31, 31);
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
