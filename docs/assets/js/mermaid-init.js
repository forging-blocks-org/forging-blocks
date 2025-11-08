document.addEventListener("DOMContentLoaded", () => {
     (!window.mermaid) return;

    rmaid.initialize({
        tOnLoad: false,
        e: "dark",
        eVariables: {
            ound: "#1d2021",
            yColor: "#3c3836",
            yTextColor: "#ebdbb2",
            yBorderColor: "#928374",
            lor: "#928374",
            aryColor: "#282828",
            ryColor: "#504945",

        rityLevel: "loose",
    ;

    nst codeBlocks = document.querySelectorAll("pre code.language-mermaid");
    deBlocks.forEach((codeBlock) => {
        t pre = codeBlock.parentElement;
        t graphDefinition = codeBlock.textContent.trim();

        t mermaidDiv = document.createElement("div");
        aidDiv.classList.add("mermaid");
        aidDiv.textContent = graphDefinition;

        parentElement.replaceChild(mermaidDiv, pre);
    ;

    rmaid.run();
});
