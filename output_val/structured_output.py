from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class queryDecompose(BaseModel):
    """Structured output for Query Decomposer Layer"""
    company: str
    start_date: str
    end_date: Optional[str] = None

    intent: Literal["full_report", "specific", "comparison"]
    rationale: str

# Structured Output for Parallel Writers
