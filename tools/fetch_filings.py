from edgar import *


class fetchData:
    def __init__(self):
        set_identity("dev@gmail.com")
        self.filings = ""
        self.company = ""
        
    def fetch_filings(self, ticker,form_type:list[str],period:str=None):
        self.company = Company(ticker)
        
        latest_duration = 1 if period == None or period in ("recent", "latest") else 3
        
        self.filings = self.company.get_filings(form=form_type).latest(latest_duration)
        return self.filings


#For Test
if __name__ == "__main__":
    
    fetcher = fetchData()
    filings = fetcher.fetch_filings("AAPL", ["10-K"],"past few years")
    print(filings)
    