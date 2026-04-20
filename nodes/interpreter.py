from tools.vectorstore import get_vectorstore
from langchain_core.messages import SystemMessage, HumanMessage
from config.model_gateway import writer_llm


### This agent fetches a spcific filing with specific date for a specific company a d interprets it
def retriever(state):
    """Retrives the specific SEC filing(s) required for answering user query"""
    query = state['query']
    filing_to_fetch = state["filing_to_fetch"]
    
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {"form": filing_to_fetch}
    })
    
    retrieved_docs = retriever.invoke(query)
    return {"retrieved_docs": retrieved_docs}


## Answer generation
def llm_response(state):
    query = state['query']
    retrieved_docs = state.get("retrieved_docs")
    print("DOC COUNT:", len(retrieved_docs))
    filing_used = state["filing_to_fetch"]
    company = state["company"]
    context = "\n\n".join([d.page_content for d in retrieved_docs])
    
    final_response = writer_llm.invoke(
        [
            SystemMessage(content="""
        You are a financial assistant analyzing SEC filings (10-K, 10-Q, 8-K).

        Answer the user’s question using ONLY the provided context.

        Guidelines:
        - Focus on what the question is asking. Do not summarize everything.
        - Extract relevant financial details (metrics, trends, risks, or management commentary).
        - Be clear and concise.
        - If specific numbers or statements are present, include them.
        - Do not add outside knowledge or assumptions.
        - If the context does not contain enough information, say so.

        Format:
        Start with a direct answer, then briefly support it using points from the context.                          
            """),
            HumanMessage(content=f"""
            User Query: {query}
            Company: {company}
            Context: {context}
            Filing from each retrived context originates from: {filing_used}
            
            Your synthesized response to the question based on the context retrieved.     
            Output: 
            
            Note: Provide citation. For example under references subheading put: Source: 10-K, Section 1, Company: AAPL
            """)
        ]
    )
    return {"final_response": final_response}