
from tools.fetch_filings import fetchData
from tools.conversion import filings_to_langchain_docs
from tools.vectorstore import get_vectorstore


### This agent fetches a spcific filing with specific date for a specific company a d interprets it
def retriever(state):
    """Retrives the specific SEC filing(s) required for answering user query"""
    query = state['query']
    filing_to_fetch = state["filing_to_fetch"]
    
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.25,
        "k": 5,
        "filter": {"form": filing_to_fetch}
    })
    
    retrieved_docs = retriever.invoke(query)
    return {"retrieved_docs": retrieved_docs}

    
        