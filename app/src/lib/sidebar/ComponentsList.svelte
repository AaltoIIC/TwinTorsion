<script lang="ts">
    import type { ComponentType } from "$lib/types/types";
    import DropdownButton from "$lib/DropdownButton.svelte";
    import ComponentListItem from "$lib/sidebar/CompontentListItem.svelte";
    import { 
        customComponents,
        currentSystemJSON,
        twinbases
    } from "$lib/stores/stores";
    import { importComponent } from "$lib/utils";
    import { goto } from "$app/navigation";
    import { twinbaseUrl } from "../../config";
    import { 
        fetchComponents,
        trimText
     } from "$lib/utils";
    import TwinbasesPopup from "./TwinbasesPopup.svelte";
    import type { SvelteComponent } from "svelte";

    let componentInput: HTMLInputElement;
    let twinbasesPopup: SvelteComponent;

    let shownComponents =  Array.from($customComponents.entries())
                                .filter(([key, val]) => key.startsWith(`${$currentSystemJSON.id}-`))
                                .reverse() as [string, ComponentType][]
    customComponents.subscribe(value => {
        shownComponents = Array.from(value.entries())
            .filter(([key, val]) => key.startsWith(`${$currentSystemJSON.id}-`))
            .reverse() as [string, ComponentType][]
    })

    const handleNewComponent = (option: string) => {
        if (option === 'Create New') {
            goto('/component-editor');
        } else if (option === 'Import New') {
            componentInput.click();
        }
    }

    const twinbaseNames = [twinbaseUrl, ...$twinbases].map((url) => {
        try {
            let org = url.split('/')[2].split('.')[0];
            let repo = url.split('/')[3];
            return trimText(`${org}/${repo}`,40);
        } catch {
            return trimText(url, 22);
        }
    });
    let digitalTwins: any[] = [];
    $twinbases.forEach((url) => {
        fetchComponents(url).then((components) => {
            digitalTwins = digitalTwins.concat(components);
        })
    })
    fetchComponents(twinbaseUrl).then((components) => {
        digitalTwins = digitalTwins.concat(components);
    })
</script>

<div class="component-cont">
    <div class="component-upper">
        <h3>Components:</h3>
            <span class="top-btn-cont">
                <DropdownButton
                    isActive={true}
                    color='var(--main-grey-color-2)'
                    textColor='dark'
                    icon='<svg class="icon-create" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>'
                    options={['Create New','Import New']}
                    optionIcons={[
                        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>',
                        '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" /></svg>'
                    ]}
                    onClick={handleNewComponent}>
                    Add
                </DropdownButton>
                <input type="file" class="hidden"
                    name="component-file"
                    bind:this={componentInput}
                    on:change={importComponent}
                    accept=".json">
                
                <button class="twinbases-button"
                    on:click={() => {if (twinbasesPopup) {twinbasesPopup.open()}}}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                    </svg>  
                </button>
            </span>           
    </div>
    <div class="filters">
        <p>Showing <span class="filter-selection">all components</span></p>
        <button class="filter-btn hidden-btn">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
            </svg>              
        </button>
        <div class="filter-url-list">
            <div class="filter-entry">
                <input type="checkbox" />
                <p>Custom Components</p>
            </div>
            {#each [...twinbaseNames] as url}
                <div class="filter-entry">
                    <input type="checkbox" />
                    <p>{url}</p>
                </div>
            {/each}
        </div>
    </div>
    <div class="component-list">
        {#each shownComponents as [id, component] (id)}
            <ComponentListItem type="custom" id={id} data={component} />
        {/each}
        {#if digitalTwins.length > 0}
            {#each digitalTwins as {id, component}}
                <ComponentListItem type="twin" id={id} data={component} />
            {/each}
        {:else}
            {#each { length: 3 } as _}
                <div class="placeholder-list-elem"></div>
            {/each}
        {/if}
    </div>
</div>
<TwinbasesPopup bind:this={twinbasesPopup} />
<style>
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
    }
    .filter-entry input {
        margin-right: 10px;
    }
    .filter-entry {
        display: flex;
        align-items: center;
        padding: 5px 10px;
        cursor: pointer;
    }
    .filter-url-list {
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background-color: white;
        border-bottom: var(--main-border);
        border-top: var(--main-border);
        box-sizing: border-box;
        z-index: 10;
    }
    .filter-btn svg {
        width: 16px;
        height: 16px;
        color: rgba(0, 0, 0, 0.8);
        margin: 0 0 -4px -8px;
    }
    .filter-selection {
        font-weight: 550;
        color: var(--main-dark-color);
    }
    .filters {
        padding: 10px 10px;
        border-top: var(--main-border);
        background-color: var(--main-grey-color);
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }
    .filters p {
        margin: 0;
        font-size: 14px;
        color: rgba(0, 0, 0, 0.8);
    }
    .placeholder-list-elem {
        width: calc(100% - 12px);
        margin: 5px;
        height: 100px;
        border: var(--main-border);
        border-radius: var(--main-border-radius);
        animation-name: placeHolderShimmer;
        animation-duration: 1s;
        animation-iteration-count: infinite;
    }
    .top-btn-cont {
        display: flex;
        gap: 6px;
    }
    .twinbases-button {
        background-color: var(--main-dark-color);
        border: none;
        margin: 0;
        padding: 6px;
        width: 34px;
        height: 34px;
        cursor: pointer;
        border-radius: 50px;
    }
    .twinbases-button svg {
        width: 16px;
        height: 16px;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: -4px;
    }
    .hidden {
        display: none;
    }
    .component-upper h3 {
        font-size: 16px;
    }
    .component-upper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 10px;
        vertical-align: middle;
        z-index: 10;
        position: relative;
    }
    .component-list {
        width: 360px;
        height: calc(100vh - 137px);
        overflow-y: scroll;
        background: white;
        border-top: var(--main-border);
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