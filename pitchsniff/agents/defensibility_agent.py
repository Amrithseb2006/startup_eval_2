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

def defense_moat_agent(state: startup_evaluator_state):
  idea_summary = state["idea_summary"]

  prompt = f"""
You are a competitive strategy analyst.

Your task is to evaluate how DEFENSIBLE a startup idea is.

Rules:
- Assume competitors are rational and well-funded.
- Do NOT assume patents or proprietary data unless stated.
- Focus on long-term competitive advantage.
- Higher scores mean stronger defensibility.

Score each metric from 0 to 10 and provide a brief justification.

Metrics:
1. ease_of_duplication – How difficult is it for competitors to copy this?
2. defensibility – Strength of long-term competitive moat.
3. switching_costs – Difficulty for users to switch away once adopted.

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