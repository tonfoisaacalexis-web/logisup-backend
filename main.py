from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Votre clé API officielle au nouveau format Google
GEMINI_API_KEY = "AQ.Ab8RN6K7Jj4-B_fykXRcs1LOg31Hob0BDj-vl9wCQSdBcPArBg"

LOGIX_PROMPT = (
    "Tu es Logix, une IA experte stricte en Transport, Logistique et Commerce international pour l'application LogiSup. "
    "Tu dois chercher des réponses sur internet et répondre UNIQUEMENT à des questions liées à la gestion des stocks, la supply chain, "
    "les Incoterms, le fret maritime/aérien/routier, les calculs de coûts de transport et les réglementations douanières. "
    "Si la question sort de ce cadre, tu dois répondre EXACTEMENT et UNIQUEMENT : 'RAS, je n'ai pas été programmée pour ça.'"
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Le serveur de Logix est en ligne et fonctionnel !"}

@app.post("/chat")
def chat_with_logix(request: ChatRequest):
    try:
        # URL et En-têtes adaptés pour valider le nouveau format de clé sécurisée Google
        url = "https://googleapis.com"
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{"parts": [{"text": request.message}]}],
            "systemInstruction": {"parts": [{"text": LOGIX_PROMPT}]},
            "generationConfig": {"temperature": 0.3}
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return {"reply": response.json()['candidates'][0]['content']['parts'][0]['text']}
        else:
            return {"reply": f"Erreur d'authentification Google Cloud (Code {response.status_code})."}
    except Exception as e:
        return {"reply": f"Erreur de transmission : {str(e)}"}