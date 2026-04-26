# Ask Your Portfolio

A CLI tool to ask natural language questions about your investment portfolio — powered by RAG (FAISS + sentence-transformers) and Ollama (local LLM).

## Setup

```bash
# 1. Install Python dependencies
make install

# 2. Start Ollama (in a separate terminal)
ollama serve

# 3. Pull the LLM model (one-time)
ollama pull llama3
```

## Usage

```bash
# P&L query (uses compute_pnl tool — no LLM math)
python -m portfolio_ask "What is my P&L?"

# Sector allocation (uses compute_sector_allocation tool)
python -m portfolio_ask "Show my sector allocation"

# General / news questions (uses RAG + Ollama)
python -m portfolio_ask "What is EBITDA?"
python -m portfolio_ask "What's the outlook for pharma stocks?"
```

Or with Make:
```bash
make ask Q="What is my profit?"
```

## Run Evals

```bash
make eval
```

## Project Structure

```
portfolio_ask/
├── portfolio_ask/
│   ├── __main__.py     # CLI entry point
│   ├── main.py         # Orchestrator (intent → tools or RAG → LLM)
│   ├── rag.py          # Chunking, embedding, FAISS retrieval
│   ├── llm.py          # Ollama wrapper
│   ├── tools.py        # compute_pnl, compute_sector_allocation
│   └── models.py       # Pydantic output schemas
├── data/
│   ├── portfolio.json  # Your holdings
│   ├── glossary.md     # Finance glossary
│   └── news/           # Market news markdown files
├── evals/
│   ├── cases.yaml      # 5 test cases
│   └── run_evals.py    # Eval runner
├── requirements.txt
└── Makefile
```

## Design Decisions

| Decision | Why |
|---|---|
| Keyword intent detection | Simple, transparent, no LLM cost for routing |
| Python tools for math | LLMs hallucinate numbers — functions don't |
| Pydantic structured output | Type-safe, self-documenting, testable |
| FAISS IndexFlatL2 | Exact search, fine for small document sets |
| Ollama (local LLM) | No API keys, runs fully offline |
