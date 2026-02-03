from typing import TypedDict, Dict, Any, List, Optional
from typing import Annotated

def merge_dicts(a: Dict, b: Dict) -> Dict:
    return {**a, **b}


class startup_evaluator_state(TypedDict):
  raw_idea : str
  idea_summary : Dict[str,Any]
  metric_scores : Annotated[Dict[str,float],merge_dicts]
  metric_rationales : Annotated[Dict[str,str],merge_dicts]
  final_score : Optional[float]
  swot_input : Optional[Dict[str,Any]]
  swot_analysis : Optional[Dict[str,List[str]]]

