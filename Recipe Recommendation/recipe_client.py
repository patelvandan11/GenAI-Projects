import streamlit as st
import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")

st.title("Recipe Recommendation Chatbot")

ingredients = st.text_area("Enter your available ingredients (comma separated)")

async def recipe_agent(ingredients):
    async with client:
        return await client.call_tool("recipe", {"ingredients": ingredients})

def run_async(coro):
    """Helper to run async functions in sync context."""
    return asyncio.run(coro)

if st.button("Find Recipes"):
    if not ingredients.strip():
        st.warning("Please enter some ingredients.")
    else:
        with st.spinner("Finding recipes..."):
            try:
                response = run_async(recipe_agent(ingredients))
                st.success("Recipes found!")
                
                if isinstance(response, list) and len(response) > 0:
                    st.markdown(response[0].text)
                else:
                    st.markdown(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
