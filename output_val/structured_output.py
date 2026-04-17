from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class queryDecompose(BaseModel):
    company: str
    start_date: str
    end_date: Optional[str] = None

    intent: Literal["full_report", "specific", "comparison"]
    rationale: str
    