from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Autorise toutes les applications mobiles à interroger ce serveur sur le web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Votre clé API Google AI Studio
GEMINI_API_KEY = "AQ.Ab8RN6JDw80nLeDM1NNt7p0M65aVMgKmiYEf1kN-Z615yimV2A"

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
        url = f"https://googleapis.com{GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": request.message}]}],
            "systemInstruction": {"parts": [{"text": LOGIX_PROMPT}]},
            "generationConfig": {"temperature": 0.3}
        }
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        
        if response.status_code == 200:
            return {"reply": response.json()['candidates'][0]['content']['parts'][0]['text']}
        else:
            return {"reply": f"Erreur Google API (Code {response.status_code})"}
    except Exception as e:
        return {"reply": f"Erreur de transmission : {str(e)}"}