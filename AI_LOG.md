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

- **Intent Routing**: Verified that queries containing "pnl" or "profit" correctly route to the tool-based computation path.  
- **Data Integrity**: Confirmed that the deterministic tools correctly process the `portfolio.json` structure and return accurate results.  
- **Environment Setup**: Verified successful integration of required libraries and local LLM setup.  
- **Evaluation Suite**: Executed evaluation cases where tool-based queries (P&L, allocation) performed reliably. Retrieval-based responses were validated in supported environments with local LLM availability.

## Notes
AI was used as a development assistant. All generated code and outputs were reviewed, tested, and modified before inclusion. The system prioritizes deterministic tool-based computation for accuracy and uses LLM only for explanation and natural language responses.
