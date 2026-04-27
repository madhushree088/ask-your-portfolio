# AI Usage Log

## Tools Used
- Ollama (for running local LLM)
- ChatGPT (for guidance, debugging, and code structuring)

## How AI Was Used
- Used Ollama to generate responses for user queries in the CLI application
- Helped design the overall system flow (tool usage + RAG + LLM)
- Assisted in writing initial code for:
  - P&L computation function
  - Basic retrieval logic (RAG)
  - Prompt design for LLM responses
- Used for debugging and improving code clarity

## What I Did Myself
- Set up and ran the local LLM using Ollama
- Integrated LLM with the CLI application
- Implemented tool-based computation for P&L instead of relying on LLM
- Built the retrieval logic to fetch relevant data from local files
- Created and structured the dataset (portfolio, news, glossary)
- Tested the system with multiple queries and verified outputs

## Validation Results
- **Intent Routing**: Verified that queries containing "pnl" or "profit" correctly route to the `pnl` tool.
- **Data Integrity**: Confirmed that the deterministic tools in [tools.py](file:///c:/Users/madhu/Downloads/portfolio_ask%20(1)/portfolio_ask/portfolio_ask/tools.py) correctly handle the `portfolio.json` structure.
- **Environment**: Verified that the system is set up to run with `sentence-transformers` and `faiss-cpu`.
- **Evaluation Suite**: Ran `evals/run_evals.py` with 4/5 cases passing. Tool-based queries (P&L, Allocation) passed successfully. The RAG/LLM path failed due to environment memory constraints (Ollama requiring 4.6GB), confirming the system's reliance on local LLM availability.

## Notes
AI was used as a development assistant. All generated code and outputs were reviewed, tested, and modified before inclusion. The system prioritizes deterministic tool-based computation for accuracy and uses LLM only for explanation and natural language responses.
