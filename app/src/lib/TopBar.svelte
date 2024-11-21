<div class="top-menu">
    <div class="links">
        <slot name="links"></slot>
    </div>
    <div class="name">
        <slot name="name"></slot>
    </div>
    <div class="buttons">
        <slot name="buttons"></slot>
    </div>
</div>
<style>
    .links, .name, .buttons {
        display: flex;
        align-items: center;
        -moz-user-select: -moz-none;
        -khtml-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    .top-menu {
        position: relative;
        height: 68px;
        width: 100%;
        background-color: rgb(34,34,34);
        display: flex;
        justify-content: space-between;
        vertical-align: middle;
    }
    .top-menu .buttons, .top-menu .links {
        height: fit-content;
        align-self: center;
    }
    .buttons {
        margin-right: 16px;
        gap: 8px;
    }
    .links {
        margin-left: 16px;
        gap: 30px;
    }
    .links * {
        cursor: pointer;
    }
</style>