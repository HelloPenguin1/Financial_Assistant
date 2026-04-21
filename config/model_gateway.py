# Stores Model Gateways
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from output_val.structured_output import queryDecompose, Section, Sections
from dotenv import load_dotenv
import os
load_dotenv()

#Api KEYS
groq_api_key = os.getenv("GROQ_API_KEY")


from langchain_openai import OpenAIEmbeddings
embedding_function = OpenAIEmbeddings()

query_llm = ChatGroq(groq_api_key=groq_api_key,
                     model_name="llama-3.3-70b-versatile",
                     temperature=0).with_structured_output(queryDecompose)

planner_llm = ChatGroq(groq_api_key=groq_api_key,
                       model_name='llama-3.1-8b-instant',
                       temperature=0.1).with_structured_output(Sections)

writer_llm = ChatGroq(groq_api_key=groq_api_key,
                      model_name="openai/gpt-oss-20b",
                      temperature=0,
                      max_tokens=1024)

#
