<script lang="ts">
    import Popup from "$lib/Popup.svelte";
    import type { SvelteComponent } from "svelte";
    import ComponentsList from "$lib/sidebar/ComponentsList.svelte";
    import { currentSystemJSON } from "$lib/stores/stores";

    let popup: SvelteComponent;
    export const open = () => {
        if (popup && popup.open) popup.open();
    }
    export const close = () => {
        if (popup && popup.close) popup.close();
    }

    currentSystemJSON.subscribe((value) => {
        if (value) {
            close();
        }
    });

</script>
<Popup bind:this={popup}
    maxHeight={2000}
    maxWidth={2000}
    padding="26px 0 0 0">
    <div class="comp-list-cont">
        <ComponentsList />
    </div>
</Popup>
<style>
    .comp-list-cont {
        width: calc(90vw);
        height: 70vh;
    }
</style>