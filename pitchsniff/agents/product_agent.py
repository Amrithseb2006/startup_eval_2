from  state.startup_state import startup_evaluator_state
from  schemas.parallel_agent_schema import ParallelAgentOutput
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

def product_originality_agent(state: startup_evaluator_state):
    idea_summary = state["idea_summary"]

    prompt = f"""
You are a startup product analyst.

Your task is to evaluate the PRODUCT QUALITY and ORIGINALITY of a startup idea.

Rules:
- Base your analysis ONLY on the provided idea summary.
- Do NOT evaluate market size, cost, or execution feasibility.
- Do NOT assume proprietary data unless explicitly stated.
- Be critical but fair.

Score each metric from 0 to 10 and provide a brief justification.

Metrics:
1. originality – How novel or unique is the idea?
2. problem_solution_fit – How well does the solution address the stated problem?
3. differentiation – How clearly differentiated is this from existing solutions?

Startup Idea Summary:
{idea_summary}

Return your response strictly in the structured format.
"""

    structured_llm = llm.with_structured_output(ParallelAgentOutput)
    result = structured_llm.invoke(prompt)

    return {
        "metric_scores": result.metric_scores,
        "metric_rationales": result.metric_rationales
    }