# Stores Model Gateways
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from output_val.structured_output import queryDecompose
from dotenv import load_dotenv
import os
load_dotenv()

#Api KEYS
groq_api_key = os.getenv("GROQ_API_KEY")


query_llm = ChatGroq(groq_api_key=groq_api_key,
                     model_name="llama-3.1-8b-instant",
                     temperature=0).with_structured_output(queryDecompose)
