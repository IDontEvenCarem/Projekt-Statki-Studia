<script setup lang="ts">
import { computed } from 'vue';
import GamePlayboard from './GamePlayboard.vue';
import { useStore } from '../store';

const store = useStore();

const ownShips = computed(() => {
    return store.ships.flatMap(ship => {
        if (ship.placed === false) {
            return [];
        }
        return [{
            isPreview: false,
            size: ship.size,
            direction: ship.direction,
            x: ship.position?.x ?? 0,
            y: ship.position?.y ?? 0,
        }];
    })
});

const ownFieldStatuses = computed(() => {
    return Object.entries(store.ownCellStatus).map(([k, status]) => {
      const [y, x] = k.split(';').map(Number);
      return {
            x,
            y,
            status
        }
    })
});

const enemyFieldStatuses = computed(() => {
    return Object.entries(store.enemyCellStatus).map(([k, status]) => {
      const [x, y] = k.split(';').map(Number);
      return {
            x,
            y,
            status
        }
    })
});

function tryToShoot(x: number, y: number) {
  if (!store.my_turn) {
    return;
  }
  store.shoot(x, y);
}

</script>

<template>
    <div class="wrapper">
      <div 
        class="box playboard-wrapper"
        :class="{ active: store.my_turn}"        
      >
        <div class="playboard-title">
          Plansza przeciwnika
        </div>
        <GamePlayboard 
          id="enemy-field" 
          @clickCell="tryToShoot"
          :cellStatuses="enemyFieldStatuses"
        />
      </div>

      <div 
        class="box playboard-wrapper"
        :class="{ active: !store.my_turn }"  
      >
        <div class="playboard-title">
          Twoja plansza
        </div>
        <GamePlayboard 
          id="player-field" 
          :ships="ownShips"
          :cellStatuses="ownFieldStatuses"
        />
      </div>
    </div>
</template>

<style scoped>

.wrapper {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1em;
    padding: 1em;
    width: 100%;
    box-sizing: border-box;
}

.playboard-wrapper {
  max-width: 50%;
  flex-grow: 1;
  border-radius: calc(var(--border-radius) * 2);
  transition: background-color 0.4s ease, scale 0.4s ease;
}
.playboard-wrapper:not(.active) {
  background-color: color-mix(in srgb, var(--main-color) 50%, #fff);
  scale: 0.8; 
}

.active {
  scale: 1;
}


.playboard-title {
  font-size: 1.4rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 0.5em;
}


</style>
