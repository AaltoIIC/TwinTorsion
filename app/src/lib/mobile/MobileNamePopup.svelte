<script lang="ts">
    import Popup from "$lib/Popup.svelte";
    import Button from "$lib/Button.svelte";
    import type { SvelteComponent } from "svelte";

    export let text: string;
    export let value: string | undefined;
    export let isError: boolean = false;
    export let onInput: (text: string) => void;

    let popup: SvelteComponent;

    export const open = () => {
        if (popup) popup.open();
    }
    export const close = () => {
        if (popup) popup.close();
    }

</script>
<Popup bind:this={popup}>
    <div class="main-mobile-name">
        <h4>{text}:</h4>
        <input
            bind:value={value}
            type="text"
            on:input={() => {onInput(value || '');}}
            style={`${isError ? "outline: solid 2px var(--main-error-color-dark);" : ""}`}
        />
        <div class="btn-cont">
            <Button
                onClick={close}
                color="var(--main-dark-color)">
                Done
            </Button>
        </div>
    </div>
</Popup>
<style>
    .btn-cont {
        width: 100%;
        display: flex;
        justify-content: flex-end;
    }
    .main-mobile-name {
        width: calc(90vw - 74px);
    }
    .main-mobile-name input {
        width: calc(100% - 16px);
        padding: 8px;
        margin: 8px 0;
        border-radius: 5px;
        border: var(--main-border);
        font-family: 'Inter', sans-serif;
    }
     h4 {
        margin: 0;
     }
</style>