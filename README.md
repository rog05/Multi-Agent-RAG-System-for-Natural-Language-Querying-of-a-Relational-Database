# Multi-Agent-RAG-System-for-Natural-Language-Querying-of-a-Relational-Database


# 🧠 Multi-Agent RAG System – Chat with Your Database

This is a web app where you can **ask questions in natural language**, and it will automatically interact with your **SQL database** (SQLite, MySQL, PostgreSQL) to give accurate answers using **Groq's LLM + LangChain**.

---

## 🚀 Features

- 🔎 Natural language to SQL conversion
- 📊 Supports SQLite, MySQL, PostgreSQL
- 🧠 Modular Multi-Agent System:
  - **Schema Agent** – Finds relevant tables and fields
  - **SQL Generator Agent** – Generates SQL using LLM
  - **Retriever Agent** – Executes the SQL query
  - **Synthesizer Agent** – Converts result to human-readable answers
- ✅ Handles complex queries:
  - Filtering, conditions
  - Aggregations (`SUM`, `AVG`, `COUNT`)
  - Joins, and temporal references (e.g., "Q1 2023")
- 🔁 Error handling:
  - Table/schema not found
  - SQL generation failure
  - No records found
- 🖥️ Interactive Streamlit web interface

---

## 📦 Tech Stack

- Python 🐍
- LangChain 🧠
- Streamlit 🎈
- PostgreSQL / MySQL / SQLite 💾
- Groq LLM (LLaMA 3) ⚡

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

bash
git clone https://github.com/your-username/multi-agent-rag-sql.git
cd multi-agent-rag-sql

## 2. Create and Activate a Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

##3. Install Dependencies
pip install -r requirements.txt

##4. Run the App
streamlit run app.py

##🔑 Get Groq API Key
Visit: https://console.groq.com/keys
Log in or sign up
Click Create API Key
Copy the key and paste it in the sidebar of the app under Groq API Key


