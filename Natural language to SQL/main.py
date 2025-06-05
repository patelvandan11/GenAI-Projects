# server.py
from openai import OpenAI
import os
from mcp.server.fastmcp import FastMCP
from sqlite3 import connect

# Create an MCP server
mcp = FastMCP("Demo")
connection = connect('student.db')

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Corrected get_all_students tool

# Optional: set your OpenAI API key if not in env vars
# os.environ["OPENAI_API_KEY"] = "api-key"

@mcp.tool()
def nl_to_sql(nl_query: str) -> str:
    """
    Convert natural language to SQL and execute it on the students table.
    Example input: "Show all students from Navsari"
    """
    try:
        # Use a prompt to generate SQL query
        prompt = f"""
You are an assistant that converts English to SQL.
Assume the SQLite table "students" with columns:
(id, name, enrollment, standard, subject, city, hobby)

Convert the following question to a SQL query ONLY (no explanation):
Question: {nl_query}
"""
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        sql_query = response.choices[0].message.content.strip().split('\n')[0]

        # Execute the SQL
        cursor = connection.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        if not rows:
            return "No results found."

        return "\n".join(str(row) for row in rows)

    except Exception as e:
        return f"Error processing query: {str(e)}"


# Run the server
if __name__ == "__main__":
    print("MCP server is running...")
    mcp.run()
