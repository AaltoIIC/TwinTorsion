<script lang="ts">
    import Popup from "$lib/Popup.svelte";
    import type { SvelteComponent } from "svelte";
    import ElementsList from "$lib/sidebar/ElementsList.svelte";
    import { currentComponentJSON } from "$lib/stores/stores";

    let popup: SvelteComponent;
    export const open = () => {
        if (popup && popup.open) popup.open();
    }
    export const close = () => {
        if (popup && popup.close) popup.close();
    }

    currentComponentJSON.subscribe((value) => {
        if (value) {
            close();
        }
    });

</script>
<Popup bind:this={popup}
    maxHeight={2000}
    maxWidth={2000}
    padding="12px 0 0 0">
    <div class="elem-list-cont">
        <ElementsList mobile={true} />
    </div>
</Popup>
<style>
    .elem-list-cont {
        width: calc(90vw - 74px);
        min-width: 275px;
        height: fit-content;
    }
</style>