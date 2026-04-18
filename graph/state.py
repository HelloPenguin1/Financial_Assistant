from typing_extensions import TypedDict
from typing import Optional, Literal, List, Any, Annotated
from langgraph.types import Send
from output_val.structured_output import Section
import operator

class GraphState(TypedDict):
    query: str
    
    #Query Decomposer Stage
    company: str
    start_date: str
    end_date: str
    intent: str
    
    #Full Report Workflow
    sections: list[Section] # list of report sections (after orchestrator)
    completed_sections: Annotated[
        list, operator.add   #all workers write to this key in parallel
    ]
    final_report: str #Final report
    

# For Data Isolation, and parallelization
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[
        list, operator.add
    ]
    
    
    