from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Indispensable pour autoriser les smartphones à se connecter via Internet
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOGIX_PROMPT = (
    "Tu es Logix, une IA experte stricte en Transport, Logistique et Commerce international pour l'application LogiSup. "
    "Réponds UNIQUEMENT à des questions liées à la gestion des stocks, la supply chain, les Incoterms, le fret maritime/aérien/routier, "
    "les calculs de coûts de transport et les réglementations douanières. Si la question sort de ce cadre, réponds strictement : "
    "'RAS, je n'ai pas été programmée pour ça.'"
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Le serveur mondial de LogiSup est en ligne et prêt !"}

@app.post("/chat")
def chat_with_logix(request: ChatRequest):
    try:
        url = "https://groq.com"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": LOGIX_PROMPT},
                {"role": "user", "content": request.message}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return {"reply": response.json()['choices']['message']['content']}
        else:
            return {"reply": f"Erreur de passerelle Cloud (Code {response.status_code})"}
    except Exception as e:
        return {"reply": f"Erreur de transmission réseau : {str(e)}"}