import streamlit as st
import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")

st.set_page_config(page_title="E-commerce Product Recommender")
st.title("🛍️ E-commerce Product Recommender")

query = st.text_input("Search for products:")

async def search_products(query):
    async with client:
        return await client.call_tool("product", {"query": query})

def run_async(coro):
    return asyncio.run(coro)

# Button interaction
if st.button("🔍 Find Products"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        with st.spinner("Searching products..."):
            try:
                result = run_async(search_products(query))
                st.success("Recommendations ready!")

                if isinstance(result, str):
                    st.markdown(result)
                elif isinstance(result, list) and result:
                    for product in result:
                        st.markdown(product.text)
                else:
                    st.info("No relevant products found.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
