import re
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do",
    "for", "from", "has", "have", "in", "into", "is", "it", "its",
    "of", "on", "or", "so", "that", "the", "their", "them", "this",
    "to", "up", "use", "using", "val", "var", "fun", "class", "private",
    "suspend", "return", "with",
}


def split_identifiers(text: str) -> str:
    """Split camelCase, PascalCase, snake_case, and hyphen-separated tokens."""
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    text = re.sub(r"[_-]+", " ", text)
    return text


def preprocess_text(text: str, remove_stopwords: bool = True) -> str:
    """Clean a requirement or source code string into space-separated tokens."""
    expanded = split_identifiers(text).lower()
    tokens = re.findall(r"[a-z]{2,}", expanded)
    if remove_stopwords:
        tokens = [tok for tok in tokens if tok not in STOPWORDS]
    return " ".join(tokens)


def load_codebase(codebase_dir: Path) -> dict[str, str]:
    """Load all source files in codebase_dir as {filename: raw_content}."""
    artifacts: dict[str, str] = {}
    for path in sorted(codebase_dir.iterdir()):
        if path.is_file():
            artifacts[path.name] = path.read_text(encoding="utf-8")
    return artifacts
