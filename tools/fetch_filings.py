from edgar import *


class fetchData:
    def __init__(self):
        set_identity("dev@gmail.com")
        self.filings = ""
        self.company = ""
    
    
    #triggers if intent is specific
    def fetch_filings(self, ticker:str,form_type:list[str],start_date:str, end_date:str=None):
        """This function fetches SEC filings and return filing objects"""
                    
        self.company = Company(ticker)
        start = f"{start_date}-01-01"
        end = f"{end_date}-01-01" if end_date is not None else ""
        final_date = f"{start}:{end}"
        self.filings = self.company.get_filings(form=form_type,
                                                date=final_date)
        return self.filings
    
    
    
    #For full report
    def fetch_latest_filings(self, ticker: str):
        self.company = Company(ticker)

        return {
            "10-K": self.company.get_filings(form="10-K", amendments=False).latest(),
            "10-Q": self.company.get_filings(form="10-Q", amendments=False).latest(),
            "8-K":  self.company.get_filings(form="8-K", amendments=False).latest()
        }
        
        

#For Test
if __name__ == "__main__":
    
    fetcher = fetchData()
    filings = fetcher.fetch_filings(
        ticker="AAPL",
        form_type="10-K",
        start_date="2020",
        end_date="2024"
    )
    print(filings)
    