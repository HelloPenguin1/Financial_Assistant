from config.model_gateway import planner_llm, writer_llm
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import WorkerState, GraphState
from langgraph.types import Send
from prompts.orchestrator_prompt import orchestrator_system_prompt
from prompts.worker_prompt import worker_system_prompt
from tools.vectorstore import get_vectorstore


def orchestrator(state: GraphState):
    """Orchestrator that generates a plan for the report with 10-K and 10-Q sections.
    
    Returns section plans with filter_sections for metadata filtering in retriever.
    Each section includes 3-4 most financially significant items to retrieve from.
    """
    
    report_section = planner_llm.invoke(
        [
            SystemMessage(content=orchestrator_system_prompt),
            HumanMessage(content=f"""Create a financial analysis plan based on:
            - User Query: {state['query']}
            - Company: {state['company']}
            - Time Duration: {state['start_date']} to {state['end_date']}""")
        ]
    )
    
    return {"sections": report_section.sections}


def assign_workers(state: GraphState):
    return [
        Send(
            "llm_call",
            {
                "section": s,
            }
        )
        for s in state["sections"]
    ]
    


def llm_call(state: WorkerState):
    """Worker writes a section of the report"""
    section = state['section']
    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 5,  # Reduced from 5 to 2 to avoid token limits
            "filter": {
                "$and": [
                    {"form": section.filing_type},
                    {"section": {"$in": section.filter_sections}}
                ]
            }
        }
    )
    docs = retriever.invoke(section.retrieval_query)
    context = "\n\n".join([d.page_content for d in docs])
    
    response = writer_llm.invoke(
        [
            SystemMessage(content=worker_system_prompt),
            
            HumanMessage(content=f"""
                         Section: {section.name} \n\n
                         Objective: {section.generation_goal} \n\n
                         Context: 
                         {context}
                         
                         Task:
                        Extract only what is explicitly present. Do not interpret.
                         """)
        ]
        
    )
    # Write the updated section to completed sections
    #add the context to state under diff name than retrieved docs
    return {"completed_sections": [response.content]}  #save to state
    
    
def synthesizer(state: GraphState):
    completed_sections = state["completed_sections"]
    header = f"# Financial Analysis Report: {state['company']}\n*Period: {state['start_date']} – {state.get('end_date', 'Present')}*\n\n"
    body = "\n\n".join(completed_sections)
    return {"final_report": header + body}
    
    