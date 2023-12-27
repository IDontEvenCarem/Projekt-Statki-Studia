<script setup lang="ts">
import { ref } from 'vue';

const name = ref('');
const isPublic = ref(false);

const $emit = defineEmits<{
    createGame: [name: string, is_public: boolean]
}>()

function onClick () {
    if (name.value.length === 0) {
        return;
    }
    $emit('createGame', name.value, isPublic.value);
}

</script>

<template>
    <div class="wrapper">
        <h2>Stwórz nową grę</h2>
        <input 
            type="text" 
            placeholder="Nazwa gry" 
            maxlength="32"
            v-model="name"    
        />
        <button
            @click="onClick"
        >Stwórz nową grę</button>
        <div>
            <input type="checkbox" id="public" v-model="isPublic" />
            <label for="public">Publiczna</label>
        </div>
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