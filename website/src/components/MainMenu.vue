<script setup lang="ts">
import JoinExistingGame from './JoinExistingGame.vue';
import CreateNewGame from './CreateNewGame.vue';
import PublicGamesList from './PublicGamesList.vue';

</script>

<template>
    <div class="main-menu__root">
        <div class="main-menu__title">Statki</div>
        <JoinExistingGame></JoinExistingGame>
        <h2 class="main-menu__separator">lub</h2>
        <CreateNewGame></CreateNewGame>
        <PublicGamesList class="main-menu__public-games-list"></PublicGamesList>
    </div>
</template>

<style scoped>
.main-menu__root {
    display: grid;
    grid-template: max-content 1fr auto / 1fr min-content 1fr;
    gap: 2em 0.25em;
    place-items: center;
    text-align: center;
    background-color: var(--main-color);
    border-radius: var(--border-radius);
    padding: 20px 50px 50px;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
    filter: drop-shadow(-0.3em 0.3em 0.2em color-mix(in srgb, var(--background-color), #000));
}

.main-menu__title {
    font-size: 3em;
    font-weight: bold;
    color: var(--main-color-light);
    grid-area: 1 / 1 / 2 / 5;
    padding: 0;
    margin: 0;
}

.main-menu__separator {
    color: var(--main-color-light);
    font-size: 1.5em;
    font-weight: bold;
    padding: 0 2em;
}

.main-menu__public-games-list {
    grid-area: 3 / 1 / 4 / 5;
}
</style>
