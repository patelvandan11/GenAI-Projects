from fastmcp import FastMCP
import urllib.request
import urllib.parse
mcp = FastMCP("ArxivMCPServer")

@mcp.tool(name="fetch_arxiv_papers", description="Fetch research papers from ArXiv using a query string.")
def fetch_arxiv_papers(query: str = "machine learning", max_results: int = 2) -> str:
    """
    Fetch research papers from ArXiv using a query string.
    This tool queries the ArXiv API and returns a string containing the XML response.
    Args:
        query (str): The search query for ArXiv.
        max_results (int): The maximum number of results to return.
        
    """
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")
    


if __name__ == "__main__":
    mcp.run(transport="streamable-http")