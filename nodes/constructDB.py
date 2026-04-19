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
    
        if state["intent"]=='full_report':
            filings = self.fetcher.fetch_latest_filings(ticker=state["company"])
            filings = [f for f in filings.values() if f is not None]
            
        else: #if intent is specific
            filings = self.fetcher.fetch_filings(
            ticker=state["company"],
            form_type=state['filing_to_fetch'],
            start_date=state["start_date"],
            end_date=state["end_date"])
            
        filings = list(filings)
    
        chunks = filings_to_langchain_docs(filings=filings, ticker=state["company"])
        vectordb = vectordb_store(chunks)
        
        return {"vectorstore": vectordb}

    
        

