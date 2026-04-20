from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class queryDecompose(BaseModel):
    """Structured output for Query Decomposer Layer"""
    company: str
    start_date: str
    end_date: Optional[str] = None

    intent: Literal["full_report", "specific", "comparison"]
    rationale: str
    filing_to_fetch: Optional[Literal["10-K", "10-Q"]] = None


# Structured Output for Full Audit Report

class Section(BaseModel):
    name: str = Field(description="Name of this section of the report")
    description: str = Field(description="Brief overview of the main financial indicators and concepts to be covered in this section")
    filing_type: Literal["10-K", "10-Q", "8-K"] = Field(description="Each section focuses on one of 3 SEC filing types")
    retrieval_query: str = Field(description="Retrieval query optimized for semantic search to retrieve important financial indicators for the particular secion")
    generation_goal: str = Field(description="The goal of generated content in this section")
    
    #For metadata filtering

    filter_sections: List[str] = Field(description="Filtered sections to retrieve per SEC filing")

class Sections(BaseModel):
    sections: List[Section] = Field(description=" Three Sections of the financial analysis report, covering 10-K, 10-Q, and 8-K")
    


