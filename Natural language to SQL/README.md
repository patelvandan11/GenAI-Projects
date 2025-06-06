# 🧠 Natural Language to SQL Converter

A smart tool to convert plain English questions into SQL queries using FastMCP, LangChain, and NVIDIA's LLM—making database interaction as easy as asking a question.

---

## ✨ Features

- Convert natural language to SQL using an LLM (LangChain + ChatNVIDIA)
- Support for basic CRUD operations on a `students` table
- Direct SQLite execution and result fetching
- Easy-to-understand code structure and output formatting

---

## 🧰 Prerequisites

- Python 3.8+
- `uv` for environment setup (optional but recommended)
- `.env` file with necessary API keys (e.g., NVIDIA cloud key if required)

---

## 🛠 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd 'GenAI-Projects/Natural language to SQL'

# Install dependencies
uv add fastmcp langchain langchain-nvidia-ai-endpoints python-dotenv

# Initialize the environment
uv init .
```

## 🚀 Usage

### 1️⃣ Start the FastMCP Server

```bash
fastmcp run nlp_server.py:mcp
```
### 2️⃣ Run the Client
```bash
python nlp_client.py
```

#### 💬 Example Query:
```bash
"give all students who are in 10th standard and name starts with N"
```
#### 🧾 Output:

```bash
SQL Query: SELECT * FROM students WHERE standard = '10th' AND name LIKE 'N%';

Result:(1, 'Neha', 'EN1234', '10th', 'Physics', 'Navsari', 'watch movies')

```
## 📋 Example Queries

| Input (Natural Language)                             | Output (SQL Query)                                        |
| ---------------------------------------------------- | --------------------------------------------------------- |
| "Show all students from Navsari"                     | `SELECT * FROM students WHERE city = 'Navsari';`          |
| "Add Neha to 10th standard with hobby reading"       | `INSERT INTO students ...`                                |
| "Update Neha's name to Pratik where city is Navsari" | `UPDATE students SET name='Pratik' WHERE city='Navsari';` |
| "Delete all students in 9th standard"                | `DELETE FROM students WHERE standard = '9th';`            |


## 🔧 Under Development

We are actively working to enhance the capabilities of the Natural Language to SQL Converter. Upcoming features include:

- 🧠 **Named Entity Recognition (NER)**  
  Automatically extract meaningful entities from user queries such as:
  - Student names
  - City names
  - Subjects
  - Standards

- 🤖 **Improved NLP Capabilities**  
  Improve the system's ability to:
  - Understand complex sentence structures
  - Handle ambiguous phrasing
  - Support broader types of database schemas
