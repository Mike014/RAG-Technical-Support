# Benchmark

Risultati ottenuti sul **manuale demo fittizio** (`data/sample_manual.pdf`). I numeri servono a verificare che la pipeline funzioni. Per rigenerarli: `python src/benchmark.py`.

## Metodologia

| Aspetto | Dettaglio |
|---------|-----------|
| Dataset | `data/golden_queries.json`: 8 query golden |
| Iterazioni | 3 per query, quindi **24 test** |
| Accuratezza | Valutata sul **top chunk** (`sources[0]`), non sull'intera risposta |
| Latenza | Tempo della singola query (`query_with_metadata`), **escluso** il caricamento dei modelli |
| Percentili | P95 su n=24; P99 non riportato (campione troppo piccolo) |
| Varianza | Std dev **tra query** distinta dalla varianza **intra-query** |

## Configurazione

| Parametro | Valore |
|-----------|--------|
| Embedding | HuggingFace `BAAI/bge-small-en-v1.5` (locale, CPU) |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| LLM | Non configurato (solo retrieval) |
| Retrieval | top-5 → rerank → top-3 |
| Chunk indicizzati | 16 |

## Risultati (manuale demo)

| Metrica | Valore |
|---------|--------|
| Latenza media | 362.92 ms |
| Latenza mediana | 323.12 ms |
| Latenza P95 | 717.25 ms |
| Fonti medie | 3.0 |
| Accuratezza tripletta | 100.0% |
| Accuratezza assegnazione | 87.5% |
| Accuratezza marca | 100.0% |
| **Accuratezza overall** | **87.5%** |

La prima iterazione di ogni query paga il warm-up del reranker: per questo P95 e varianza intra-query risultano alti rispetto alla mediana.

## Output

- `output/benchmark_report.json`: metriche aggregate e risultati per singolo test
- `output/benchmark_plot.png`: latenza per query, distribuzione delle latenze, accuratezza, top score
