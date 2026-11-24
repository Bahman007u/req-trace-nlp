from typing import Any
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess_text


def compute_semantic_trace_links(
    requirements: list[dict[str, str]],
    codebase: dict[str, str],
    threshold: float = 0.25,
    model_name: str = "all-MiniLM-L6-v2",
) -> pd.DataFrame:
    model = SentenceTransformer(model_name)

    req_ids = [r["id"] for r in requirements]
    req_texts_raw = [r["text"] for r in requirements]
    req_texts_clean = [preprocess_text(t) for t in req_texts_raw]

    file_names = list(codebase.keys())
    code_texts_clean = [preprocess_text(codebase[f]) for f in file_names]

    req_embeddings = model.encode(req_texts_clean, normalize_embeddings=True)
    code_embeddings = model.encode(code_texts_clean, normalize_embeddings=True)

    sim_matrix = cosine_similarity(req_embeddings, code_embeddings)

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
