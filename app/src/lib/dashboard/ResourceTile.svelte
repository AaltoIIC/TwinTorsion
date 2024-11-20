<script lang="ts">
    import { goto } from '$app/navigation';
    import Link from '$lib/Link.svelte';

    export let name: string;
    export let icon: string;

    export let texts: string[];
    export let links: string[];
</script>
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
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
                <Link text={text} url={links[i]} />
            </span>
        {/each}
    </div>
</div>

<style>
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
        background: linear-gradient(rgba(0,0,0,0) 60%, var(--main-color-tr-2) 100%);
        cursor: pointer;
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
    .inactive {
        cursor: default;
    }
</style>