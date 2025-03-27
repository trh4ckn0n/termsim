document.getElementById('command-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        const command = this.value;
        this.value = '';
        
        // Ajouter la commande à l'écran
        const output = document.getElementById('output');
        
        // Afficher le prompt selon l'état (normal ou root)
        const prompt = (command.includes("pkexec")) ? "root@kali:~#" : "user@kali:~$";
        output.innerHTML += `<div><span style="color: #ff0;">${prompt}</span> ${command}</div>`;
        
        // Envoyer la commande au serveur Flask pour exécution
        fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `command=${command}`
        })
        .then(response => response.json())
        .then(data => {
            output.innerHTML += `<div>${data.response}</div>`;
            window.scrollTo(0, document.body.scrollHeight); // Scroller jusqu'en bas
        });
    }
});
