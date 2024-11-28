<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { twinbaseUrl } from "../../config";
    import { twinbases } from "$lib/stores/stores";
    import { onMount } from 'svelte';

    interface optionType {
        id: string;
        name: string;
        checked: boolean;
    }

    const getBaseName = (url: string) => {
        try {
            let org = url.split('/')[2].split('.')[0];
            let repo = url.split('/')[3];
            return `${org}/${repo}`;
        } catch {
            return url;
        }
    }

    let options: optionType[] = [
        {
            id: 'custom components',
            name: 'custom components',
            checked: true
        },
        {
            id: twinbaseUrl,
            name: getBaseName(twinbaseUrl),
            checked: true
        }
    ]
    $twinbases.forEach((url) => {
        options.push({
            id: url,
            name: getBaseName(url),
            checked: true
        })
    })
    let checkedOptions: string[] = options.map(option => option.id);
    let isOpen = false;
    const dispatch = createEventDispatcher();

    const handleClick = (id: string) => {
        const option = options.find(option => option.id === id);
        if (option) {
            if (option.checked) {
                // don't let user uncheck all options
                if (checkedOptions.length === 1) return;
                
                option.checked = false;
                checkedOptions = checkedOptions.filter(option => option !== id);
            } else {
                option.checked = true;
                checkedOptions = [...checkedOptions, option.id];
            }
            options = options;
        }
    }
    
    $: dispatch('update', checkedOptions);

    let filterText = 'all components';
    $: if (checkedOptions.length === 1) {
        filterText = options.find(option => option.checked === true)?.name || '';
    } else if (checkedOptions.length === options.length) {
        filterText = 'all components';
    } else {
        filterText = `${checkedOptions.length} sources`;
    }

    let onHover = false;
    onMount(() => {
        document.addEventListener('pointerdown', (e) => {
            if (isOpen && !onHover) {
                isOpen = false;
            }
        })
        document.addEventListener('wheel', (e) => {
            if (isOpen && !onHover) {
                isOpen = false;
            }
        })

        dispatch('update', checkedOptions);
    })
</script>
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="filters {isOpen ? "open": ""}"
    on:mouseenter={() => {onHover = true}}
    on:mouseleave={() => {onHover = false}}>
    <div class="filter-head"
        on:click={() => {isOpen = !isOpen}}>
        <p>Showing <span class="filter-selection">{filterText}</span></p>
        <button class="filter-btn hidden-btn">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
            </svg>              
        </button>
    </div>
    <div class="filter-layover" style={`--nof-entries: ${options.length};`}>
        <div class="filter-option-list">
            {#each options as {id, name, checked}}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div class="filter-entry" on:click={() => handleClick(id)}>
                    <input type="checkbox" bind:checked={checked} />
                    <p>{name}</p>
                </div>
            {/each}
        </div>
        <button class="done-btn" on:click={() => {isOpen = false}}>           
            Done
        </button>
    </div>
</div>
<style>
    .done-btn {
        width: calc(100% - 10px);
        padding: 8px;
        background-color: var(--main-dark-color);
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        margin: 5px;
        border: none;
        border-top: var(--main-border);
        cursor: pointer;
        border-bottom: solid 2px rgba(0, 0, 0, 0.3);
        border-radius: 50px;
    }

    input[type="checkbox"]:checked {
        background-size: cover;
        padding: 2px;
    }

    input[type="checkbox"]:not(:disabled):checked {
        border-color: var(--main-dark-color);
        background-color: var(--main-dark-color);
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="rgba(255, 255, 255, 0.9)"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" /></svg>');
    }
    input[type="checkbox"] {
        box-sizing: border-box;
        width: 14px;
        height: 14px;
        margin: 6px;
        padding: 0;
        border: solid 2px rgba(0, 0, 0, 0.12);
        border-radius: 2px;
        appearance: none;
        background-color: transparent;
        outline: none;
        transition: outline 0.1s;
        pointer-events: none;
    }
    .filter-entry input {
        margin-right: 10px;
        flex-shrink: 0;
    }
    .filter-entry {
        display: flex;
        align-items: center;
        padding: 5px 10px;
        cursor: pointer;
    }
    .filter-entry p {
        flex-shrink: 1;
        flex-grow: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .filter-option-list {
        height: fit-content;
        max-height: 300px;
        margin-top: 5px;
        overflow-y: scroll;
    }
    
    .filter-layover {
        position: absolute;
        top: calc(100% + 5px);
        left: 5px;
        height: 0;
        overflow: hidden;
        background-color: rgb(252, 252, 252);
        z-index: 10;
        transition: height .3s;
        width: calc(100% - 18px);
        border-radius: var(--main-border-radius);
    }
    .open .filter-layover {
        border: var(--main-border);
        height: min( calc(var(--nof-entries) * 36px + 50px), 350px);
    }
    .filter-btn svg {
        width: 16px;
        height: 16px;
        color: rgba(0, 0, 0, 0.8);
        margin: 0 0 -4px -8px;
    }
    .open .filter-btn svg {
        transform: rotate(180deg);
    }

    .filter-selection {
        font-weight: 550;
        color: var(--main-dark-color);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .filter-head {
        cursor: pointer;
        padding: 10px 10px;
        border-top: var(--main-border);
        background-color: var(--main-grey-color);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .filter-head p {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex-grow: 1;
        flex-shrink: 1;
    }
    .filter-selection {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis; 
    }
    .filter-btn {
        flex-grow: 0;
        flex-shrink: 0;
    }

    .filters {
        position: relative;
    }
    .filters p {
        margin: 0;
        font-size: 14px;
        color: rgba(0, 0, 0, 0.8);
    }

    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        cursor: pointer;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 0, 0, 0.15);
    }
</style>