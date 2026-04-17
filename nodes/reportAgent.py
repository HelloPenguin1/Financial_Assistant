from tools.fetch_filings import fetchData


class Report_Agent:
    def __init__(self):
        #Intialize the fetcher
        self.fetcher = fetchData()
    
    def Report_Agent(self, state):
        """This node fetches all 3 SEC filing types for each"""
        # Break it down retrieve filings
        filings = self.fetcher.fetch_filings(
            ticker=state["company"],
            form_type=["10-K", "10-Q", "8-k"],
            start_date=state["start_date"],
            end_date=state["end_date"]
        )
        
        