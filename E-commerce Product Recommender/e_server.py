import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings

# Load environment variables
load_dotenv()
nvidia_api_key = os.getenv("NVIDIA_API_KEY")

# FastMCP instance
mcp = FastMCP("mcp")

loadder= CSVLoader(file_path="D:\Code\GIt repo\internship+gen ai\GenAI-Projects\E-commerce Product Recommender\cleaned_flipkart_data.csv",encoding="utf-8")

llm= ChatNVIDIA()
embedding= NVIDIAEmbeddings()

vectorestre=Chroma(
    persist_directory="e-commerce_recommender",
    embedding_function=embedding,
    collection_name="e-commerce_recommender",
)

def create_product_recommender_chain(query:str):
    prompt= PromptTemplate(
    input_variables=["query"],
    template="You are a helpful assistant. Given the query: {query}, provide a relevant product recommendation from the e-commerce dataset.",
)
    output_parser= StrOutputParser()
    chain= prompt|llm|output_parser
    return chain.invoke({"query": query})
    
    
@mcp.tool()
def product(query: str):
    print("Calling product recommender...")
    return create_product_recommender_chain(query)

# Run MCP server
if __name__ == "__main__":
    print("Starting FastMCP server...")
    mcp.run(transport="streamable-http")