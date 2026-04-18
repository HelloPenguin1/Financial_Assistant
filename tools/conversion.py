from langchain_classic.schema import Document
from config.model_gateway import embedding_function

        
def filings_to_langchain_docs(self, filings, ticker):
    """Take chunks from filings, convert into Lanchain documents with metadata"""
    chunks=[]
    for filing in filings:
        try:
            obj = filing.obj()
            chunk_doc = obj.chunked_document
            items = chunk_doc.list_items()

            for item in items:
                chunks = chunk_doc.chunks_for_item(item)

                for i, c in enumerate(chunks):

                    # robust extraction
                    if isinstance(c, str):
                        text = c
                    else:
                        text = getattr(c, "text", str(c))

                    # filtering
                    if not text or len(text.strip()) < 40:
                        continue
                    if "TableBlock" in text:
                        continue

                    chunks.append(
                        Document(
                            page_content=text,
                            metadata={
                                "ticker": ticker,
                                "form": filing.form,
                                "filing_date": str(filing.filing_date),
                                "section": item,
                                "chunk_id": i,
                                "source": "SEC"
                            }
                        )
                    )

        except Exception:
            continue

    return chunks
    
