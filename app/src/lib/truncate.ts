export const truncate = (
    node: HTMLElement,
    { text }: { text: string }
) => {
    const resizeObserver = new ResizeObserver(() => updateTruncation());
    resizeObserver.observe(node);

    function updateTruncation() {


        const maxWidth = node.offsetWidth;
        let truncatedText = text;
        node.textContent = text;

        while (node.scrollWidth > maxWidth && truncatedText.length > 0) {
            truncatedText = truncatedText.slice(0, -1);
            node.textContent = truncatedText + "...";
        }
    }

    // Initial truncation
    updateTruncation();

    return {
        update(newParams: { text: string }) {
            text = newParams.text;
            updateTruncation();
        },
        destroy() {
            resizeObserver.disconnect();
        },
    };
}