
def retrieve_chunks(vectorstore, query, filing_type, k=5):
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": k,
            "filter": {"form": filing_type}
        }
    )
    return retriever.invoke(query)


def tenk_node(vectorstore):
    docs = retrieve_chunks(
        vectorstore,
        query="long term risks, business overview, strategy",
        filing_type="10-K"
    )
    return generate_report(docs, "10-K")


def tenq_node(vectorstore):
    docs = retrieve_chunks(
        vectorstore,
        query="quarterly performance, revenue changes, margins",
        filing_type="10-Q"
    )
    return generate_report(docs, "10-Q")


def eightk_node(vectorstore):
    docs = retrieve_chunks(
        vectorstore,
        query="material events, announcements, sudden changes",
        filing_type="8-K"
    )
    return generate_report(docs, "8-K")