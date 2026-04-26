"""
RAG pipeline: chunk documents -> embed -> store in FAISS -> retrieve top-k.
No framework magic — just sentence-transformers + faiss.
"""
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = Path(__file__).parent.parent / "data"
_model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory store: parallel lists (chunks + metadata)
_chunks: list[str] = []
_sources: list[str] = []
_index = None

class NumpyIndex:
    def __init__(self, dim):
        self.dim = dim
        self.embeddings = None

    def add(self, x):
        if self.embeddings is None:
            self.embeddings = np.array(x, dtype="float32")
        else:
            self.embeddings = np.vstack((self.embeddings, np.array(x, dtype="float32")))

    def search(self, q, k):
        all_dists = []
        all_indices = []
        for query_vec in q:
            # L2 squared distance
            diff = self.embeddings - query_vec
            dists = np.sum(diff**2, axis=1)
            idx = np.argsort(dists)[:k]
            all_dists.append(dists[idx])
            all_indices.append(idx)
        return np.array(all_dists), np.array(all_indices)


def _load_documents() -> list[tuple[str, str]]:
    """Return (text, source) pairs from all data files."""
    docs = []

    # Portfolio JSON -> one chunk per holding
    portfolio_path = DATA_DIR / "portfolio.json"
    if portfolio_path.exists():
        data = json.loads(portfolio_path.read_text())
        for h in data["holdings"]:
            text = (
                f"{h['name']} ({h['ticker']}) | Sector: {h['sector']} | "
                f"Qty: {h['quantity']} | Avg Cost: {h['avg_cost']} | "
                f"Current Price: {h['current_price']}"
            )
            docs.append((text, "portfolio.json"))

    # Glossary -> split by lines (simple chunking)
    glossary_path = DATA_DIR / "glossary.md"
    if glossary_path.exists():
        for line in glossary_path.read_text().splitlines():
            line = line.strip()
            if len(line) > 20:
                docs.append((line, "glossary.md"))

    # News markdown files
    news_dir = DATA_DIR / "news"
    if news_dir.exists():
        for md_file in sorted(news_dir.glob("*.md")):
            text = md_file.read_text().strip()
            # Chunk by paragraph (split on blank lines)
            paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
            for para in paragraphs:
                docs.append((para, md_file.name))

    return docs


def build_index() -> None:
    """Build FAISS index from all documents. Called once at startup."""
    global _chunks, _sources, _index

    docs = _load_documents()
    if not docs:
        raise ValueError("No documents found in data/")

    texts, srcs = zip(*docs)
    _chunks = list(texts)
    _sources = list(srcs)

    embeddings = _model.encode(_chunks, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype="float32")

    dim = embeddings.shape[1]
    _index = NumpyIndex(dim)
    _index.add(embeddings)


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Return top-k relevant chunks with their source filenames."""
    if _index is None:
        raise RuntimeError("Call build_index() before retrieve()")

    query_vec = _model.encode([query], show_progress_bar=False)
    query_vec = np.array(query_vec, dtype="float32")

    _, indices = _index.search(query_vec, top_k)
    results = []
    for i in indices[0]:
        if i < len(_chunks):
            results.append({"text": _chunks[i], "source": _sources[i]})
    return results
