"""
LLM-powered bullet point rewriting using LangChain + Groq.

Takes a weak resume bullet (flagged by quality.py) and asks an LLM to
rewrite it with a stronger verb and clearer impact framing.

Uses LangChain's ChatGroq integration rather than the raw groq SDK -
this keeps the implementation swappable to other LangChain-supported
providers later (OpenAI, Anthropic, etc.) with minimal code changes.

Requires a GROQ_API_KEY environment variable to be set - never hardcode
the key directly in this file. Reads it from a .env file if present.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables from a .env file in the project root,
# if one exists. This lets GROQ_API_KEY be set once in .env instead
# of needing `export GROQ_API_KEY=...` in every terminal session.
load_dotenv()

# Model choice: llama-3.1-8b-instant is fast and free-tier friendly,
# a good fit for a quick single-bullet rewrite task.
MODEL_NAME = "llama-3.1-8b-instant"

REWRITE_SYSTEM_PROMPT = (
    "You are a professional resume writer. Rewrite the given resume "
    "bullet point to be more impactful: use a strong action verb, and "
    "if a metric/number is missing and can be reasonably implied, "
    "suggest where one could go using a bracketed placeholder like "
    "[X%] - do not invent a fake specific number. Keep it to ONE "
    "sentence, no longer than the original. Return ONLY the rewritten "
    "bullet point text, nothing else - no preamble, no quotes, no "
    "explanation."
)


def get_llm():
    """
    Create a LangChain ChatGroq client using the API key from the
    environment. Raises a clear error if the key isn't set, rather
    than letting LangChain fail with a less helpful message later.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set. "
            "Set it in a .env file before running the app (see README)."
        )

    return ChatGroq(
        model_name=MODEL_NAME,
        groq_api_key=api_key,
        temperature=0.4,
        max_tokens=150,
    )


def rewrite_bullet(bullet_text):
    """
    Send a single bullet point to the LLM (via LangChain) and return
    the rewritten version.

    Returns the rewritten text as a string. Raises an exception on
    API failure - the caller (app.py) is responsible for catching
    this and showing a user-friendly message.
    """
    llm = get_llm()

    # Strip leading bullet markers before sending, so the LLM doesn't
    # try to "rewrite" a stray "-" or "•" character.
    cleaned = bullet_text.strip().lstrip("-*•").strip()

    messages = [
        SystemMessage(content=REWRITE_SYSTEM_PROMPT),
        HumanMessage(content=cleaned),
    ]

    response = llm.invoke(messages)
    return response.content.strip()