from typing_extensions import TypedDict
from typing import Optional, Literal, List, Any, Annotated
from langgraph.types import Send
from output_val.structured_output import Section
from langchain_core.vectorstores import VectorStore
import operator
from langchain_core.documents import Document


class GraphState(TypedDict):
    query: str
    
    #Query Decomposer Stage
    company: str
    start_date: Optional[str]
    end_date: Optional[str] = None
    intent: str
    
    filing_to_fetch: Optional[list[str]]
            
    
    #Full Report Workflow
    sections: list[Section] # list of report sections (after orchestrator)
    completed_sections: Annotated[
        list, operator.add   #all workers write to this key in parallel
    ]
    final_report: str #Final report
    
    
    #specific filing workflow
    retrieved_docs: List[Document]
    final_response: str #for specific query
    

# For Data Isolation, and parallelization
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[
        list, operator.add
    ]
    
    
    