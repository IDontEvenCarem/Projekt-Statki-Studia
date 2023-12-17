<template>
    <div class="base-button">
        <slot></slot>
    </div>
</template>

<style scoped>
.base-button {
    background-color: var(--main-color);
    border-radius: 0.25em;
    color: #fff;
    padding: 0.5em 1em;
    text-decoration: none;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    width: fit-content;
}
.base-button:hover {
    background-color: var(--main-color-darken);
}
</style>