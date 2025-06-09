import os
from dotenv import load_dotenv

from fastmcp import FastMCP
from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import CSVLoader

load_dotenv()
nvidia_api_key = os.getenv("NVIDIA_API_KEY")

loader = CSVLoader(
    file_path="D:/Code/GIt repo/internship+gen ai/GenAI-Projects/Recipe Recommendation/recipe_cleaned.csv"
)

mcp = FastMCP("mcp")

def recipe_finder(ingredients: str):
    embeddings = NVIDIAEmbeddings()

    vector_store = Chroma(
        persist_directory='my_chroma_db',
        embedding_function=embeddings,
        collection_name='recipe_collection'
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    llm = ChatNVIDIA()

    prompt = PromptTemplate(
        template="""
        You are a smart recipe assistant designed to help users cook using ingredients they already have. Your task is to search a provided database of recipes and return the best matching options.

        Instructions:
        - Use only the recipes in the provided context.
        - Recommend 3 to 5 recipes that most closely match the user's available ingredients.
        - For each selected recipe, output:
        - Recipe Name
        - Complete list of ingredients (do not filter by user's ingredients)
        - Clear, concise, and numbered cooking instructions.

        Response Format:
        ---
        Recipe: <Recipe Name>

        Ingredients:
        - item 1
        - item 2
        - ...

        Instructions:
        1. Step one
        2. Step two
        ...

        ---

        Rules:
        - Do NOT fabricate recipes or instructions.
        - Do NOT include any URLs or external links.
        - If no recipe matches the ingredients, reply: "No recipes found using your ingredients."

        Inputs:
        Recipe Database: {context}
        Available Ingredients: {ingredients}
        """,
        input_variables=["context", "ingredients"]
    )

    parser = StrOutputParser()

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "ingredients": RunnablePassthrough()
    })

    main_chain = parallel_chain | prompt | llm | parser

    response = main_chain.invoke(ingredients)
    return response

@mcp.tool()
def recipe(ingredients: str):
    print("calling recipe_finder")
    return recipe_finder(ingredients)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
