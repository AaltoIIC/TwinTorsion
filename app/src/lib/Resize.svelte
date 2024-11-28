<script lang="ts">
    import { onMount } from 'svelte';

    export let direction: 'vertical' | 'horizontal' = 'horizontal';
    export let defaultFirstSize: number = 220;
    export let defaultSecondSize: number | null = null;
    export let minFirstSize: number | null = null;
    export let maxFirstSize: number | null = null;
    export let minSecondSize: number | null = null;
    export let maxSecondSize: number | null = null;

    let container: HTMLDivElement;
    let isResizing = false;

    
    // the width or height of the element with default size specified
    let specifiedSize: number = defaultSecondSize || defaultFirstSize;
    let nonSpecifiedSize: string = '0';
    $: nonSpecifiedSize =  `calc(100% - ${specifiedSize + 2}px)`;
    let specifiedSizeIs = defaultSecondSize ? 'second' : 'first';
    let sizeProp = direction === 'horizontal' ? 'width' : 'height';

    const resizeEditor = (event: MouseEvent) => {
        if (direction === 'horizontal') {
            const newFirstSize = event.clientX - container.getBoundingClientRect().left;
            const newSecondSize = container.getBoundingClientRect().width - newFirstSize;

            const isMinFirstSizeValid = !minFirstSize || newFirstSize >= minFirstSize;
            const isMinSecondSizeValid = !minSecondSize || newSecondSize >= minSecondSize;
            const isMaxFirstSizeValid = !maxFirstSize || newFirstSize <= maxFirstSize;
            const isMaxSecondSizeValid = !maxSecondSize || newSecondSize <= maxSecondSize;

            if (isMinFirstSizeValid && isMinSecondSizeValid && isMaxFirstSizeValid && isMaxSecondSizeValid) {
                if (specifiedSizeIs === 'first') {
                    specifiedSize = newFirstSize;
                } else {
                    specifiedSize = newSecondSize;
                }
            }
        } else {
            const newFirstSize = event.clientY - container.getBoundingClientRect().top;
            const newSecondSize = container.getBoundingClientRect().height - newFirstSize;

            const isMinFirstSizeValid = !minFirstSize || newFirstSize >= minFirstSize;
            const isMinSecondSizeValid = !minSecondSize || newSecondSize >= minSecondSize;
            const isMaxFirstSizeValid = !maxFirstSize || newFirstSize <= maxFirstSize;
            const isMaxSecondSizeValid = !maxSecondSize || newSecondSize <= maxSecondSize;

            if (isMinFirstSizeValid && isMinSecondSizeValid && isMaxFirstSizeValid && isMaxSecondSizeValid) {
                if (specifiedSizeIs === 'first') {
                    specifiedSize = newFirstSize;
                } else {
                    specifiedSize = newSecondSize;
                }
            }
        }
    }

    onMount(() => {
        window.addEventListener('mouseup', () => {isResizing = false;});
        window.addEventListener('dragstart', () => {isResizing = false;});
    });

</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="main-section {direction}"
    bind:this={container}
    on:mousemove={(event) => {
        if (isResizing) {
            resizeEditor(event);
        }
    }}>
    <div class="child child-one" style={
        `${sizeProp}: ${specifiedSizeIs === 'first' ? `${specifiedSize}px` : nonSpecifiedSize};`}>
        <slot name="1"></slot>
    </div>
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="resize-slider {isResizing ? 'active' : ''}"
        style={`
            width: 100%;
            height: 100%;
            ${sizeProp}: 2px !important;
        `}>
        <div class="resize-hover"
            on:mousedown={() => {isResizing = true;}}
            style={`
                width: 100%;
                height: 100%;
                cursor: ${direction === 'horizontal' ? 'ew-resize' : 'ns-resize'};
                position: absolute;
                ${direction === 'horizontal' ? 'left' : 'top'}: -5px;
                ${sizeProp}: 12px !important;
            `}>

        </div>
    </div>
    <div class="child child-two" style={
        `${sizeProp}: ${specifiedSizeIs === 'second' ? `${specifiedSize}px` : nonSpecifiedSize};`}>
        <slot name="2"></slot>
    </div>
</div>

<style>
    .child {
        overflow: hidden;
    }
    .main-section {
        display: flex;
        flex-direction: row;
        height: 100%;
        width: 100%;
        position: relative;
    }
    .main-section.vertical {
        flex-direction: column;
    }
    .resize-slider {
        position: relative;
        background-color: var(--main-grey-color-2);
        border: none !important;
        transition: .5s;
    }
    .resize-slider.active {
        background-color: var(--main-dark-color);
    }
    .resize-hover {
        background-color: transparent;
    }
</style>