from  state.startup_state import startup_evaluator_state
from  schemas.swot_schema import SWOTAnalysisOutput
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

def swot_analysis_agent(state: startup_evaluator_state):
    structured_llm = llm.with_structured_output(SWOTAnalysisOutput)

    result = structured_llm.invoke(
        f"""
You are a startup strategy analyst.

Generate a SWOT analysis using the evaluation data below.

Rules:
- Do NOT rescore or recompute metrics.
- Do NOT introduce new facts.
- Be concise and specific.
- Output exactly four lists: strengths, weaknesses, opportunities, threats.

Evaluation Data:
{state["swot_input"]}
"""
    )

    return {
        "swot_analysis": result.model_dump()
    }