from  state.startup_state import startup_evaluator_state

def final_score_aggregation(state:startup_evaluator_state):
  scores = state["metric_scores"]

  weights = {
        "originality": 0.1,
        "problem_solution_fit": 0.1,
        "differentiation": 0.1,
        "market_size": 0.15,
        "market_growth": 0.1,
        "customer_willingness_to_pay": 0.1,
        "defensibility": 0.1,
        "switching_costs": 0.05,
        "execution_complexity": 0.1,
        "scalability": 0.1,
  }

  weighted_sum = sum(
      scores[k] * weights.get(k,0) for k in scores
  )

  final_score = round(weighted_sum*10,2)

  return {
      "final_score" : final_score,
      "swot_input" : {
            "idea_summary": state["idea_summary"],
            "metric_scores": scores,
            "metric_rationales": state["metric_rationales"],
            "final_score": final_score
      }
  }