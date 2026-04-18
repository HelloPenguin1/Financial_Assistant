from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class queryDecompose(BaseModel):
    """Structured output for Query Decomposer Layer"""
    company: str
    start_date: str
    end_date: Optional[str] = None

    intent: Literal["full_report", "specific", "comparison"]
    rationale: str


# Structured Output for Full Audit Report

class Section(BaseModel):
    name: str = Field(description="Name of this section of the report")
    description: str = Field(description="Brief overview of the main financial indicators and concepts to be covered in this section")
    

class Sections(BaseModel):
    sections: List[Section] = Field(description="Sections of the financial analysis report, covering 10-K, 10-Q, and 8-K")
    


