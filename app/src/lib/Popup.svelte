<script lang="ts">
    import { onMount } from "svelte";
    import Portal from "svelte-portal";

    export let maxWidth: Number = 600;
    export let maxHeight: Number = 400;
    export let padding: string = "22px 42px 16px 32px";

    let isOpen = false;
    export const open = () => {
        isOpen = true;
    }
    export const close = () => {
        isOpen = false;
    }

    onMount(() => {
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                isOpen = false;
            }
        });
    });

    let mainPopupCont: HTMLDivElement;
    let cover: HTMLDivElement;
    let opacityTimeout: any;
    $: if (isOpen) {   
        clearTimeout(opacityTimeout);
        opacityTimeout = setTimeout(() => {
            if (mainPopupCont && cover) {
                mainPopupCont.style.opacity = "1";
                cover.style.opacity = "1";
            }
        }, 10);
    } else {
        clearTimeout(opacityTimeout);
        if (mainPopupCont && cover) {
            mainPopupCont.style.opacity = "0";
            cover.style.opacity = "0";
        }
    }
</script>
<Portal target="body">
    {#if isOpen}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="viewport-cover"
            bind:this={cover}
            on:click={close}>
        </div>
        <div class="main-popup-cont"
            style={`
                max-width: ${maxWidth}px;
                max-height: ${maxHeight}px;
                padding: ${padding};
            `}
            bind:this={mainPopupCont}>
            <button class="btn-close"
                on:click={() => {isOpen = false;}}>
                <svg class="icon-close" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
            </button>
            <slot></slot>
        </div>
    {/if}
</Portal>
<style>
    .main-popup-cont {
        position: fixed;
        top: 100px;
        left: 50vw;
        transform: translateX(-50%);
        width: fit-content;
        height: fit-content;
        box-shadow: var(--main-box-shadow);
        z-index: 10000000000;
        transition: .3s;
        border-radius: var(--main-border-radius);
        background-color: white;
        opacity: 0;
        overflow: hidden;
    }
    .viewport-cover {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.1);
        z-index: 1000000;
        transition: .3s;
        opacity: 0;
    }
    .btn-close {
        margin: 0;
        padding: 0;
        background-color: transparent;
        border: none;
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 10000000000;
    }
    .icon-close {
        width: 18px;
        height: 18px;
        color: rgba(0, 0, 0, 0.2);
        cursor: pointer;
    }
</style>