from fastmcp import FastMCP
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP('resume_analyzer_server')

def analyze_resume(page_content: str):
    """
    Analyze the resume content and provide feedback and suggestions.
    """
    llm = ChatNVIDIA()

    prompt_template = PromptTemplate(
        template="""
        You are a smart and helpful Resume Analyzer working inside an MCP server.

        Your job is to analyze the input document provided as {page_content}.

        1. First, check if the document is a valid resume.
           - If it is not a resume (e.g., report, article, cover letter), reply with:
             "❌ This is not a resume. Please upload a valid resume document for analysis."

        2. If it **is a resume**, provide detailed and specific feedback in the following areas:
           - **Content Quality**: Are the skills, education, and experiences clearly described and relevant?
           - **Experience Section**:
             - If an address is listed, assume it is the *company's address*.
             - Do **not** confuse it with the candidate's home address.
           - **Address Handling**:
             - Do not mix the candidate's personal address with education-related addresses.
           - **Formatting**:
             - Do not change the format unless it is inconsistent or unclear.
             - Only suggest improvements if formatting affects professionalism or readability.

        3. After feedback, generate an improved version of the resume **only based on your suggestions**.
           - Keep the **original formatting intact** unless formatting improvements were suggested.
           - Do not remove or restructure content unless clearly needed.

        Respond in a helpful, professional tone with concise feedback and actionable changes.
        """,
        input_variables=['page_content']
    )

    chain = prompt_template | llm
    response = chain.invoke({"page_content": page_content})
    print("response generated")
    return response.content

def feedback_resume(query: str, page_content: str):
    """
    Provide feedback on the resume based on a user's query.
    """
    prompt = PromptTemplate(
        template="""
        You are a smart and helpful Resume Analyzer working inside an MCP server.
        Resume Content: {page_content}
        Query: {query}

        Provide specific feedback or answer based on the query.
        """,
        input_variables=["page_content", "query"]
    )
    llm = ChatNVIDIA()
    chain = prompt | llm
    response = chain.invoke({"page_content": page_content, "query": query})
    return response.content

@mcp.tool()
def feed(page_content: str, query: str):
    """
    This tool provides feedback on the resume content based on the user's query.
    """
    print("calling feedback_resume")
    result = feedback_resume(query, page_content)
    return result

@mcp.tool()
def call_analyze_resume(page_content: str):
    """
    This tool analyzes the resume content and provides feedback and suggestions.
    """
    print("calling analyze_resume")
    result = analyze_resume(page_content)
    return result

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
