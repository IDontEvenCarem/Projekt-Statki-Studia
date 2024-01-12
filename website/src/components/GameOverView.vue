<script setup lang="ts">
import { useStore } from '../store';

const store = useStore();

function onRestart() {
    window.location.reload();
}

</script>

<template>
    <div class="wrapper">
        <div v-if="store.self_won">
            <h2>Wygrałeś!</h2>
        </div>
        <div v-else>
            <h2>Przegrałeś!</h2>
        </div>
        <button @click="onRestart" class="replay-button">Zagraj ponownie</button>
    </div>
</template>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    gap: 0.25em;
    align-items: center;
    text-align: center;
    background-color: color-mix(in srgb, var(--main-color) 75%, #000);
    border-radius: var(--border-radius);
    filter: drop-shadow(-4px 4px 5px  color-mix(in srgb, var(--main-color) 50%, #000));
    padding: 1em;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}

.replay-button {
    padding: 10px;
    font-size: larger;
}

</style>