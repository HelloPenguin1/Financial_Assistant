    
from langchain_chroma import Chroma
from config.model_gateway import embedding_function


def vectordb_store(chunks):
    """This function takes preprocessed chunks and stored in a vector database for retrieval and querying """
    vectorstore = Chroma.from_documents(
        documents = chunks,
        embedding = embedding_function,
    )
        
    return vectorstore