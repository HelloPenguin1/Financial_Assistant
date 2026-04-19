# Stores Model Gateways
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from output_val.structured_output import queryDecompose, Section, Sections
from dotenv import load_dotenv
import os
load_dotenv()

#Api KEYS
groq_api_key = os.getenv("GROQ_API_KEY")

#Hugging Face 
# embedding_function = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     model_kwargs={"device": "cpu"},
#     encode_kwargs={"normalize_embeddings": True},
# )

from langchain_openai import OpenAIEmbeddings
embedding_function = OpenAIEmbeddings()

query_llm = ChatGroq(groq_api_key=groq_api_key,
                     model_name="llama-3.1-8b-instant",
                     temperature=0).with_structured_output(queryDecompose)

planner_llm = ChatGroq(groq_api_key=groq_api_key,
                       model_name='llama-3.1-8b-instant',
                       temperature=0.1).with_structured_output(Sections)

writer_llm = ChatGroq(groq_api_key=groq_api_key,
                      model_name="openai/gpt-oss-20b",
                      temperature=0)


