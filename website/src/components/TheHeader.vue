<template>
    <div class="the-header">
        <div class="title">
            🚢💣
        </div>
        <div class="breadcrumbs">
            
        </div>
        <div class="right">
            <div class="user">
                <div class="user-name">
                    <span>Jan Kowalski</span>
                </div>
                <div class="user-subline">
                    <span>1037 Pkt.</span>
                </div>
                <div class="user-avatar">
                    <img src="https://picsum.photos/50/50" alt="avatar">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.the-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5em 1em;
    background-color: var(--main-color);
    color: #fff;
    box-sizing: border-box;
    border-radius: var(--border-radius);
}

.title {
    font-size: 1.5em;
    font-weight: bold;
}

.right {
    display: flex;
    align-items: center;
}
.user {
    display: grid;
    align-items: center;
    gap: 0.1em 0.5em;
    grid-template: "name avatar" auto
                   "subline avatar" auto / auto 50px;
    text-align: right;
}
.user-name {
    font-weight: bold;
}
.user-subline {
    font-size: 0.8em;
}
.user-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    overflow: hidden;
    grid-area: avatar;
}

</style>
