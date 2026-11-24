from typing import Any
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess_text


def compute_trace_links(
    requirements: list[dict[str, str]],
    codebase: dict[str, str],
    threshold: float = 0.08,
) -> pd.DataFrame:
    """Compute ranked TF-IDF cosine similarity links between requirements and code files."""
    req_ids = [r["id"] for r in requirements]
    req_texts_raw = [r["text"] for r in requirements]
    req_texts_clean = [preprocess_text(t) for t in req_texts_raw]

    file_names = list(codebase.keys())
    code_texts_clean = [preprocess_text(codebase[f]) for f in file_names]

    # Fit TF-IDF on combined corpus so IDF weights reflect both requirements and code
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectorizer.fit(req_texts_clean + code_texts_clean)

    req_matrix = vectorizer.transform(req_texts_clean)
    code_matrix = vectorizer.transform(code_texts_clean)

    # Shape: (num_requirements, num_code_files)
    sim_matrix = cosine_similarity(req_matrix, code_matrix)

    rows: list[dict[str, Any]] = []
    for i, req_id in enumerate(req_ids):
        ranked_indices = sorted(
            range(len(file_names)),
            key=lambda j: sim_matrix[i][j],
            reverse=True,
        )
        for rank, j in enumerate(ranked_indices, start=1):
            score = float(sim_matrix[i][j])
            rows.append(
                {
                    "requirement_id": req_id,
                    "requirement_text": req_texts_raw[i],
                    "code_file": file_names[j],
                    "similarity_score": round(score, 4),
                    "rank": rank,
                    "predicted_link": score >= threshold,
                }
            )

    return pd.DataFrame(rows)
