    
from langchain_chroma import Chroma
from config.model_gateway import embedding_function

_current_vectorstore = None

def vectordb_store(chunks):
    global _current_vectorstore
    _current_vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
    )
    return _current_vectorstore

def get_vectorstore():
    return _current_vectorstore





# def vectordb_store(chunks):
#     """This function takes preprocessed chunks and stored in a vector database for retrieval and querying """
#     vectorstore = Chroma.from_documents(
#         documents = chunks,
#         embedding = embedding_function,
#         persist_directory="./db_chroma"   #Adding persistence
#     )
        
#     return vectorstore