"""
Orchestrates: detect intent -> run tool or RAG -> call LLM -> return response.
"""
import json
from pathlib import Path

from portfolio_ask import rag, llm, tools
from portfolio_ask.models import GeneralResponse

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_portfolio() -> list[dict]:
    path = DATA_DIR / "portfolio.json"
    return json.loads(path.read_text())["holdings"]


def _detect_intent(query: str) -> str:
    """
    Simple keyword-based intent detection.
    Returns: 'pnl' | 'allocation' | 'general'
    """
    q = query.lower()
    if any(w in q for w in ["p&l", "pnl", "profit", "loss", "return", "gain"]):
        return "pnl"
    if any(w in q for w in ["sector", "allocation", "weight", "breakdown", "diversif", "invested"]):
        return "allocation"
    return "general"


def answer(query: str) -> dict:
    """Main entry point. Returns a dict ready to print as JSON."""
    rag.build_index()

    intent = _detect_intent(query)
    holdings = _load_portfolio()

    # --- Tool-use path (structured output, no LLM for math) ---
    if intent == "pnl":
        result = tools.compute_pnl(holdings)
        return result.model_dump()

    if intent == "allocation":
        result = tools.compute_sector_allocation(holdings)
        return result.model_dump()

    # --- RAG + LLM path (general / news questions) ---
    chunks = rag.retrieve(query, top_k=5)
    context = "\n\n".join(f"[{c['source']}] {c['text']}" for c in chunks)
    sources = list(dict.fromkeys(c["source"] for c in chunks))  # deduplicated, order-preserving

    system = (
        "You are a financial assistant. Answer using ONLY the context provided. "
        "Be concise. Do not make up numbers or facts not present in the context."
    )
    user = f"Context:\n{context}\n\nQuestion: {query}"

    answer_text = llm.ask(system, user)
    result = GeneralResponse(answer=answer_text, sources=sources)
    return result.model_dump()
