from prompts.query_planner_prompt import query_planner_prompt
from config.model_gateway import query_llm

def QueryDecomposer(state):
    """This node takes the user query and decides which company data/filings to retrieve"""
    chain = query_planner_prompt | query_llm
    output = chain.invoke({"question": state["query"]})
    return {
        "company":output.company,
        "start_date": output.start_date,
        "end_date":output.end_date,
        "intent": output.intent,
        "rationale": output.rationale,
        "filing_to_fetch": output.filing_to_fetch
    }
    
