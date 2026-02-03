from  state.startup_state import startup_evaluator_state
from  schemas.idea_schema import idea_summary_schema
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    # other params...
)

def idea_parser_node(state: startup_evaluator_state):
    startup_idea = state["raw_idea"]

    prompt = f"""
You are an analyst whose only task is to extract and normalize a startup idea.

Rules:
- Do NOT evaluate, score, judge, or improve the idea.
- Do NOT suggest alternatives or opinions.
- Do NOT add information not explicitly stated or logically implied.

Convert the following startup idea into a structured, factual summary:

Startup Idea:
{startup_idea}
"""

    structured_llm = llm.with_structured_output(idea_summary_schema)
    result = structured_llm.invoke(prompt)

    return {
        "idea_summary": result.model_dump()
    }