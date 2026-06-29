from typing import List, TypedDict
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
import os
from dotenv import load_dotenv 


load_dotenv()  


class Recensione(BaseModel):
    id_prodotto: int = Field(description="L'ID numerico del prodotto")
    voto: int = Field(description="Un punteggio da 1 a 5")
    commento: str
    sentiment: str 
    tag_chiave: List[str]

class ProfiloUtente(TypedDict):
    username: str
    email: str
    attivo: bool
    badge: List[str]

# --- Inizializzazione lato Client ---

client = instructor.from_openai(OpenAI())

def analizza_testo_con_llm(testo: str) -> Recensione:
    """Invia il testo all'LLM e forza la risposta nel formato Pydantic"""
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=Recensione,
        messages=[
            {"role": "system", "content": "Sei un analista esperto. Estrai i dati richiesti."},
            {"role": "user", "content": f"Estrai le informazioni da questa recensione: {testo}"}
        ]
    )

# --- 3. Esecuzione ---
if __name__ == "__main__":
    # Testo esempio
    testo_input = "Il prodotto 4789 è fantastico, voto 4.8. Il codice è pulito e intuitivo!"
    
    try:
        print("--- Richiesta all'LLM in corso... ---")
        recensione_validata = analizza_testo_con_llm(testo_input)
        
        print("\n--- ESEMPIO 1: Oggetto Pydantic Validato ---")
        print(f"ID Prodotto: {recensione_validata.id_prodotto}")
        print(f"Sentiment: {recensione_validata.sentiment}")
        print(f"Tag: {', '.join(recensione_validata.tag_chiave)}")

        utente_1: ProfiloUtente = {
            "username": "Code456",
            "email": "giuliana@aulab.it",
            "attivo": True,
            "badge": ["Primo Codice", "Fan di Python"]
        }

        print("\n--- ESEMPIO 2: Dizionario Strutturato (TypedDict) ---")
        print(f"Username: {utente_1['username']}")
        print(f"Stato Attivo: {utente_1['attivo']}")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")