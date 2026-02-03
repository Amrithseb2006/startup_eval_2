from pydantic import BaseModel, Field
from typing import Dict

class ParallelAgentOutput(BaseModel):
    metric_scores: Dict[str, float] = Field(
        description="Metric scores between 0 and 10"
    )
    metric_rationales: Dict[str, str] = Field(
        description="Justification for each metric score"
    )