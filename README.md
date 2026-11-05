# RAG Assistenza Tecnica

Sistema **Retrieval-Augmented Generation (RAG)** per l'assistenza tecnica su impianti fotovoltaici e termici.
Estrae le soluzioni da un manuale PDF strutturato ad albero decisionale, le indicizza semanticamente e risponde alle domande restituendo categoria, note, script e assegnazione.

> **Dati di esempio.** Il manuale incluso è un PDF **fittizio** generato da `src/generate_sample_pdf.py`. Marche (Voltaris, Sunwave, Ampera, Heliora, Termika, Chargex), team e procedure sono inventati a scopo dimostrativo.

## Obiettivo

Trovare automaticamente la procedura corretta a partire dalla descrizione di un problema (es. *"inverter con Wi-Fi scollegato"*, *"caldaia ibrida con perdita d'acqua"*), restituendo la soluzione più pertinente del manuale.

## Architettura

```
generate_sample_pdf.py  →  data/sample_manual.pdf
                                  ↓
                          parse_pdf.py     →  output/chunks.json
                                  ↓
                          build_index.py   →  output/index/
                                  ↓
                          query_engine.py  →  risposte strutturate
                                  ↓
                          benchmark.py     →  report + grafici
```

| Fase | Script | Output |
|------|--------|--------|
| 0 — Manuale di esempio | `src/generate_sample_pdf.py` | `data/sample_manual.pdf` (16 soluzioni, 62 pagine) |
| 1 — Parsing | `src/parse_pdf.py` | `output/chunks.json` |
| 2 — Indicizzazione | `src/build_index.py` | `output/index/` (vector store LlamaIndex) |
| 3 — Query Engine | `src/query_engine.py` | `output/query_results.json` |
| 4 — Benchmark | `src/benchmark.py` | `output/benchmark_report.json`, `benchmark_plot.png` |

Tutto ciò che sta in `output/` è rigenerabile e non viene versionato.

## Struttura del progetto

```
├── data/
│   ├── sample_manual.pdf        # Manuale fittizio (generato)
│   └── golden_queries.json      # Dataset di test (8 query)
├── src/
│   ├── domain.py                # Vocabolario di dominio (marche, parole chiave)
│   ├── generate_sample_pdf.py   # Generatore del manuale di esempio
│   ├── parse_pdf.py             # Estrazione chunk dal PDF
│   ├── build_index.py           # Creazione indice vettoriale
│   ├── query_engine.py          # Motore di query RAG
│   └── benchmark.py             # Benchmark e metriche
├── output/                      # Artefatti generati (ignorati da git)
├── notebooks/
└── requirements.txt
```

## Tecnologie

| Componente | Tecnologia | Ruolo |
|------------|------------|-------|
| Framework RAG | [LlamaIndex](https://www.llamaindex.ai/) | Orchestrazione retrieval + generazione |
| Parsing / generazione PDF | [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`) | Estrazione e creazione testo strutturato |
| Embedding | OpenAI `text-embedding-3-small` *oppure* HuggingFace `BAAI/bge-small-en-v1.5` | Vettorizzazione chunk |
| LLM | OpenAI `gpt-4o-mini` (opzionale) | Sintesi della risposta |
| Reranking | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Riordino per rilevanza |
| Vector store | LlamaIndex (persistente su disco) | Ricerca per similarità |
| Analisi | pandas, matplotlib | Benchmark e grafici |

## Setup

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install llama-index-embeddings-huggingface sentence-transformers
```

Opzionale: impostare la variabile d'ambiente `OPENAI_API_KEY`. Senza API key il sistema funziona in **modalità locale** (embedding HuggingFace + solo retrieval).

## Utilizzo

```powershell
python src\generate_sample_pdf.py   # Fase 0 - crea il manuale di esempio
python src\parse_pdf.py             # Fase 1
python src\build_index.py           # Fase 2
python src\query_engine.py          # Fase 3
python src\benchmark.py             # Fase 4
```

### Usare un altro PDF

Il parser legge `data/sample_manual.pdf` per default. Per indicare un PDF diverso con la stessa struttura:

```powershell
python src\parse_pdf.py "percorso\manuale.pdf"
# oppure
$env:RAG_PDF_PATH = "percorso\manuale.pdf"; python src\parse_pdf.py
```

Marche e parole chiave riconosciute si configurano in `src/domain.py`.

## Formato di una soluzione (chunk)

| Campo | Descrizione |
|-------|-------------|
| `id` | Identificativo (`sol_013`) |
| `page` | Pagina PDF |
| `tripletta` | Categoria della richiesta |
| `note_standard` | Tipo intervento |
| `note` | Istruzioni operative |
| `script` | Testo da comunicare al cliente |
| `assegnazione` | Team a cui inoltrare la richiesta |
| `tempistiche` | Tempi di intervento (se presenti) |
| `path` | Percorso nell'albero decisionale |
| `marca` | Marca estratta da `note_standard` → `note` → `path` |

## Benchmark

Metodologia e risultati sul manuale di esempio in [Benchmark.md](Benchmark.md).

## Limitazioni note

- **Path euristico**: il percorso si ricostruisce prendendo la prima opzione di ogni pagina-domanda e si azzera sulla domanda radice; con layout diversi va adattato.
- **Embedding locale**: `bge-small-en-v1.5` è english-first; con `OPENAI_API_KEY` i risultati in italiano migliorano.
- **LLM opzionale**: senza OpenAI il sistema restituisce il contesto recuperato anziché una risposta sintetizzata.
