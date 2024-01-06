<script setup lang="ts">
import { ref } from 'vue';

const whichFieldActive = ref<'player' | 'enemy'>('player');

</script>

<template>
    <div class="wrapper">
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
</template>