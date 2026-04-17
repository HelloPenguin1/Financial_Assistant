from edgar import *


class fetchData:
    def __init__(self):
        set_identity("dev@gmail.com")
        self.filings = ""
        self.company = ""
        
    # def fetch_filings(self, ticker,form_type:list[str],period:str=None):
    #     self.company = Company(ticker)
        
    #     latest_duration = 1 if period == None or period in ("recent", "latest") else 3
        
    #     self.filings = self.company.get_filings(form=form_type).latest(latest_duration)
    #     return self.filings
    
    
    def fetch_filings(self, ticker:str,form_type:list[str],start_date:str, end_date:str=None):
        self.company = Company(ticker)
        start = f"{start_date}-01-01"
        end = f"{end_date}-01-01" if end_date is not None else ""
        final_date = f"{start}:{end}"
        self.filings = self.company.get_filings(form=form_type,
                                                date=final_date)
        return self.filings
        
        

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
    