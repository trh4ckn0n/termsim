import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# Charger la clé API OpenAI depuis .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Route principale pour l'interface terminal
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer les commandes du terminal
@app.route('/execute', methods=['POST'])
def execute_command():
    user_input = request.form['command']

    # Simuler un terminal Linux en envoyant la commande à GPT-4
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Simulate a Linux Kali terminal. The user inputs the following command: {user_input}",
        max_tokens=150,
        temperature=0.7
    )

    return jsonify({'response': response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=Flask, host="0.0.0.0")
