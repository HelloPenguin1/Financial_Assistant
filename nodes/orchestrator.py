from config.model_gateway import planner_llm
from langchain_core.messages import SystemMessage, HumanMessage


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

        Return STRICT JSON:
        {
        "sections": [...]
        }

        Constraints:
        - Exactly 3 sections
        - No overlap between sections
        - Queries must target financial signals"""),
        HumanMessage(content=f"User Query: {state['query']}, ")
            
        ]
    )
    