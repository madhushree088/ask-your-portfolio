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

## Validation
- Verified that P&L calculations are done using Python logic (not LLM)
- Checked that retrieval returns relevant context
- Ensured system behaves correctly for both tool-based and LLM-based queries

## Notes
AI was used as a development assistant. All generated code and outputs were reviewed, tested, and modified before inclusion. The system prioritizes deterministic tool-based computation for accuracy and uses LLM only for explanation and natural language responses.