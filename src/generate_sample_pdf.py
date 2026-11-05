"""Fase 0 - Genera un manuale di assistenza tecnica FITTIZIO in PDF.

Il PDF riproduce la struttura del manuale operativo usato dalla pipeline
(pagine-domanda dell'albero decisionale + pagine-soluzione con i campi
Tripletta / Note Standard / Note / Assegnazione / Script / Tempistiche),
ma con contenuti completamente inventati: nessun dato sensibile.
"""
import fitz
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
OUTPUT_PDF = PROJECT_DIR / "data" / "sample_manual.pdf"

TRIPLETTA_PV = "Richiesta - Fotovoltaico - Assistenza Tecnica"
TRIPLETTA_TERMICO = "Richiesta - Termico - Assistenza Tecnica"
TRACCIATURA = "Nessuna, solo per tracciatura"
TEAM_ELETTRICO = "Team Tecnico Elettrico"
TEAM_TERMICO = "Team Tecnico Termico"
SCRIPT_RICHIAMO = ("La invito a seguire la guida che le inviamo via email. Se entro 24 ore "
                   "il problema non si risolve, ci contatti nuovamente.")
SCRIPT_ESCALATION = "Le confermo che abbiamo aperto una segnalazione verso il reparto tecnico competente."

# Domande per livello dell'albero decisionale
LEVEL_QUESTIONS = [
    "Dove riscontra il problema il cliente?",
    "Di che marca e il componente installato?",
    "Quale problematica descrive il cliente?",
]

# Alternative mostrate sulle pagine-domanda (la scelta seguita e sempre la prima)
LEVEL_ALTERNATIVES = [
    ["Inverter", "Batteria", "Wallbox", "Caldaia ibrida", "Impianto termico", "Evento climatico"],
    ["Voltaris", "Sunwave", "Ampera", "Heliora", "Termika", "Chargex"],
    [],
]

SOLUTIONS = [
    # --- Inverter -------------------------------------------------------
    dict(path=["Inverter", "Voltaris", "Connessione Wi-Fi assente"],
         tripletta=TRIPLETTA_PV, note_standard="Inverter Voltaris",
         note="inserire che si tratta di un problema di connessione, data di installazione, codice "
              "inverter e recapito del cliente; inviare la guida demo di collegamento Wi-Fi.",
         assegnazione=TRACCIATURA, script=SCRIPT_RICHIAMO),
    dict(path=["Inverter", "Voltaris", "Riavvio non effettuato"],
         tripletta=TRIPLETTA_PV, note_standard="Inverter Voltaris",
         note="inserire che il riavvio non e stato effettuato e inviare la guida demo di "
              "spegnimento e riavvio dell'inverter.",
         assegnazione=TRACCIATURA, script=SCRIPT_RICHIAMO),
    dict(path=["Inverter", "Voltaris", "Errore con codice, produzione bassa"],
         tripletta=TRIPLETTA_PV, note_standard="Inverter Voltaris",
         note="inserire il codice di errore mostrato a display, la data di installazione e la "
              "produzione giornaliera stimata dal cliente.",
         assegnazione=TEAM_ELETTRICO, script=SCRIPT_ESCALATION, tempistiche="Entro 5 giorni lavorativi"),
    dict(path=["Inverter", "Voltaris", "Riavvio effettuato ma non risolutivo"],
         tripletta=TRIPLETTA_PV, note_standard="Inverter Voltaris",
         note="inserire che il riavvio e stato effettuato senza esito e che l'inverter risulta "
              "connesso alla rete domestica.",
         assegnazione=TEAM_ELETTRICO, script=SCRIPT_ESCALATION, tempistiche="Entro 5 giorni lavorativi"),
    dict(path=["Inverter", "Sunwave", "Produzione intermittente con molto sole"],
         tripletta=TRIPLETTA_PV, note_standard="Inverter Sunwave",
         note="inserire che la produzione si interrompe nelle ore di massimo irraggiamento; "
              "fornire al cliente il numero dell'assistenza del produttore.",
         assegnazione=TRACCIATURA,
         script="Per questa anomalia la invito a contattare direttamente l'assistenza del produttore."),
    dict(path=["Inverter", "Sunwave", "Errore inverter spento"],
         tripletta=TRIPLETTA_PV, note_standard="Inverter Sunwave",
         note="inserire che l'inverter risulta spento, la data di installazione e se c'e stato "
              "un temporale nei giorni precedenti.",
         assegnazione=TEAM_ELETTRICO, script=SCRIPT_ESCALATION),
    # --- Batteria -------------------------------------------------------
    dict(path=["Batteria", "Ampera", "Batteria spenta dopo il riavvio"],
         tripletta=TRIPLETTA_PV, note_standard="Anomalia batterie Ampera",
         note="inserire che la batteria resta spenta anche dopo il riavvio guidato e lo stato "
              "dei led frontali.",
         assegnazione=TEAM_ELETTRICO, script=SCRIPT_ESCALATION, tempistiche="Entro 3 giorni lavorativi"),
    dict(path=["Batteria", "Ampera", "Batteria non si carica, riavvio non effettuato"],
         tripletta=TRIPLETTA_PV, note_standard="Anomalia batterie Ampera",
         note="inserire che la batteria non accumula energia e inviare la guida demo di riavvio "
              "del sistema di accumulo.",
         assegnazione=TRACCIATURA, script=SCRIPT_RICHIAMO),
    dict(path=["Batteria", "Heliora", "Richiesta assistenza batterie"],
         tripletta=TRIPLETTA_PV, note_standard="Anomalia batterie Heliora",
         note="inserire la richiesta del cliente e fornire il contatto del servizio clienti "
              "del produttore delle batterie.",
         assegnazione=TRACCIATURA,
         script="Per le batterie di questa marca l'assistenza e gestita direttamente dal produttore."),
    # --- Wallbox --------------------------------------------------------
    dict(path=["Wallbox", "Chargex", "Display spento, non carica"],
         tripletta=TRIPLETTA_PV, note_standard="Wallbox Chargex (colonnina di ricarica)",
         note="inserire che la colonnina non eroga corrente, che il display e spento e la data "
              "di installazione.",
         assegnazione=TEAM_ELETTRICO, script=SCRIPT_ESCALATION, tempistiche="Entro 5 giorni lavorativi"),
    dict(path=["Wallbox", "Chargex", "App non sincronizzata"],
         tripletta=TRIPLETTA_PV, note_standard="Wallbox Chargex (colonnina di ricarica)",
         note="inserire che l'app non mostra i dati di ricarica e inviare la guida demo di "
              "associazione dell'app.",
         assegnazione=TRACCIATURA, script=SCRIPT_RICHIAMO),
    # --- Caldaia ibrida -------------------------------------------------
    dict(path=["Caldaia ibrida", "Termika", "Perdita d'acqua dopo il collaudo"],
         tripletta=TRIPLETTA_TERMICO, note_standard="Caldaia ibrida Termika",
         note="inserire che la perdita d'acqua e comparsa dopo il collaudo eseguito dal "
              "produttore e fornire il contatto del centro assistenza autorizzato.",
         assegnazione=TRACCIATURA,
         script="Essendo stato eseguito il collaudo, la invito a contattare il centro assistenza del produttore."),
    dict(path=["Caldaia ibrida", "Termika", "Errore caldaia in blocco"],
         tripletta=TRIPLETTA_TERMICO, note_standard="Caldaia ibrida Termika",
         note="inserire il codice di blocco mostrato dalla caldaia e se il cliente ha gia "
              "provato lo sblocco manuale.",
         assegnazione=TEAM_TERMICO, script=SCRIPT_ESCALATION, tempistiche="Entro 2 giorni lavorativi"),
    # --- Impianto termico -----------------------------------------------
    dict(path=["Impianto termico", "Perdita di pressione tra 1.5 e 2 bar"],
         tripletta=TRIPLETTA_TERMICO, note_standard="Impianto termico con problemi",
         note="inserire che la pressione oscilla tra 1.5 e 2 bar, valore nella norma; "
              "rassicurare il cliente.",
         assegnazione=TRACCIATURA,
         script="Le confermo che una pressione tra 1.5 e 2 bar rientra nei valori di normale funzionamento."),
    dict(path=["Impianto termico", "Pressione sotto 1 bar"],
         tripletta=TRIPLETTA_TERMICO, note_standard="Impianto termico con problemi",
         note="inserire che la pressione scende sotto 1 bar anche dopo il ricarico manuale.",
         assegnazione=TEAM_TERMICO, script=SCRIPT_ESCALATION),
    # --- Evento climatico -----------------------------------------------
    dict(path=["Evento climatico", "Grandine sui moduli"],
         tripletta=TRIPLETTA_PV, note_standard="Evento climatico/Grandine",
         note="inserire data dell'evento, foto dei moduli danneggiati e se l'impianto produce ancora.",
         assegnazione=TEAM_ELETTRICO, script=SCRIPT_ESCALATION, tempistiche="Entro 10 giorni lavorativi"),
]

PAGE_W, PAGE_H = fitz.paper_size("a4")
MARGIN = 50
FONT_SIZE = 10
MAX_CHARS = 90


def wrap(text, width=MAX_CHARS):
    """A capo manuale: le righe di continuazione non iniziano mai con una maiuscola,
    cosi il parser (che si ferma alla prima riga maiuscola) cattura tutto il campo."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width or not current or word[0].isupper():
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def write_lines(page, lines):
    y = MARGIN + FONT_SIZE
    for line in lines:
        page.insert_text((MARGIN, y), line, fontsize=FONT_SIZE, fontname="helv")
        y += FONT_SIZE * 1.6


def add_cover(doc):
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    write_lines(page, [
        "# Manuale DEMO - Assistenza Tecnica Impianti",
        "# Documento fittizio generato automaticamente a scopo dimostrativo.",
        "# Marche, team e procedure sono inventati.",
    ])


def add_question_page(doc, level, chosen):
    if level == 0:
        kind = 0
    elif chosen in LEVEL_ALTERNATIVES[1]:
        kind = 1
    else:
        kind = 2
    alternatives = [a for a in LEVEL_ALTERNATIVES[kind] if a != chosen]
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    lines = [LEVEL_QUESTIONS[kind], ""]
    lines += [f"- {opt}" for opt in [chosen] + alternatives]
    write_lines(page, lines)


def add_solution_page(doc, sol):
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    lines = [
        f"Tripletta: {sol['tripletta']}",
        f"Note Standard: {sol['note_standard']}",
        *wrap(f"Note: {sol['note']}"),
        f"Assegnazione: {sol['assegnazione']}",
        *wrap(f"Script: {sol['script']}"),
    ]
    if sol.get("tempistiche"):
        lines.append(f"Tempistiche: {sol['tempistiche']}")
    write_lines(page, lines)


def generate(output_path=OUTPUT_PDF):
    doc = fitz.open()
    add_cover(doc)
    for sol in SOLUTIONS:
        for level, chosen in enumerate(sol["path"]):
            add_question_page(doc, level, chosen)
        add_solution_page(doc, sol)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    total = len(doc)
    doc.close()
    return total


if __name__ == "__main__":
    pages = generate()
    print(f"Manuale demo generato: {OUTPUT_PDF}")
    print(f"Pagine: {pages} | Soluzioni: {len(SOLUTIONS)}")
