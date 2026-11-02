document.addEventListener("DOMContentLoaded", function {
    // Function to render Mermaid diagrams
    function renderMermaidDiagrams() {
        if (window.mermaid) {
            mermaid.initialize({
                startOnLoad: true,
                theme: "dark", // Use the dark theme for better visual consistency
                securityLevel: "strict",
                themeVariables: {
                    background: "#1d2021", // Gruvbox background
                    primaryColor: "#fabd2f", // Gruvbox yellow
                    edgeLabelBackground: "#282828", // Gruvbox dark
                    labelColor: "#ebdbb2", // Gruvbox text
                },
            });

            mermaid.init(undefined, document.querySelectorAll(".mermaid"));
        }
    }

    // Render Mermaid diagrams initially
    renderMermaidDiagrams();

    // Monitor navigation changes for re-rendering
    document.addEventListener('navigation', function() {
        renderMermaidDiagrams();
    });
});
