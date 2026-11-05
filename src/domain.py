"""Vocabolario di dominio condiviso tra generatore, parser e test.

Tutti i valori sono fittizi. Per usare un PDF diverso con la stessa
struttura basta adattare queste liste e puntare RAG_PDF_PATH al file.
"""

# Marche riconosciute in fase di arricchimento (ordine = priorita di match)
BRANDS = ["Voltaris", "Sunwave", "Ampera", "Heliora", "Termika", "Chargex"]

# Frasi che identificano una pagina-domanda dell'albero decisionale
QUESTION_KEYWORDS = [
    "Dove riscontra", "Di che marca", "Quale problematica",
    "Quale problema", "Ha gia provato", "Quando e stata",
    "C'e stato", "Cosa si e danneggiato", "Da dove proviene",
]

# Domanda radice: quando compare, il percorso nell'albero riparte da zero
ROOT_QUESTION = "Dove riscontra"

# Parole chiave che identificano una riga-opzione su una pagina-domanda
OPTION_KEYWORDS = [
    "Inverter", "Batteria", "Wallbox", "Caldaia", "termico", "Evento",
    "Wi-Fi", "connessione", "Errore", "Riavvio", "Produzione", "Display",
    "Perdita", "Pressione", "Grandine", "App", "Richiesta",
] + BRANDS

UNKNOWN_BRAND = "Sconosciuta"
