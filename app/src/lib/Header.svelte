<script>
    import { version } from '$app/environment'
    import { goto } from '$app/navigation';
    import DropdownMenu from './DropdownMenu.svelte';

    export let noTap = false;

    const menuItems = [
        {
            name: 'User Guide',
            link: 'https://github.com/AaltoIIC/TwinTorsion/wiki/User-Guide'
        },
        {
            name: 'GitHub',
            link: 'https://github.com/AaltoIIC/TwinTorsion'
        },
        {
            name: 'Aalto IIC',
            link: 'https://www.aalto.fi/en/aiic'
        }
    ];

</script>
<div class="main-header {noTap ? 'no-tap' : ''}">
    <a href="/" class="logo-cont">
        <img class="main-logo" src="./../icon.svg" alt="TwinTorsion Editor Logo">
        TwinTorsion Editor <sub>{version}</sub>
    </a>
    <p class="links-desktop">
        {#each menuItems as item}
            <a href={item.link}>
                {item.name}
            </a>
        {/each}
    </p>
    <div class="links-mobile">
        <DropdownMenu
            options={menuItems.map(item => item.name)}
            onClick={(option) => {
                const item = menuItems.find(item => item.name === option);
                if (item) {
                    goto(item.link);
                }
            }}
        />
    </div>
</div>
<style>
    .main-header {
        border-radius: var(--main-border-radius);
        background: white;
        position: fixed;
        top:10px;
        left: calc(50vw - 550px);
        width: 1100px;
        height: 68px;
        border: var(--main-border);
        z-index: 10000;
        display: flex;
        justify-content: space-between;
    }
    .main-header.no-tap {
        pointer-events: none;
    }
    .main-logo {
        width: 36px;
        height: 36px;
        display: block;
        margin-right: 10px;
    }
    .logo-cont {
        display: flex;
        align-items: center;
        height: 100%;
        margin: 0 24px;
        text-decoration: none;
        font-weight: 550;
    }
    .logo-cont sub {
        font-size: 10px;
        position: relative;
        top: -3.5px;
        left: 3px;
        color: rgba(0, 0, 0, 0.6);
    }
    .links-desktop {
        display: flex;
        gap: 20px;
        margin: 0 24px;
        align-items: center;
    }
    .links-desktop a {
        text-decoration: none;
        font-size: 14px;
    }
    .links-mobile {
        display: none;
    }

    @media (max-width: 1100px) {
        .main-header {
            width: calc(100% - 20px);
            left: 10px;
        }
        .links-desktop {
            display: none;
        }
        .links-mobile {
            display: block;
            height: 100%;
            display: flex;
            align-items: center;
            margin-right: 12px;
        }
    }
</style>