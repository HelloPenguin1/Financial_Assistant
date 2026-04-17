from prompts.template import query_planner_prompt
from config.model_gateway import query_llm

def QueryDecomposer(state):
    """This node takes the user query and decides which company data/filings to retrieve"""
    chain = query_planner_prompt | query_llm
    output = chain.invoke({"question": state["query"]})
    return {
        "company":output.company,
        "filing_to_fetch":output.filing_to_fetch,
        "rationale": output.rationale
    }