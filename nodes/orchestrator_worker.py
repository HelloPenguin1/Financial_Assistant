from config.model_gateway import planner_llm, writer_llm
from langchain_core.messages import SystemMessage, HumanMessage
from output_val.structured_output import Work
from graph.state import WorkerState, GraphState
from langgraph.types import Send    

def orchestrator(state: GraphState):
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


def assign_workers(state: GraphState):
    return [
        Send(
            "llm_call",
            {
                "section": s,
                 "vectorstore": state["vectorstore"]
            }
        )
        for s in state["sections"]
    ]
    


def llm_call(state: WorkerState, vectorstore):
    """Worker writes a section of the report"""
    section = state['section']
    
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k":5,
            "filter": {
                "form": section["filing_type"]
            }
        }
    )
    docs = retriever.invoke(section["retrieval_query"])
    context = "\n\n".join([d.page_content for d in docs])
    
    response = writer_llm.invoke(
        [
            SystemMessage(content="""
        You are a financial analyst.

        Write a precise analytical section using retrieved SEC filing data.

        Focus:
        - Extract signals, not generic summaries
        - Highlight changes, trends, anomalies
        - Be specific and data-driven
        - No introduction or conclusion
        - Output markdown"""),
            
            HumanMessage(content=f"""
                         Section: {section["name"]} \n\n
                         Objective: {section["generation_goal"]} \n\n
                         Context: 
                         {context}
                         """)
        ]
        
    )
    # Write the updated section to completed sections
    return {"completed_sections": [response.content]}  #save to state
    
    
def synthesizer(state: GraphState):
    completed_sections = state["completed_sections"]

    return {
        "final_report": "\n\n---\n\n".join(completed_sections)
    }
    

    
    