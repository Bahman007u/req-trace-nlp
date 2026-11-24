# Requirements Traceability Prototype (NLP)

A lightweight Python prototype for automated **trace link recovery** between natural-language software requirements and source code artifacts using text preprocessing, TF-IDF vectorization, dense sentence embeddings, and cosine similarity.

---

## Project Structure

```text
req-trace-nlp/
├── data/
│   ├── codebase/                  # Sample Kotlin source files
│   ├── ground_truth.json          # Verified requirement-to-code mappings
│   └── requirements.json          # High-level functional requirements
├── outputs/
│   └── traceability_matrix.csv    # Generated candidate links & evaluation flags
├── src/
│   ├── preprocess.py              # Identifier splitting, cleaning, and code loader
│   ├── linker.py                  # TF-IDF + cosine similarity link recovery
│   ├── semantic_linker.py         # Sentence-embedding semantic similarity linker
│   └── evaluate.py                # Precision, Recall, F1 evaluation & CSV export
├── .gitignore
├── README.md
└── requirements.txt