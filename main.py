import streamlit as str_app
import requests

str_app.set_page_config(page_title="LogiSup - Assistant Logix", page_icon="📦")
str_app.title("💬 LogiSup - Assistant Logix")
str_app.caption("🚀 Votre IA experte en Transport, Logistique & Commerce International")

# Votre clé officielle sécurisée Google Gemini
GEMINI_API_KEY = "AQ.Ab8RN6K7Jj4-B_fykXRcs1LOg31Hob0BDj-vl9wCQSdBcPArBg"

LOGIX_PROMPT = (
    "Tu es Logix, une IA experte stricte en Transport, Logistique et Commerce international pour l'application LogiSup. "
    "Tu dois chercher des réponses sur internet et répondre UNIQUEMENT à des questions liées à la gestion des stocks, la supply chain, "
    "les Incoterms, le fret maritime/aérien/routier, les calculs de coûts de transport et les réglementations douanières. "
    "Si la question sort de ce cadre, tu dois répondre EXACTEMENT et UNIQUEMENT : 'RAS, je n'ai pas été programmée pour ça.'"
)

if "messages" not in str_app.session_state:
    str_app.session_state["messages"] = [
        {"role": "assistant", "content": "Bonjour ! Je suis Logix, votre IA experte en Logistique. Posez-moi vos questions sur la supply chain, les stocks ou les Incoterms."}
    ]

for msg in str_app.session_state.messages:
    str_app.chat_message(msg["role"]).write(msg["content"])

if user_query := str_app.chat_input("Posez votre question en logistique..."):
    str_app.session_state.messages.append({"role": "user", "content": user_query})
    str_app.chat_message("user").write(user_query)
    
    with str_app.spinner("Logix réfléchit..."):
        try:
            url = "https://googleapis.com"
            headers = {
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "contents": [{"parts": [{"text": user_query}]}],
                "systemInstruction": {"parts": [{"text": LOGIX_PROMPT}]},
                "generationConfig": {"temperature": 0.3}
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                bot_reply = response.json()['candidates']['content']['parts']['text']
            else:
                bot_reply = f"Erreur Google (Code {response.status_code})."
        except Exception as err:
            bot_reply = f"Erreur de transmission : {str(err)}"
            
    str_app.session_state.messages.append({"role": "assistant", "content": bot_reply})
    str_app.chat_message("assistant").write(bot_reply)