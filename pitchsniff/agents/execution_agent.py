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

def execution_feasibility_agent(state:startup_evaluator_state):
  idea_summary = state["idea_summary"]

  prompt = f"""You are a startup execution and operations analyst.

Your task is to evaluate how FEASIBLE it is to build and scale this startup.

Rules:
- Assume a small but competent founding team.
- Do NOT evaluate market size or originality.
- Consider infrastructure, talent, and operational complexity.
- Higher scores mean easier execution.

Score each metric from 0 to 10 and provide a brief justification.

Metrics:
1. execution_complexity – Difficulty of building the product.
2. cost_feasibility – Likelihood of building sustainably at reasonable cost.
3. scalability – Ability to scale without proportional cost increase.

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