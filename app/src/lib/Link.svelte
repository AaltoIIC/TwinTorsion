<script>
    export let text;
    export let url;
    export let newPage = true;
</script>
<a class="link" href={url} target="{newPage ? '_blank' : '_self'}">
    {text}
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
    </svg>                      
</a>

<style>
    .link {
        font-size: 12px;
        color: rgba(0, 0, 0, 0.6);
        text-decoration: none;
        background-color: rgba(0, 0, 0, 0.04);
        border-radius: 50px;
        padding: 1px 6px;
        transition: .2s;
    }
    .link:hover {
        background-color: var(--main-grey-color-2);
    }
    .link svg {
        width: 12px;
        height: 12px;
        margin-bottom: -2px;
        
    }
</style>