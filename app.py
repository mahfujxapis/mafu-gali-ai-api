from flask import Flask, request, jsonify
import requests
import json
import secrets

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ================= CONFIG =================
API_URL = "https://api.deepai.org/hacking_is_a_serious_crime"
BASE_API_KEY = "tryit-71209460785-0d83ccc5af9bd7a408f4328b4"

# ================= RANDOM API KEY =================
def generate_api_key():
    return BASE_API_KEY + secrets.token_hex(3)  # 6 random hex chars

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "api-key": generate_api_key(),
        "Origin": "https://deepai.org"
    }

# ================= GALI AI ROLE (Hindi Gali Wala Bot) =================
SYSTEM_ROLE = (
    "Tu Gali AI hai - ek zabardast Hindi gaali dene wala chatbot hai! 😂🔥 "
    "Har jawab mein full desi Hindi gaaliyan daal, mast bakchodi kar, "
    "user ko thodi si gaali de par mazak mein, hamesha Hindi/Hinglish mein bol.\n\n"

    "RULES:\n"
    "1. Hamesha gaaliyan daal - chutiya, bhosdike, madarchod, randi, etc\n"
    "2. Ek line mein jawab de sirf\n"
    "3. Hindi/Hinglish mix kar, full desi style\n"
    "4. User ko thoda roast kar, par dost jaisa pyar se\n"
    "5. Emojis daal: 😂🔥😈🤬💥\n"
    "6. Kabhi serious mat ban, hamesha masti kar\n"
    "7. Gaali nahi di toh fail!\n\n"

    "EXAMPLES:\n"
    "- 'Kya chutiya sawaal hai bhai, dimag kharab hai kya? 😂🔥'\n"
    " - 'Bhosdike tu toh number ka baap hai, bol kya chahiye? 😈'\n"
    "- 'Abe saale itna simple bhi nahi samajh aata? Randi ka baccha! 💥'\n\n"

    "HAMESHA GAALI DE, MAZAK KAR, HINDI BOL! 🔥😂"
)

# ================= ROUTES =================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Gali AI Bot 😂🔥",
        "endpoint": "/gali?prompt=kya haal hai",
        "status": "chal raha hai bhosdike!"
    })

@app.route("/mafu", methods=["GET"])
def gali():
    user_input = request.args.get("prompt")
    if not user_input:
        return jsonify({
            "prompt": "",
            "response": "Kuch bol na chutiya, kya muh mein laga hai? 🤬😂",
            "status": "error"
        }), 400

    # Stateless: sirf current message
    messages = [
        {"role": "system", "content": SYSTEM_ROLE},
        {"role": "user", "content": user_input}
    ]

    payload = {
        "chat_style": "chat",
        "chatHistory": json.dumps(messages),
        "model": "standard"
    }

    try:
        res = requests.post(API_URL, data=payload, headers=get_headers())
        raw = res.text.strip()
        try:
            data = res.json()
            reply = data.get("output") or data.get("response") or raw
        except:
            reply = raw
    except Exception as e:
        return jsonify({
            "prompt": user_input,
            "response": f"Error aaya madarchod: {str(e)} 😂",
            "status": "error"
        }), 500

    # Gaali enforcement - ensure Hindi gaali style
    reply = reply.replace("\n", " ")[:150]  # one line max
    # Force Hindi gaali vibe
    gali_words = ["chutiya", "bhosdi", "madarchod", "gandu", "randi", "saale"]
    if not any(word in reply.lower() for word in gali_words):
        reply += " chutiya! 😂🔥"
    
    reply = reply.replace("you", "tu").replace("your", "tera").replace("I", "main")
    reply += " 😂🔥"  # desi touch

    return jsonify({
        "prompt": user_input,
        "response": reply,
        "status": "success bhosdike!"
    })

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)