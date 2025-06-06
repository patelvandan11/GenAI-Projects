from fastmcp import FastMCP
import sqlite3
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import StrOutputParser
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import PromptTemplate

mcp = FastMCP("NLP")



@mcp.tool()
def nl_to_sql(nl_query: str) -> str:
    try:
        prompt = PromptTemplate(
            input_variables=["nl_query"],
            template="""
You are an assistant that converts English to SQL.
Assume the SQLite table "students" with columns:
(id, name, enrollment, standard, subject, city, hobby)

Convert the following question to a SQL query ONLY (no explanation):
Question: {nl_query}
"""
        )
        llm = ChatNVIDIA()
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"nl_query": nl_query})
        sql_query = response.strip().split('\n')[0]

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        connection.close()

        result = "\n".join([str(row) for row in rows]) or "No results found."
        return f"SQL Query: {sql_query}\nResult:\n{result}"

    except Exception as e:
        return f"Error: {str(e)}"


    
if __name__ == "__main__":
    print("MCP server(NLP ) is running...")
    mcp.run()