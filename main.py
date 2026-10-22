import streamlit as str_app
import requests

str_app.set_page_config(page_title="LogiSup - Assistant Logix", page_icon="📦")
str_app.title("💬 LogiSup - Assistant Logix")
str_app.caption("🚀 Application Connectée au Serveur Cloud Mondial")

if "messages" not in str_app.session_state:
    str_app.session_state["messages"] = [
        {"role": "assistant", "content": "Bonjour ! Je suis Logix, votre IA experte en Logistique connectée au Cloud. Posez-moi vos questions sur la supply chain, les stocks ou les Incoterms."}
    ]

for msg in str_app.session_state.messages:
    str_app.chat_message(msg["role"]).write(msg["content"])

if user_query := str_app.chat_input("Posez votre question en logistique..."):
    str_app.session_state.messages.append({"role": "user", "content": user_query})
    str_app.chat_message("user").write(user_query)
    
    with str_app.spinner("Connexion au serveur mondial Render (Logix réfléchit...)..."):
        try:
            # L'interface graphique interroge désormais votre VRAI serveur en ligne
            url = "https://onrender.com"
            response = requests.post(url, json={"message": user_query}, timeout=30)
            
            if response.status_code == 200:
                bot_reply = response.json().get("reply", "Pas de réponse reçue.")
            else:
                bot_reply = f"Erreur du serveur distant (Code {response.status_code})."
        except Exception as err:
            bot_reply = f"Erreur de liaison Internet : {str(err)}"
            
    str_app.session_state.messages.append({"role": "assistant", "content": bot_reply})
    str_app.chat_message("assistant").write(bot_reply)