<script setup lang="ts">
import { useStore } from '../store';

const store = useStore();

function onClick () {
    store.createNewGame();
}

</script>

<template>
    <div class="wrapper">
        <h2>Stwórz nową grę</h2>
        <button
            @click="onClick"
        >Stwórz nową grę</button>
    </div>
</template>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    gap: 0.25em;
    align-items: stretch;

    text-align: center;
    background-color: color-mix(in srgb, var(--main-color) 75%, #000);
    border-radius: var(--border-radius);
    filter: drop-shadow(-4px 4px 5px color-mix(in srgb, var(--main-color) 50%, #000));
    padding: 1em;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}

</style>