import streamlit as st
import os
import asyncio
from fastmcp import Client
from langchain_community.document_loaders import PyPDFLoader

# Connect to your local MCP server
client = Client("http://127.0.0.1:8000/mcp")

st.title("Resume Analyzer")

query = st.text_input("💬 Enter your query:", placeholder="Ask something like 'Is my experience section strong enough?'")
submit_button = st.button("Submit Query")
uploaded_file = st.file_uploader("📤 Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    pdf_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Resume uploaded successfully!")

    # Load PDF content
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    page_content = docs[0].page_content

    async def resume_agent(page_content):
        async with client:
            return await client.call_tool("call_analyze_resume", {"page_content": page_content})

    async def feedback_agent(page_content, query):
        async with client:
            return await client.call_tool("feed", {"page_content": page_content, "query": query})

    with st.spinner("🔍 Analyzing your resume..."):
        print("Calling resume_agent...")
        result = asyncio.run(resume_agent(page_content))
        st.subheader("📝 Resume Feedback:")
        st.subheader("-------------------------------------------")
        st.write(result[0].text)

        if query and submit_button:
            print("Calling feedback_agent...")
            feedback = asyncio.run(feedback_agent(page_content, query))
            st.subheader("Response to Your Query:")
            st.subheader("-------------------------------------------")
            st.write(feedback[0].text)

    # Clean up
    try:
        os.remove(pdf_path)
        print("Temporary file removed.")
    except Exception as e:
        print(f"Error removing file: {e}")
