<script lang="ts">
    import {
        assignNodeNumbers,
        addElement
    } from "../componentHelpers";
    import {
        possibleParams
    } from "../params";
    import { currentComponentJSON } from "$lib/stores/stores";
    import { onMount } from "svelte";
    import TableCell from "./TableCell.svelte";
    import { getScreenSize } from "$lib/utils";

    let elements: Record<string, any>[];
    let nodeNos: Record<string, string> = {};

    let columns: string[] = ["node", "name", "type"];
    Object.values(possibleParams).forEach(paramsObj => {
        columns.push(...paramsObj.required);
    });
    Object.values(possibleParams).forEach(paramsObj => {
        columns.push(...paramsObj.optional);
    });
    columns = [...new Set(columns)];

    const possibleParamsList: Record<string, string[]> = {};
    Object.entries(possibleParams).forEach(([key, value]) => {
        possibleParamsList[key] = [...value.required, ...value.optional];
    });

    currentComponentJSON.subscribe(value => {
        elements = value.json.elements as Record<string, any>[];
        nodeNos = assignNodeNumbers(value.json.elements);
    });


    // handle add element button
    let addElementButton: HTMLButtonElement;
    let isAddLayoverOpen = false;

    // handle pan
    let tableOuter: HTMLDivElement;
    let pointerdown = false;
    const handlePan = (e: MouseEvent) => {
        if (pointerdown) {
            tableOuter.scrollTop -= e.movementY;
            tableOuter.scrollLeft -= e.movementX;
            isAddLayoverOpen = false;
        }
    };

    // handle action buttons
    let hoveredElement: string | null = null;
    let selectedElement: string | null = null;

    const handleElementDelete = (elemName: string) => {
        currentComponentJSON.update(val => {
            val.json.elements = val.json.elements.filter(element => element.name !== elemName);
            return val;
        });
    };

    const moveUp = (elemName: string) => {
        currentComponentJSON.update(val => {
            let elements = [...val.json.elements];
            const index = elements.findIndex(element => element.name === elemName);
            if (index === 0) return val;

            const elem = elements[index];
            elements[index] = elements[index - 1];
            elements[index - 1] = elem;

            return {
                ...val,
                json: {
                    ...val.json,
                    elements
                }
            };
        });
    };

    const moveDown = (elemName: string) => {
        currentComponentJSON.update(val => {
            let elements = [...val.json.elements];
            const index = elements.findIndex(element => element.name === elemName);
            if (index === elements.length - 1) return val;

            const elem = elements[index];
            elements[index] = elements[index + 1];
            elements[index + 1] = elem;

            return {
                ...val,
                json: {
                    ...val.json,
                    elements
                }
            };
        });
    };

    // handle mobile view
    let isMobile = getScreenSize() === "mobile";
    onMount(() => {
        document.addEventListener("pointerdown", (e) => {
            pointerdown = true;
        });
        document.addEventListener("click", (e) => {
            if (e.target !== addElementButton) {
                isAddLayoverOpen = false;
            }

            if (!(e.target as HTMLElement).hasAttribute("data-mobilebtn")) {
                selectedElement = null;
            }
        });
        document.addEventListener("dragstart", (e) => {
            pointerdown = false;
        });
        document.addEventListener("pointerup", () => {
            pointerdown = false;
        });
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                isAddLayoverOpen = false;
            }
        });
    });

</script>

<div class="table-outer"
    bind:this={tableOuter}>
    <table class="main-table-editor"
        on:mouseleave={() => hoveredElement = null}
        on:pointermove={handlePan}>
        <tr on:mouseenter={() => hoveredElement = null}>
            {#each columns as column}
                <th>{column}</th>
            {/each}
        </tr>
        {#each elements as element (element.name)}
            <tr on:mouseenter={() => {if (!isMobile) hoveredElement = element.name}}
                class={(isMobile ?
                    (selectedElement === element.name ? 'selected' : '')
                    :
                    (hoveredElement === element.name ? 'selected' : '')
                )}>
                <td class="nodeNo">{nodeNos[element.name]}</td>
                <TableCell
                    editable={true}
                    element={element['name']}
                    param="name"
                />
                <TableCell
                    editable={false}
                    element={element['name']}
                    param="type"
                />
                {#each columns.slice(3) as column }
                    <TableCell
                        editable={possibleParamsList[element.type]?.includes(column)}
                        element={element['name']}
                        param={column}
                        required={possibleParams[element.type]?.required.includes(column)}
                    />
                {/each}
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div class="action-cont">
                    <div class="action-inner">
                        <button class="btn-action"
                            on:click={() => moveUp(element.name)}>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" />
                            </svg>
                        </button>
                        <button class="btn-action"
                            on:click={() => moveDown(element.name)}>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" />
                            </svg>                                                  
                        </button>
                        <button class="btn-action rm"
                            on:click={() => handleElementDelete(element.name)}>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>                      
                        </button>
                        <!-- svelte-ignore a11y-click-events-have-key-events -->
                        <!-- svelte-ignore a11y-no-static-element-interactions -->
                        <div class="mobile-select-btn"
                            data-mobilebtn="true"
                            on:click={() => {selectedElement = element.name;}}>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                            </svg>                              
                        </div>
                    </div>
                </div>
            </tr>
        {/each}
        <tr class="row-add" on:mouseenter={() => hoveredElement = null}>
            <td class="cell-add" colspan="8">
                <button class="add-inside"
                    bind:this={addElementButton}
                    on:click={() => isAddLayoverOpen = true}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                    </svg>                  
                    Add Element
                    <div class={`add-layover
                            ${isAddLayoverOpen ? 'open' : ''}
                            ${elements.length < 2 ? 'down' : ''}`}>
                        {#each Object.keys(possibleParams) as type}
                            <button on:click={() => addElement(type)}>
                                {type}
                            </button>
                        {/each}
                    </div>
                </button>
            </td>
        </tr>
    </table>
</div>
<style>
    .action-cont {
        position: absolute;
        right: -104px;
        width: 100%;
        pointer-events: none;
    }
    .action-inner {
        width: fit-content;
        position: sticky;
        left: calc(100vw - 476px);
        pointer-events: all;
        margin-top: 4px;
        display: flex;
    }
    .btn-action {
        background: white;
        border: none;
        border-top: var(--main-border);
        border-bottom: var(--main-border);
        border-radius: 0;
        width: 28px;
        height: 28px;
        cursor: pointer;
        display: none;
        margin: 0;
    }
    .btn-action:first-of-type {
        border-left: var(--main-border);
        border-top-left-radius: var(--main-border-radius);
        border-bottom-left-radius: var(--main-border-radius);
    }
    .btn-action:last-of-type {
        border-right: var(--main-border);
        border-top-right-radius: var(--main-border-radius);
        border-bottom-right-radius: var(--main-border-radius);
    }
    tr.selected .btn-action {
        display: block;
    }
    .btn-action svg {
        width: 14px;
        height: 14px;
        margin-bottom: -3px;
        margin-left: -1px;
        color: rgba(0, 0, 0, 0.7);
    }
    .btn-action.rm svg {
        color: var(--main-error-color-dark);
    }
    .btn-remove:hover {
        background-color: var(--main-hover-color);
    }
    .name-error:focus {
        outline: solid 2px var(--main-error-color);
        border-radius: 2px;
    }
    .add-inside {
        width: fit-content;
        position: relative;
        border: none;
        background-color: white;
        font-family: 'Roboto Mono', monospace;
        cursor: pointer;
        color: rgba(0, 0, 0, 0.8);
    }
    .add-inside:hover {
        color: rgb(0, 0, 0);
    }
    .add-layover {
        position: absolute;
        bottom: 0;
        right: -155px;
        width: 134px;
        background-color: white;
        padding: 8px;
        border: var(--main-border);
        border-radius: var(--main-border-radius);
        display: none;
        z-index: 100;
    }
    .add-layover.down {
        top: 0;
        bottom: auto;
    }
    .add-layover.open {
        display: block;
    }
    .add-layover button {
        margin: 4px;
        color: rgba(0, 0, 0, 0.7);
        font-family: 'Roboto Mono', monospace;
        border: none;
        background: none;
        padding: 0;
        text-align: left;
        cursor: pointer;
        width: 100%;
        z-index: 10000;
    }
    .add-layover button:hover {
        color: rgb(0, 0, 0);
    }
    .cell-add {
        background-color: white;
        padding: 8px;
        position: sticky;
        left: 0;
        border: none;
    }
    .cell-add svg {
        width: 18px;
        height: 18px;
        margin-bottom: -3px;
    }
    .nodeNo {
        text-align: center;
        font-weight: 550;
    }
    .table-outer {
        width: 100%;
        height: 100%;
        padding: 0 10px 10px 10px;
        margin-top: 2px;
        box-sizing: border-box;
        overflow: scroll;
        cursor: grab;
        -khtml-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    .table-outer:active {
        cursor: grabbing;
    }
    .main-table-editor {
        width: 100%;
        border-collapse: collapse;
        position: relative;
    }
    td, th {
        text-align: left;
        padding: 0;
        font-family: 'Roboto Mono', monospace;
        font-size: 14px;
    }
    td {
        border: var(--main-border);
    }
    th {
        font-weight: 550;
        padding: 8px;
        font-family: 'Roboto Mono', monospace;
    }
    tr:first-of-type {
        position: sticky;
        top: 0;
    }
    th:first-of-type {
        position: relative;
        left: -1px;
        background-color: white;
    }
    th:first-of-type::after {
        content: "";
        position: absolute;
        top: 0;
        right: -1px;
        width: 1px;
        height: 100%;
        background-color: white;
    }
    th:last-of-type::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0px;
        width: 2px;
        height: 100%;
        background-color: white;
    }
    .no-edit {
        white-space: nowrap;
        padding: 8px;
    }
    tr {
        background-color: white;
    }
    tr.selected {
        background-color: rgb(250, 250, 250);
    }
    .mobile-select-btn {
        display: none;
    }

    @media (max-width: 600px) {

        .action-inner {
            left: calc(100vw - 116px);
            border-radius: 50px;
        }
        .mobile-select-btn {
            background-color: white;
            border: var(--main-border);
            width: 28px;
            height: 28px;
            box-sizing: border-box;
            border-radius: var(--main-border-radius);
            margin: 0;
            position: relative;
            right: -55px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .mobile-select-btn svg {
            width: 14px;
            height: 14px;
            color: rgba(0, 0, 0, 0.7);
            margin: 7px;
            pointer-events: none;
        }
        .main-table-editor {
            margin-bottom: 62px;
        }
        th {
            position: relative;
            z-index: 1000;
        }
    }
</style>