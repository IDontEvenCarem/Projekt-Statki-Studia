<script setup lang="ts">
export type ShipData = {
    x: number;
    y: number;
    size: number;
    direction: 'horizontal' | 'vertical';
    isPreview?: boolean;
}

const props = defineProps<{
    ships?: ShipData[];
    cellStatuses?: {
        x: number;
        y: number;
        status: 'empty' | 'hit' | 'miss';
    }[];
}>()

const $emit = defineEmits<{
    clickCell: [x: number, y: number];
    hoverCell: [x: number, y: number];
    unhoverGrid: [];
}>()

function to_letter (num: number) {
    return String.fromCharCode(64 + num);
}

function shipStyle (ship: ShipData) {
    const fromX = ship.x + 1;
    const fromY = ship.y + 1;
    let toX = ship.x + (ship.direction === 'horizontal' ? 1 : ship.size) + 1;
    let toY = ship.y + (ship.direction === 'vertical' ? 1 : ship.size) + 1;
    let outOfBounds = false;
    if (toX > 12) {
        toX = 12;
        outOfBounds = true;
    }
    if (toY > 12) {
        toY = 12;
        outOfBounds = true;
    }

    return {
        gridArea: `${fromX} / ${fromY} / ${toX} / ${toY}`,
        opacity: ship?.isPreview ? 0.5 : 1,
        backgroundColor: outOfBounds ? '#f00' : undefined,
    }
}

function cellStyle (x: number, y: number) {
    return {
        gridArea: `${x+1} / ${y+1} / ${x+2} / ${y+2}`,
    }
}

function cellClass (x: number, y: number) {
    const cellStatus = props.cellStatuses?.find(cell => cell.x === x && cell.y === y)?.status;
    return {
        'cell--hit': cellStatus === 'hit',
        'cell--miss': cellStatus === 'miss',
    }
}

</script>

<template>
    <div class="game-playboard">
        <div 
            class="board-wrapper"
            @mouseleave="$emit('unhoverGrid')"
        >
            <div class="row">
                <div></div>
                <div class="header-cell" v-for="x in 10">{{ to_letter(x) }}</div>
            </div>
            <div 
                v-for="y in 10" 
                class="row"
                :key="y"
            >
                <div class="header-cell" :key="-1">{{ y }}</div>
                <div v-for="x in 10" 
                    class="cell" 
                    @click="$emit('clickCell', x, y)" 
                    @mouseover="$emit('hoverCell', x, y)"
                    :key="x + y"
                    :class="cellClass(x, y)"
                    :style="cellStyle(x, y)"
                >
                    {{ to_letter(y) }}{{ x }}
                </div>
            </div>
            <div v-for="ship in ships"
                class="ship"
                :style="shipStyle(ship)"
            >
                <div class="ship-inner"></div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.game-playboard {
    display: grid;
    grid-template: max-content 1fr / 1fr;
    place-items: center;
    place-content: center;
    width: 100%;
    aspect-ratio: 1;
}
.board-wrapper {
    background-color: color-mix(in srgb, var(--main-color), #000);
    border-radius: calc(var(--border-radius) * 2);
    padding: calc(var(--border-radius) * 2);
    display: grid;
    grid-template-columns: repeat(11, 1fr);
    grid-template-rows: repeat(11, 1fr);
    gap: 4px;
    width: 100%;
    box-sizing: border-box;
}
.row {
    display: contents;
}

.cell {
    background-color: var(--main-color);
    border-radius: var(--border-radius);
    aspect-ratio: 1;
    display: grid;
    place-items: center;
    color: transparent;
    font-size: large;
    transition: background-color 0.2s ease, color 0.2s ease;
}
.cell--hit {
    background-color: #f00;
}
.cell--miss {
    background-color: #fff;
    color: #000;
}
.header-cell {
    border-radius: var(--border-radius);
    aspect-ratio: 1;
    display: grid;
    place-items: center;
    color: #fff;
    font-size: large;
}

.ship {
    padding: 5px;
    pointer-events: none;
}
.ship-inner {
    background-color: color-mix(in srgb, var(--main-color) 66%, #000);
    border-radius: var(--border-radius);
    width: 100%;
    height: 100%;
}

.cell:hover {
    background-color: color-mix(in srgb, var(--main-color) 66%, #fff);
    color: #fff;
}
</style>