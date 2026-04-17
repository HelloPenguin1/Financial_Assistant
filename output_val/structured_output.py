from pydantic import BaseModel, Field
from typing import Literal, List

class queryDecompose(BaseModel):
    company: str
    filing_to_fetch: Literal["10-K", "10-Q", "8-k"]
    rationale: str = Field(description="The reasoning behind filing to fetch")