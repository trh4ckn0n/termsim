import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# Charger la clé API OpenAI depuis .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Variable globale pour simuler l'état de l'utilisateur (root ou normal)
user_state = "normal"  # "normal" ou "root"

# Route principale pour l'interface terminal
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer les commandes du terminal
@app.route('/execute', methods=['POST'])
def execute_command():
    global user_state
    user_input = request.form['command']
    
    # Simulation de pkexec pour escalader les privilèges
    if 'pkexec' in user_input:
        if user_state == "normal":
            # Simuler l'exploitation de pkexec pour obtenir les privilèges root
            user_state = "root"
            response_text = "Vulnerability in pkexec exploited! You are now root."
        else:
            response_text = "You are already root."
    elif 'sudo' in user_input or 'su' in user_input:
        if user_state == "normal":
            # Simuler l'élévation de privilèges
            user_state = "root"
            response_text = "Permission granted. You are now root."
        else:
            response_text = "You are already root."
    else:
        # Envoyer la commande à GPT-4 en utilisant l'API de chat
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a simulated Kali Linux terminal responding as if the user were in a real terminal session."},
                {"role": "user", "content": f"The user is in {user_state} mode. The user inputs the following command: {user_input}"}
            ],
            max_tokens=750,
            temperature=0.7
        )
        response_text = response['choices'][0]['message']['content'].strip()

    # Renvoi de la réponse du terminal simulé
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
