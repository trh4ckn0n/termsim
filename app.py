import os
from flask import Flask, render_template, request, jsonify, session
import openai
from dotenv import load_dotenv

# Charger la clé API OpenAI depuis .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = "trhacknon-secret-key"  # Nécessaire pour gérer les sessions

# Initialisation de l'état de l'utilisateur
def get_user_state():
    return session.get("user_state", "user")  # "user" ou "root"

def set_user_state(state):
    session["user_state"] = state

@app.route('/')
def index():
    # Assurer un état initial
    if "user_state" not in session:
        session["user_state"] = "user"
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    user_input = request.form['command']
    user_state = get_user_state()
    
    # Gestion des commandes spécifiques
    if user_input.strip() == "pkexec":
        if user_state == "user":
            set_user_state("root")
            response_text = "Vulnerability in pkexec exploited! You are now root."
        else:
            response_text = "You are already root."
    elif user_input.strip() in ["sudo su", "su"]:
        if user_state == "user":
            set_user_state("root")
            response_text = "Permission granted. You are now root."
        else:
            response_text = "You are already root."
    elif user_input.strip() == "id":
        response_text = "uid=0(root) gid=0(root) groups=0(root)" if user_state == "root" else "uid=1000(kali) gid=1000(kali) groups=1000(kali),27(sudo)"
    elif user_input.strip() == "ls":
        response_text = "Desktop  Downloads  Documents  Music  Pictures  Videos"
    else:
        # Envoi à OpenAI pour une simulation réaliste
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a simulated Kali Linux terminal, responding exactly like a real shell."},
                {"role": "user", "content": f"The user is currently {user_state}. They entered: {user_input}"}
            ],
            max_tokens=750,
            temperature=0.7
        )
        response_text = response['choices'][0]['message']['content'].strip()

    # Génération du prompt en fonction de l'état de l'utilisateur
    prompt = "root@kali:~# " if get_user_state() == "root" else "trhacknon@kali:~$ "
    
    return jsonify({'response': response_text, 'prompt': prompt})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
