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

def market_demand_agent(state: startup_evaluator_state):
  idea_summary = state["idea_summary"]

  prompt = f"""
You are a market research analyst.

Your task is to evaluate the MARKET POTENTIAL of a startup idea.

Rules:
- Base your analysis ONLY on the provided idea summary.
- Use reasonable industry heuristics when exact data is unavailable.
- Do NOT evaluate product originality or technical difficulty.
- Avoid optimism bias.

Score each metric from 0 to 10 and provide a brief justification.

Metrics:
1. market_size – Estimated total addressable market.
2. market_growth – Expected growth rate of the market.
3. customer_willingness_to_pay – Likelihood that customers will pay for this solution.

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