<script setup lang="ts">
import { computed, ref } from 'vue';
import GamePlayboard from './GamePlayboard.vue';

type ShipInfo = {
    size: number;
    name: string;
    position: null | {
        x: number;
        y: number;
        direction: 'horizontal' | 'vertical';
    };
}

const shipInfos : ShipInfo[] = [
    {
        size: 5,
        name: 'Lotniskowiec',
        position: null,
    },
    {
        size: 4,
        name: 'Pancernik',
        position: null,
    },
    {
        size: 3,
        name: 'Krążownik',
        position: null,
    },
    {
        size: 3,
        name: 'Okręt podwodny',
        position: null,
    },
    {
        size: 2,
        name: 'Niszczyciel',
        position: null,
    },  
]

const selectedShip = ref<ShipInfo['name'] | null>(null);
const previewPosition = ref<{ x: number; y: number; } | null>(null);
const currentDirection = ref<'horizontal' | 'vertical'>('horizontal');


const shownShips = computed(() => {
    return shipInfos.flatMap(ship => {
        if (ship.name === selectedShip.value && previewPosition.value !== null) {
            return [{
                isPreview: true,
                size: ship.size,
                direction: currentDirection.value,
                x: previewPosition.value?.x ?? 0,
                y: previewPosition.value?.y ?? 0,
            }]
        }

        if (ship.position === null) {
            return [];
        }
        return [{
            isPreview: false,
            size: ship.size,
            direction: ship.position?.direction ?? 'horizontal',
            x: ship.position?.x ?? 0,
            y: ship.position?.y ?? 0,
        }];
    })
})

function onCellClick (x: number, y: number) {
    if (selectedShip.value === null) {
        return;
    }

    const ship = shipInfos.find(ship => ship.name === selectedShip.value);
    if (ship === undefined) {
        return;
    }

    ship.position = {
        x,
        y,
        direction: currentDirection.value,
    }
    selectedShip.value = null;
}

function onShipClick(ship: ShipInfo) {
    if (ship.position === null) {
        // Not placed yet
        selectedShip.value = ship.name;
    } else {
        // Already placed
        ship.position = null;
        selectedShip.value = ship.name;
    }
}

const $emit = defineEmits<{
    ready: [],
}>()

</script>

<template>
    <div class="wrapper">
        <GamePlayboard
            :style="{ 'height': '100%' }"
            :ships="shownShips"
            @hover-cell="(x, y) => previewPosition = { x, y }"
            @click-cell="onCellClick"
            @unhover-grid="() => previewPosition = null"
        />
        <div class="ships-to-place box">
            <div class="title">Statki do rozmieszczenia:</div>
            <div class="ships">
                <div 
                    class="ship" 
                    v-for="ship in shipInfos" 
                    :class="{ 
                        placed: ship.position !== null,
                        selected: selectedShip === ship.name,
                    }"
                    @click="onShipClick(ship)"
                >
                    <div class="ship-name">{{ ship.name }}</div>
                    <div class="ship-preview">
                        <div class="ship-preview__cell" v-for="_ in ship.size"></div>
                    </div>
                </div>
            </div>
            <div class="direction">
                <button
                    @click="currentDirection = currentDirection === 'horizontal' ? 'vertical' : 'horizontal'"
                    class="direction__button"
                >
                    Kierunek:
                    {{ 
                        currentDirection === 'horizontal' ? '↔️ Poziomy' : '↕️ Pionowy'  
                    }}
                </button>
            </div>
            <div class="ready">
                <button
                    @click="() => $emit('ready')"
                    class="ready__button"
                    :disabled="shipInfos.some(ship => ship.position === null)"
                >
                    Gotowy
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.wrapper {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    height: 100%;
    gap: 20px;
}

.ships-to-place {
    display: flex;
    flex-direction: column;
    width: max-content;
    height: 100%;
}

.title {
    font-size: 1.4rem;
    font-weight: bold;
    text-align: center;
}

.ships {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.ship {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 10px;
    border-radius: var(--border-radius);
    background-color: var(--main-color);
    color: #fff;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease;
}

.ship.selected {
    background-color: #fff;
    color: #000;
}

.ship.placed {
    background-color: #3a3;
}

.ship-name {
    font-size: 1.2rem;
    font-weight: bold;
}

.ship-preview {
    display: flex;
    gap: 5px;
}

.ship-preview__cell {
    background-color: color-mix(in srgb, var(--main-color), #000);
    border-radius: var(--border-radius);
    aspect-ratio: 1;
    display: grid;
    place-items: center;
    width: 20px;
}

.direction {
    display: flex;
    flex-direction: column;
    padding: 10px 0 0;
}

.direction__button {
    padding: 10px;
}

.ready {
    display: flex;
    flex-direction: column;
    padding: 10px 0;
}

.ready__button {
    padding: 10px;
}
</style>