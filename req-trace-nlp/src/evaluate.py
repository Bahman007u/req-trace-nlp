import json
from pathlib import Path
import pandas as pd

from linker import compute_trace_links
from preprocess import load_codebase


def evaluate_trace_links(
    links_df: pd.DataFrame,
    ground_truth: dict[str, list[str]],
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Attach ground-truth labels to candidate links and compute Precision, Recall, and F1."""
    evaluated_df = links_df.copy()
    evaluated_df["actual_link"] = evaluated_df.apply(
        lambda row: row["code_file"] in ground_truth.get(row["requirement_id"], []),
        axis=1,
    )

    tp = int(((evaluated_df["predicted_link"]) & (evaluated_df["actual_link"])).sum())
    fp = int(((evaluated_df["predicted_link"]) & (~evaluated_df["actual_link"])).sum())
    fn = int(((~evaluated_df["predicted_link"]) & (evaluated_df["actual_link"])).sum())

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    metrics = {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
    }
    return evaluated_df, metrics


def run_pipeline(
    base_dir: Path = Path("req-trace-nlp"),
    threshold: float = 0.08,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Run end-to-end trace link recovery, evaluation, and CSV export."""
    requirements = json.loads(
        (base_dir / "data" / "requirements.json").read_text(encoding="utf-8")
    )
    ground_truth = json.loads(
        (base_dir / "data" / "ground_truth.json").read_text(encoding="utf-8")
    )
    codebase = load_codebase(base_dir / "data" / "codebase")

    links_df = compute_trace_links(requirements, codebase, threshold=threshold)
    evaluated_df, metrics = evaluate_trace_links(links_df, ground_truth)

    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "traceability_matrix.csv"
    evaluated_df.to_csv(csv_path, index=False)

    return evaluated_df, metrics
