<script lang="ts">
    import { onMount } from 'svelte';
    import Portal from "svelte-portal";
    import type { ElementType, ExcitationType } from '$lib/types/types';
    import { isExcitationType } from '$lib/types/typeguards';
    import { editElement } from '../componentHelpers';
    import { paramUnits, paramTypes } from '../params';
    import { currentComponentJSON, highlightLinesInEditor } from '../../../stores/stores';
    import { nthLinesInJSON } from '$lib/utils';
    import LayoverProperty from './LayoverProperty.svelte';
    
    export let params: ElementType;
    export let possibleParams: {required: string[], optional: string[]};

    // handle deletion
    const deleteElement = () => {
        isOpen = false;
        isEditing = false;
        currentComponentJSON.update(value => {
            let newVal = {...value};
            newVal.json.elements = value.json.elements.filter((el: any) => el.name !== params.name)
            return newVal;
        })
    }

    // handle parameter change
    $: undefinedParams = possibleParams.optional
        .filter(item => !(item in params))
        .reduce((acc, key) => {
            acc[key] = undefined;
            return acc;
        }, {} as { [key: string]: undefined });

    let allProperties: ElementType;
    $: allProperties = {...params, ...undefinedParams};
    const handleParamChange = (key: string, value: any) => {
        const isValidNumber = /^-?\d+(\.\d+)?([eE][+-]?\d+)?$/.test(value);
        
        // try to convert to list if it's a list
        const isObjectStr = typeof value === 'string' && value.startsWith("{") && value.endsWith("}");
        try {
            let parsedValue = isObjectStr ? JSON.parse(value) : value;
            if (isExcitationType(parsedValue)) {
                value = parsedValue as ExcitationType;
            }
        } catch (e) {}

        allProperties = {...allProperties, [key]: isValidNumber ? Number(value) : value};
    }

    // handle element name change
    let isNameError = false;
    let nameField: HTMLInputElement;
    const handleNameChange = (event: any) => {
        // remove illegal characters
        const illegalChars = /['"\n]/g;
        if (illegalChars.test(event.target.value)) {
            event.target.value = event.target.value.replace(illegalChars, '');
        }

        // check if the name is already taken or empty
        const nameExists = $currentComponentJSON.json.elements.some((el: any) => el.name !== params.name && el.name === event.target.value);
        if (nameExists || event.target.value === '') {
            isNameError = true;

        } else {
            isNameError = false;
        }

        allProperties.name = event.target.value;

        // set width of the input field
        setNameFieldWidth();
    }

    const setNameFieldWidth = () => {
        const span = nameField.nextElementSibling as HTMLSpanElement;
        span.textContent = allProperties.name;
        nameField.style.width = `${span.offsetWidth}px`;
    }

    // handle layover behavior (position, visibility, etc.)
    let onHover = false;
    let isOpen = false;
    let isEditing = false;
    let x = 0;
    let y = 0;
    export const show = (parentX: number, parentY: number) => {
        x = parentX;
        y = parentY;

        isEditing = true;
        setTimeout(() => {
            setNameFieldWidth();
        }, 0);
    }
    export let nodeOnHover = false;
    $: isOpen = (x !== 0) && (isEditing || nodeOnHover || onHover);

    export const nodeClick = () => {
        isEditing = true;
        setNameFieldWidth();
        
        // highligt JSON corresponding to the element in the JSON editor
        if (highlightLinesInEditor) {
            let [startIndex, endIndex] = nthLinesInJSON($currentComponentJSON.json, 'elements', 'name', params.name);
            $highlightLinesInEditor(startIndex, endIndex);
        }
    }

    const handleMouseMove = (event: any) => {
        if (isEditing) return;
        x = event.clientX;
        y = event.clientY;
    };

    // update transform based on the position of the layover
    const transform = ['0', '0'];
    $: if (x > window.innerWidth/2) {
        transform[0] = 'calc(-100% - 15px)';
    } else {
        transform[0] = '15px';
    }
    $: if (y > window.innerHeight/2) {
        transform[1] = 'calc(-100% - 15px)';
    } else {
        transform[1] = '15px';
    }

    const closeLayover = () => {
        if (isEditing) {
            // if name is invalid, revert to the original name
            if (isNameError) {
                allProperties.name = params.name;
                nameField.value = params.name;
                isNameError = false;
            }

            // update the element with the new properties
            if (isEditing) {
                currentComponentJSON.update(value => {
                let newVal = {...value};

                // go throguh allProperties and change empty strings to 0 for number type parameters
                Object.entries(allProperties).forEach(([key, value]) => {
                    if (paramTypes[key] === 'number' && value === '') {
                        (allProperties as any)[key] = 0;
                    }
                });

                newVal.json.elements =  editElement(value.json.elements, params.name, allProperties, true);
                return newVal;
                })
            }
        }

        isOpen = false;
        isEditing = false;
        $highlightLinesInEditor(-1, -1);
    }
    
    const handleClickOutside = (event: any) => {
        if (onHover || nodeOnHover) return;
        closeLayover();
    };

    const handleKeydown = (event: any) => {
        if (event.key === 'Escape') {
            closeLayover();
        }
    };

    onMount(() => {
        window.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('pointerdown', handleClickOutside);
        document.addEventListener('dragstart', closeLayover);
        document.addEventListener('keydown', handleKeydown);

        const flowEditor = document.querySelector('.svelte-flow__pane');
        if (flowEditor) {
            flowEditor.addEventListener('wheel', closeLayover);
        }

        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('pointerdown', handleClickOutside);
            document.removeEventListener('dragstart', closeLayover);
            document.removeEventListener('keydown', handleKeydown);
            flowEditor?.removeEventListener('wheel', closeLayover);
        };
    });

</script>
<Portal target="body">
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="main-layover-cont {isOpen ? 'active' : ''}"
        style={`top: ${y}px;
                left: ${x}px;
                border: ${isEditing ? 'solid 1px var(--main-color)' : 'solid 1px rgba(0, 0, 0, 0.06)'};
                transform: translate(${transform[0]},${transform[1]});
            `}
        on:mouseenter={() => {onHover = true}}
        on:mouseleave={() => {onHover = false}}>
        <div class="name-cont {isEditing ? 'editing' : ''}">
            <input
                type="text"
                name="element-name"
                value={allProperties.name}
                on:input={handleNameChange}
                bind:this={nameField}
                class="main-name-field {(isNameError ? "name-error" : "")}"
            />
            <span class="hidden-span"></span>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <svg
                on:click={deleteElement}
                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>              
        </div>
        <span class="name-error-info {(isNameError ? "active" : "")}">
            Name has to be unique and non-empty.  
        </span>
        <div class="params-cont">
            {#each Object.entries(allProperties) as [paramName, paramValue]}
                {#if paramName != 'name'}
                    <LayoverProperty
                        paramName={paramName}
                        paramValue={paramValue}
                        paramUnit={paramUnits[paramName]}
                        isEditing={isEditing}
                        required={possibleParams.required.includes(paramName)}
                        onChange={handleParamChange}
                    />
                {/if}
            {/each}
        </div>
        <button class="close-btn"
            on:click={() => {closeLayover()}}
            style="display: {isEditing ? 'block' : 'none'};">
            Done
        </button>
    </div>
</Portal>
<style>
    .hidden-span {
        visibility: hidden;
        white-space: pre;
        position: absolute;
        font-size: 13.5px;
        font-family: 'Inter', sans-serif;  
        font-weight: 550;
        padding: 1px;
        width: fit-content;
    }
    .name-cont.editing svg {
        display: block;
    }
    .name-cont svg {
        cursor: pointer;
        width: 14px;
        height: 14px;
        padding: 4px;
        border-radius: 50px;
        background-color: rgba(0, 0, 0, 0.1);
        border: solid 1px rgba(255, 255, 255, 0.2);
        color: rgba(0, 0, 0, 0.4);
        display: none;
    }
    .name-cont svg:hover {
        background-color:  rgb(240, 100, 100);
        color: rgba(255, 255, 255, 0.9)
    }
    .name-error-info {
        width: 100%;
        font-size: 10px;
        line-height: 1;
        display: none;
        padding: 0 12px 6px 12px;
        font-weight: 450;
        color: var(--main-error-color);
    }
    .name-error-info.active {
        display: block;
    }
    .main-name-field {
        padding: 1px;
        outline: none;
        border: none;
        min-width: 16px;
        font-family: 'Inter', sans-serif;
        font-weight: 550;
        max-width: 16ch;
        width: 16ch; 
    }
    .name-cont.editing .main-name-field {
        border-bottom: solid 2px rgba(0, 0, 0, 0.1);
    }
    .name-error {
        border-bottom: solid 2px var(--main-error-color) !important;
    }
    .close-btn {
        width: 100%;
        padding: 8px;
        background-color: var(--main-color);
        color: white;
        border: none;
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        cursor: pointer;
        border-radius: 0 0 var(--main-border-radius) var(--main-border-radius);
    }
    .close-btn:hover {
        filter: brightness(1.05);
    }
    .params-cont {
        display: flex;
        flex-direction: column;
        padding: 4px 2px 4px 2px;
        border-top: solid 1px rgba(0, 0, 0, 0.06);
    }
    .name-cont {
        padding: 8px 12px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
    }
    .main-layover-cont {
        display: none;
        position: absolute;
        width: 268px;
        height: fit-content;
        background-color: rgba(255, 255, 255, 1);
        border: solid 1px rgba(0, 0, 0, 0.06);
        z-index: 1000000;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: rgba(0, 0, 0, 0.9);
        border-radius: var(--main-border-radius);
    }
    .main-layover-cont.active {
        display: block;
    }

    @media (max-width: 1048px) {
        .main-layover-cont {
            display: none !important;
        }
    }
</style>