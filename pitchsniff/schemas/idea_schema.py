from pydantic import BaseModel, Field
from typing import List

class idea_summary_schema(BaseModel):
  problem: str = Field(description="Core Problem being solved")
  target_user: str = Field(description="Primary user or customer segment")
  solution: str = Field(description="Proposed solution or product")
  industry: str = Field(description="Industry or domain")
  assumptions: List[str] = Field(description="Key assumptions the idea relies on.")