<script lang="ts">
    import type { SvelteComponent } from "svelte";
    import Button from "./Button.svelte";
    import Popup from "./Popup.svelte";

    let popup: SvelteComponent;
    let dialogText = "";
    let confirmText = "";
    let denyText = "";  
    let resolvePromise: (value: boolean) => void;

    export const openDialog = (dialog: string, confirm: string, deny: string): Promise<boolean> => {
        dialogText = dialog;
        confirmText = confirm;
        denyText = deny;
        if (popup) {
            popup.open();
        }
        return new Promise((resolve) => {
            resolvePromise = resolve;
        });
    }

    const handleConfirm = () => {
        if (popup) {
            popup.close();
        }
        if (resolvePromise) {
            resolvePromise(true);
        }
    };

    const handleDeny = () => {
        if (popup) {
            popup.close();
        }
        if (resolvePromise) {
            resolvePromise(false);
        }
    };

</script>
<Popup bind:this={popup} maxWidth={400}>      
    <p>{dialogText}</p>
    <div class="btn-cont">
        <Button 
            onClick={handleConfirm}
            color="var(--main-dark-color)">
            <svg class="option-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
            </svg>                                        
            {confirmText}
        </Button>
        <Button 
            onClick={handleDeny}
            color="var(--main-dark-color)">
            <svg class="option-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>                      
            {denyText}
        </Button>
    </div>
</Popup>
<style>
    .option-icon {
        width: 18px;
        height: 18px;
        margin: 0 0 -4px 0;
        stroke: rgba(255, 255, 255, 0.9);
        stroke-width: 2px;
        stroke-linejoin: round;
        margin-top: -2px;
    }
    .btn-cont {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 16px;
    }
    p {
        font-size: 14px;
        font-weight: 450;
        margin: 0;
        color: rgb(0, 0, 0, 0.7);
        text-align: center;
    }
</style>