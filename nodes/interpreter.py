
from tools.fetch_filings import fetchData
from tools.conversion import filings_to_langchain_docs
from tools.vectorstore import get_vectorstore


### This agent fetches a spcific filing with specific date for a specific company a d interprets it


def retriever(state):
    """Retrives the specific SEC filing(s) required for answering user query"""
    
    
    vectorstore = get_vectorstore()
    
    
    
    
    return {"final": "test"}

    
        