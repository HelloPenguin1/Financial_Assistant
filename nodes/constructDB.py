from tools.fetch_filings import fetchData
from tools.conversion import filings_to_langchain_docs
from tools.vectorstore import vectordb_store

class Construct_DB:
    def __init__(self):
        #Intialize the fetcher
        self.fetcher = fetchData()
    
    def build_vectordb(self, state):
        """This node fetches all 3 SEC filing types for each, converts to Langchain docs, ingests into vectordb
        
        """
        # Break it down retrieve filings
        filings = self.fetcher.fetch_filings(
            ticker=state["company"],
            form_type=["10-K", "10-Q", "8-K"],
            start_date=state["start_date"],
            end_date=state["end_date"]
        )
        chunks = filings_to_langchain_docs(filings, state["company"])
        vectordb = vectordb_store(chunks)
        
        return {"vectorstore": vectordb}

    
        

