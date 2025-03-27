document.addEventListener("DOMContentLoaded", function () {
    const terminalOutput = document.getElementById("output");
    const commandInput = document.getElementById("command-input");

    function appendToTerminal(text) {
        let newLine = document.createElement("div");
        newLine.textContent = text;
        terminalOutput.appendChild(newLine);
        terminalOutput.scrollTop = terminalOutput.scrollHeight; // Scroll vers le bas
    }

    commandInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            let command = commandInput.value.trim();
            if (command) {
                appendToTerminal("trhacknon@kali:~$ " + command);
                commandInput.value = "";
                simulateTyping("Processing command...", () => {
                    fetch("/execute", {
                        method: "POST",
                        body: new URLSearchParams({ command: command }),
                        headers: { "Content-Type": "application/x-www-form-urlencoded" }
                    })
                    .then(response => response.json())
                    .then(data => {
                        simulateTyping(data.response, () => {
                            commandInput.focus();
                        });
                    });
                });
            }
        }
    });

    function simulateTyping(text, callback) {
        let index = 0;
        let interval = setInterval(() => {
            if (index < text.length) {
                appendToTerminal(text[index]);
                index++;
            } else {
                clearInterval(interval);
                appendToTerminal(""); // Ajoute une ligne vide après le texte
                callback();
            }
        }, 20); // Vitesse de frappe simulée
    }

    commandInput.focus();
});
