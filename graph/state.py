from typing_extensions import TypedDict
from typing import Optional, Literal, List, Any

class GraphState(TypedDict):
    query: str
    
    #Query Decomposer Stage
    company: str
    
    start_date: str
    end_date: str
    
    intent: str
    
    
    
    
    