"""
Thin wrapper around Ollama. Keeps all LLM calls in one place.
Requires: ollama serve (running locally) + ollama pull llama3
"""
import ollama


def ask(system_prompt: str, user_prompt: str, model: str = "llama3") -> str:
    """Send a prompt to Ollama and return the text response."""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response["message"]["content"].strip()
