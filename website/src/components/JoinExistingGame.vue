<script setup lang="ts">
import { ref } from 'vue';

defineEmits<{
    joinGame: [gameCode: string]
}>()

const value = ref('');

</script>

<template>
    <div class="wrapper">
        <h2>Dołącz do gry</h2>
        <input 
            type="text" 
            placeholder="Wprowadź kod gry" 
            maxlength="8"
            v-model="value" 
        />
        <button 
            @click="$emit('joinGame', value)"
            :disabled="value.length !== 8"
        >Dołącz do gry</button>
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
    filter: drop-shadow(-4px 4px 5px  color-mix(in srgb, var(--main-color) 50%, #000));
    padding: 1em;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}

input {
    display: block;
}

</style>
