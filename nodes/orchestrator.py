from config.model_gateway import planner_llm
from langchain_core.messages import SystemMessage, HumanMessage
from output_val.structured_output import Work
from graph.state import WorkerState

def orchestrator(state):
    """Orchestrator that generates a plan for the report"""
    report_section = planner_llm.invoke(
        [
            SystemMessage(content="""
        You are a financial planning agent.

        Decompose the user query into exactly 3 sections, one per SEC filing type:

        - 10-K → long-term fundamentals, risks, strategy
        - 10-Q → recent financial performance and trends
        - 8-K → material events and announcements

        For each section, output:
        - name
        - description
        - filing_type
        - retrieval_query (optimized for semantic search, not a question)
        - filters (must include form)
        - generation_goal

        Constraints:
        - Exactly 3 sections
        - No overlap between sections
        - Queries must target financial signals"""),
        HumanMessage(content=f"""Use these information for report. 
                     User Query: {state['query']}, 
                     Company: {state['company']}, 
                     Time Duration: {state['start_date']} to {state['end_date']}""")
        ]
    )
    
    return {"sections": report_section.sections}



def llm_call(state: WorkerState, vectorstore):
    """Worker writes a section of the report"""
    section = state['section']
    
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k":5,
            #"filter": section['filters'] ##look into it later. maybe modify output_val for planner to output sectiosn
        }
    )
    docs = retriever.invoke(section[""])
    
    
    
    