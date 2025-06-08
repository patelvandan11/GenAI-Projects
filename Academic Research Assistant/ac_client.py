import streamlit as st
import asyncio
from fastmcp import Client
import xml.etree.ElementTree as ET

# MCP server endpoint (make sure ac_server.py is running)
client = Client("http://127.0.0.1:8000/mcp")
ns = {'atom': 'http://www.w3.org/2005/Atom'}

# UI Title
st.title("📚 Academic Research Assistant")

# Query input
query = st.text_input("🔍 Enter a research topic to search ArXiv", value="deep learning")
max_results = st.slider("📄 Number of papers to fetch", 1, 10, 3)

# Parse XML result from ArXiv API
def parse_arxiv_xml(xml_string):
    root = ET.fromstring(xml_string)
    entries = root.findall('atom:entry', ns)

    papers = []
    for entry in entries:
        title = entry.find('atom:title', ns).text.strip()
        summary = entry.find('atom:summary', ns).text.strip()
        link = None
        for l in entry.findall('atom:link', ns):
            if l.attrib.get('rel') == 'alternate':
                link = l.attrib.get('href')
                break
        papers.append({
            "title": title,
            "summary": summary,
            "link": link
        })
    return papers

# Async tool call to fetch ArXiv papers
async def fetch_papers(query, max_results=3):
    async with client:
        result = await client.call_tool("fetch_arxiv_papers", {
            "query": query,
            "max_results": max_results
        })
        xml_data = result[0].text if isinstance(result, list) and hasattr(result[0], "text") else result
        return parse_arxiv_xml(xml_data)

# Sync wrapper for Streamlit
def fetch_papers_sync(query, max_results):
    return asyncio.run(fetch_papers(query, max_results))

# UI Button
if st.button("🚀 Search Papers"):
    with st.spinner("Calling ArXiv tool..."):
        try:
            papers = fetch_papers_sync(query, max_results)
            if not papers:
                st.warning("No papers found.")
            else:
                st.subheader("📑 Search Results")
                for i, paper in enumerate(papers):
                    st.markdown(f"### {i+1}. [{paper['title']}]({paper['link']})")
                    st.write(paper['summary'])
                    st.markdown("---")
        except Exception as e:
            st.error(f"❌ Error: {e}")
