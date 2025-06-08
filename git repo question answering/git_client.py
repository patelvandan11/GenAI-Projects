import streamlit as st
from fastmcp import Client
import asyncio

st.title("🧠 GitHub Project Q&A Assistant")
st.markdown("Ask questions about the `Ai-Trip-Planner` GitHub repository.")

client = Client("http://127.0.0.1:8000/mcp")

async def call_tools(user_query: str):
    """Call the registered tool with the user's query."""
    async with client:
        result = await client.call_tool("github_project_qa", {"question": user_query})
        return result[0].text if isinstance(result, list) and hasattr(result[0], "text") else result
    
def call_tool_sync(user_query: str):
    """Synchronous wrapper for the async tool call."""
    return asyncio.run(call_tools(user_query))

user_query = st.text_input("💬 Enter your question", placeholder="e.g., What does main.py do?")

if st.button("Ask") and user_query:
    with st.spinner("Generating answer..."):
        try:
            response = call_tool_sync(user_query)
            if not response:
                st.warning("No answer found for your question.")
            else:
                st.success("✅ Answer from LLM:")
                st.write(response)
        except Exception as e:
            st.error(f"❌ Error: {e}")