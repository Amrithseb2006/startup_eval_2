from pydantic import BaseModel, Field
from typing import List

class SWOTAnalysisOutput(BaseModel):
    strengths: List[str] = Field(
        description="Internal advantages of the startup"
    )
    weaknesses: List[str] = Field(
        description="Internal limitations or gaps"
    )
    opportunities: List[str] = Field(
        description="External factors the startup can leverage"
    )
    threats: List[str] = Field(
        description="External risks or competitive pressures"
    )
