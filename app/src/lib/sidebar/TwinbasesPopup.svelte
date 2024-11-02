<script lang="ts">
    import Popup from "$lib/Popup.svelte";
    import { twinbaseUrl } from "../../config";
    import {
        twinbases,
        notification
    } from "$lib/stores/stores";
    import {
        trimText,
        isTwinbaseUrl
    } from "$lib/utils";
    import type { SvelteComponent } from "svelte";

    let popup: SvelteComponent;
    export const open = () => {
        if (popup) {
            popup.open();
        }
    }

    let isAddingNew = false;
    let isInputFormatValid = false;
    let verifyingUrl = false;
    let isVerificationFailed = false;
    let currentNewUrl = '';

    const validateNewUrlForm = (e: Event) => {
        if (!(e.target as HTMLInputElement).checkValidity() ||
            currentNewUrl === '' ||
            $twinbases.includes(currentNewUrl) ||
            currentNewUrl === twinbaseUrl) {
            isInputFormatValid = false;
        } else {
            isInputFormatValid = true;
        }
    }

    const addNew = () => {
        if (verifyingUrl) return;
        verifyingUrl = true;
        isTwinbaseUrl(currentNewUrl).then((isValid) => {
            if (isValid) {
                twinbases.update((twinbases) => {
                    twinbases.push(currentNewUrl);
                    return twinbases;
                });
                notification.set({
                    message: "Twinbase added.",
                    type: "success",
                    duration: 3000
                });
                isAddingNew = false;
            } else {
                notification.set({
                    message: "Invalid twinbase url.",
                    type: "error",
                    duration: 3000
                });
                isVerificationFailed = true;
            }
            currentNewUrl = '';
            verifyingUrl = false;
            isInputFormatValid = false;
        });
    }

    const handleDelete = (url: string) => {
        twinbases.update((twinbases) => {
            twinbases = twinbases.filter((twinbaseUrl) => twinbaseUrl !== url);
            return twinbases;
        });
    }
</script>
<Popup
    bind:this={popup}
    maxWidth={500}
    maxHeight={500}>
    <h4>Twinbases:</h4>
    <div class="twinbases-list-cont">
        <div class="twinbase">
            <p>{trimText(twinbaseUrl, 60)}</p>
            <span class="default-txt">
                Default
            </span>
        </div>
        {#each $twinbases as twinbaseUrl}
            <div class="twinbase">
                <p>{trimText(twinbaseUrl, 60)}</p>
                <button class="btn-delete"
                    on:click={() => handleDelete(twinbaseUrl)}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                    </svg>    
                </button>                  
            </div>
        {/each}
    </div>
    {#if !isAddingNew}
        <button class="add-twinbase-btn" on:click={() => {isAddingNew = true;}}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>                
        </button>
    {:else}
        <div class={`add-new
            ${isAddingNew ? "active" : "inactive"}
            ${verifyingUrl ? "verifying" : ""}}`}>
            <input
                type="url"
                bind:value={currentNewUrl}
                on:input={validateNewUrlForm}
                disabled={verifyingUrl}
                placeholder="Add twinbase url..." />
            {#if verifyingUrl}
                <span class="verify-cont">
                    <svg class="icon-verify" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50" width="50" height="50">
                        <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="3.5" stroke-linecap="round" stroke="currentColor" stroke-dasharray="42, 126" />
                    </svg>
                </span>
            {:else}
                <span class="btn-cont">
                    <button
                        class="btn-check {isInputFormatValid ? "active" : "inactive"}"
                        on:click={addNew}>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                        </svg>  
                    </button>
                    <button class="btn-cancel" on:click={() => {isAddingNew = false; currentNewUrl = '';}}>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                        </svg>                                               
                    </button>   
                </span>
            {/if}       
        </div>
    {/if}
</Popup>
<style>
    .btn-delete {
        background-color: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
        margin: 0 20px 0 0;
    }
    .btn-delete svg {
        width: 16px;
        width: 16px;
        color: rgba(0, 0, 0, 0.3);
    }
    .btn-delete svg:hover {
        color: rgba(0, 0, 0, 0.5);
    }
    .verify-cont {
        position: relative;
        margin-right: 20px;
        width: 18px;
        height: 18px;
    }
    .icon-verify {
        width: 18px;
        height: 18px;
        color: rgba(0, 0, 0, 0.3);
        transform-origin: center;
        animation: rotate 0.4s linear infinite;
        position: absolute;
    }
    @keyframes rotate {
      100% {
        transform: rotate(360deg);
      }
    }
    .add-new {
        border-bottom: none !important;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .btn-cont {
        padding: 2px 4px;
        margin: 0 14px;
        border: var(--main-border);
        border-radius: var(--main-border-radius);
    }
    .btn-check, .btn-cancel {
        background-color: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
    }
    .add-new input {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: rgba(0, 0, 0, 0.6);
        margin: 14px 0;
        border: none;
        width: 400px;
        background-color: transparent;
    }
    .add-new input:focus {
        outline: none;
    }
    .btn-check svg, .btn-cancel svg {
        width: 16px;
        height: 16px;
        color: rgba(0, 0, 0, 0.5);
        margin-bottom: -2px;
    }
    .btn-check.inactive {
        pointer-events: none;
    }
    .btn-check.inactive svg {
        color: rgba(0, 0, 0, 0.2);
    }
    .btn-check svg:hover, .btn-cancel svg:hover {
        color: rgba(0, 0, 0, 0.6);
    }

    h4 {
        font-weight: 550;
        margin: 0 0 10px 0;
    }
    .add-twinbase-btn {
        width: 34px;
        height: 34px;
        border: none;
        background-color: var(--main-dark-color);
        border-radius: 50px;
        float: right;
        margin: 12px 8px 0 0;
        cursor: pointer;
    }
    .add-twinbase-btn svg {
        color: rgba(255, 255, 255, 0.9);
        width: 18px;
        height: 18px;
        margin-bottom: -3px;
    }
    .twinbase {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: var(--main-border);
    }
    .twinbase:hover {
        background-color: var(--main-hover-color);
    }
    .twinbase p {
        font-size: 14px;
    }
    .default-txt {
        color: rgba(255, 255, 255, 0.9);
        font-size: 12px;
        background-color: var(--main-color);
        padding: 2px 6px;
        border-radius: 50px;
        font-weight: 400;
        margin-right: 4px;
    }
    .twinbases-list-cont {
        width: 500px;
        height: fit-content;
        max-height: 400px;
        overflow-y: scroll;
    }
</style>