from typing import List
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv() 

class Recensione(BaseModel):
    id_prodotto: int = Field(description="L'ID numerico del prodotto")
    voto: float = Field(description="Un punteggio da 1 a 5 (può essere decimale)")
    commento: str
    sentiment: str 
    tag_chiave: List[str]

class ProfiloUtente(BaseModel):
    username: str = Field(description="Il nome utente scelto")
    email: str = Field(description="L'indirizzo email")
    attivo: bool = Field(description="True se l'utente è attivo, False altrimenti")
    badge: List[str] = Field(description="Lista dei badge ottenuti dall'utente")


client = instructor.from_openai(OpenAI())

def analizza_recensione(testo: str) -> Recensione:
    """Usa l'LLM per estrarre una struttura Recensione da un testo"""
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=Recensione,
        messages=[
            {"role": "system", "content": "Sei un analista esperto. Estrai i dati richiesti dalla recensione."},
            {"role": "user", "content": testo}
        ]
    )

def estrai_profilo_utente(testo: str) -> ProfiloUtente:
    """Usa l'LLM per estrarre una struttura ProfiloUtente da una descrizione testuale"""
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=ProfiloUtente,
        messages=[
            {"role": "system", "content": "Sei un sistema che estrae dati utente in formato strutturato."},
            {"role": "user", "content": f"Estrai i dati del profilo da questo testo: {testo}"}
        ]
    )


if __name__ == "__main__":
    
   
    testo_recensione = "Il prodotto 4789 è fantastico, voto 4.8. Il codice è pulito e intuitivo!"
    
    
    testo_profilo = "Giuliana, nota come Code456, ha l'email giuliana@aulab.it. È un membro attivo e ha guadagnato i badge: Primo Codice e Fan di Python."
    
    try:
        print("--- Richiesta LLM 1: Analisi Recensione ---")
        recensione = analizza_recensione(testo_recensione)
        print(f"ID Prodotto: {recensione.id_prodotto} | Sentiment: {recensione.sentiment}")
        print(f"Tag: {', '.join(recensione.tag_chiave)}")

        print("\n--- Richiesta LLM 2: Profilo Utente Strutturato ---")
        profilo = estrai_profilo_utente(testo_profilo)
        print(f"Username: {profilo.username}")
        print(f"Email: {profilo.email}")
        print(f"Stato Attivo: {profilo.attivo}")
        print(f"Badge: {', '.join(profilo.badge)}")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")