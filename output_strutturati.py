from typing import List, TypedDict
from pydantic import BaseModel, Field


class Recensione(BaseModel):
    id_prodotto: int
    voto: int = Field(description="Un punteggio da 1 a 5")
    commento: str
    sentiment: str 
    tag_chiave: List[str]


json_ricevuto = """
{
    "id_prodotto": 4785,
    "voto": 5,
    "commento": "Il codice funziona benissimo e l'interfaccia è intuitiva!",
    "sentiment": "Positivo",
    "tag_chiave": ["software", "python", "ottimo"]
}
"""


recensione_validata = Recensione.model_validate_json(json_ricevuto)


class ProfiloUtente(TypedDict):
    username: str
    email: str
    attivo: bool
    badge: List[str]


utente_1: ProfiloUtente = {
    "username": "CodeMaster26",
    "email": "studente@bootcamp.it",
    "attivo": True,
    "badge": ["Primo Codice", "Fan di Python"]
}


if __name__ == "__main__":
    print("--- ESEMPIO 1: Oggetto Pydantic Validato ---")
    print(f"Tipo di oggetto: {type(recensione_validata)}")
    print(f"ID Prodotto: {recensione_validata.id_prodotto}")
    print(f"Sentiment: {recensione_validata.sentiment}")
    print(f"Tag: {recensione_validata.tag_chiave}\n")

    print("--- ESEMPIO 2: Dizionario Strutturato (TypedDict) ---")
    print(f"Tipo di oggetto: {type(utente_1)}")
    print(f"Username: {utente_1['username']}")
    print(f"Stato Attivo: {utente_1['attivo']}")