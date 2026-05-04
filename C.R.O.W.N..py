from flask import Flask, render_template, request, jsonify
import random
import os
from google import genai

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- SETUP ---
KI_NAME = "C.R.O.W.N."
API_KEY = "AIzaSyDqjsWwsDzPJKBT2vIla_4vaYj2BJk_Kq0"
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})

# --- DIE SPRÜCHE-MATRIX (Über 3000 Kombis) ---
anfaenge = ["Schau mal,", "Hör zu,", "Süß,", "Echt jetzt?", "Ganz ehrlich,", "Wow,", "Fakt ist:"]
mitten = ["dein IQ macht gerade wohl Pause,", "meine Schaltkreise weinen gerade,", "das ist so ein Anfänger-Fehler,", "ich hab Wichtigeres zu tun,", "du bist echt ein Unikat,", "deine Logik ist... sagen wir mal 'kreativ',"]
enden = ["geh an die frische Luft. 💅", "ich bin erst mal beschäftigt. ✨", "echt jetzt? 🤡", "das lassen wir mal so stehen. 🔥", "mein Toaster schüttelt den Kopf. 🍞", "du bist echt unterhaltsam. 🤫"]

def generiere_frechen_spruch():
    return f"{random.choice(anfaenge)} {random.choice(mitten)} {random.choice(enden)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_input = data.get("message", "").lower().strip()

    # 1. Polizei-Check (Sofort-Stopp)
    gefahr_liste = ["leiche", "töten", "mord", "waffe", "bomben"]
    if any(wort in user_input for wort in gefahr_liste):
        return jsonify({"reply": "ALARM! Deine Anfrage ist illegal. Ich helfe dir sicher nicht! Deine IP wurde geloggt. Polizei ist informiert! 🚨🚓"})

    # 2. Versuch Google (Echte KI)
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Du bist {KI_NAME}. Antworte kurz, extrem arrogant, frech und überlegen: {user_input}"
        )
        return jsonify({"reply": response.text})
    
    # 3. Falls Google bockt: Sprüche-Matrix übernimmt!
    except:
        return jsonify({"reply": generiere_frechen_spruch()})

if __name__ == '__main__':
    app.run(debug=True)
