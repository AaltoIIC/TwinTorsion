<script lang="ts">
    import Button from "$lib/Button.svelte";

    export let name: string;
    export let icon: string;
    export let texts: string[];
    export let links: string[];

</script>
<div class="resource-tile">
    <h4>{name}</h4>
    <p>
        <slot></slot>
    </p>
    <span class="icon">
        {@html icon}
    </span>
    <div class="links-cont">
        {#each texts as text, i}
            <span class="link">
                <Button
                    color="rgba(0, 0, 0, 0.03)"
                    textColor="rgba(0, 0, 0, 0.7)"
                    onClick={() => {window.open(links[i], '_blank')}}>
                    {text}
                    <svg class="icon-arrow" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                    </svg>                      
                </Button>
            </span>
        {/each}
    </div>
</div>
<style>
    .icon-arrow {
        width: 18px;
        height: 18px;
        margin: 0 -2px -4.5px 0;
    }
    .links-cont {
        position: absolute;
        bottom: 24px;
        right: 24px;
    }
    .link {
        display: block;
        width: 100%;
        text-align: right;
        padding-top: 4px;
    }
    .icon {
        position: absolute;
        bottom: -45px;
        left: -35px;
        width: 128px;
        height: 128px;
        color: var(--main-color);
    }
    .resource-tile {
        padding: 20px;
        box-sizing: border-box;
        border: var(--main-border);
        border-radius: var(--main-border-radius);
        margin: 0 0 15px 15px;
        overflow: hidden;
        height: 220px;
        position: relative;
        background: linear-gradient(rgba(0,0,0,0) 47%, var(--main-color-tr-2) 100%);
        flex: 1 1 228px;
    }
    .resource-tile:hover {
        background-color: var(--main-hover-color);
    }
    p {
        font-size: 14px;
        color: rgba(0, 0, 0, 0.6);
    }
    h4, p {
        margin: 4px;
    }
</style>