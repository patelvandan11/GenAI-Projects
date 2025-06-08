import os
from fastmcp import FastMCP
from dotenv import load_dotenv
from langchain_community.document_loaders import GithubFileLoader
from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
mcp = FastMCP("github_project_qa")

@mcp.tool()
def github_project_qa(question: str) -> str:
    """Answer a question about a GitHub project by analyzing .py, .md, and .jsx files."""
    github_token = os.getenv("GITHUB_TOKEN")

    loader = GithubFileLoader(
        repo="patelvandan11/Ai-Trip-Planner",
        branch="main",
        access_token=github_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith((".py", ".md", ".jsx"))
    )

    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    vector_store = Chroma(
        collection_name="ai_trip_planner_docs",
        embedding_function=NVIDIAEmbeddings(),
        persist_directory="./chroma_langchain_db"
    )

    vector_store.add_documents(split_docs)
    retrieved_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    llm = ChatNVIDIA()
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are an expert AI assistant helping users understand a GitHub project based on its documentation.
        Use the following context, which is extracted from the project's README files and other source files.
        Be concise, accurate, and helpful. If the context does not contain a direct answer, say so clearly. Generate at least 4 sentences.

        ---------------------
        Context:
        {context}
        ---------------------

        Question: {question}

        Answer:
        """.strip()
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"context": context, "question": question})



if __name__ == "__main__":
    print("Github Q&A tool is running...")
    mcp.run(transport="streamable-http")  # Explicitly set port to 8000