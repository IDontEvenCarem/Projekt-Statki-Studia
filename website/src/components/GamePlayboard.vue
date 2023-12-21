<template>
    <div class="game-playboard">
        <div class="board-header">
            <div class="board-title">
                <span>{{ title }}</span>
            </div>
        </div>
        <div class="board-wrapper">
            <div v-for="_ in 10*10" class="cell"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    title: string;
}>()
</script>

<style scoped>
.game-playboard {
    display: grid;
    grid-template: max-content 1fr / 1fr;
    place-items: center;
    place-content: center;
    width: 100%;
}
.board-wrapper {
    background-color: color-mix(in srgb, var(--main-color), #000);
    border-radius: calc(var(--border-radius) * 2);
    padding: calc(var(--border-radius) * 2);
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 0.3em;
    width: 100%;
}
.board-header {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    border-radius: calc(var(--border-radius) * 2) calc(var(--border-radius) * 2) 0 0;
    background-color: color-mix(in srgb, var(--main-color), #000);
    font-size: large;
}

.cell {
    background-color: var(--main-color);
    border-radius: var(--border-radius);
    aspect-ratio: 1;
}
</style>