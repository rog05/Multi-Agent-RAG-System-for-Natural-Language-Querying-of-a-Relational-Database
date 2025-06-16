# Multi-Agent-RAG-System-for-Natural-Language-Querying-of-a-Relational-Database


Multi-Agent RAG System – Chat with Your Database

A smart web app that lets you ask natural language questions and get answers directly from your database (SQLite, MySQL, or PostgreSQL) using LangChain + Groq + Streamlit.

✅ What This App Can Do

- Ask: “How many customers joined last year?”
- Works with SQLite, MySQL, or PostgreSQL
- Breaks down the query into smart steps using multi-agents:
  - Identify relevant tables
  - Generate SQL query
  - Run the query
  - Convert result into a human-readable answer
- Handles errors gracefully with helpful messages
- Clean, interactive web UI with Streamlit

🛠️ Setup Instructions

1. Clone the Project

git clone https://github.com/rog05/Multi-Agent-RAG-System-for-Natural-Language-Querying-of-a-Relational-Database.git
cd Multi-Agent-RAG-System-for-Natural-Language-Querying-of-a-Relational-Database

2. Create and Activate Virtual Environment

python -m venv venv

For Windows:
venv\Scripts\activate

For Mac/Linux:
source venv/bin/activate

3. Install Requirements

pip install -r requirements.txt

4. Run the App

streamlit run app.py

🔑 Get Your Groq API Key

1. Visit: https://console.groq.com/keys
2. Sign up / Log in
3. Click on Create API Key
4. Copy the key and paste it in the sidebar input box of the app

💬 How to Use the App

1. Choose your database from the sidebar:
   - SQLite (default)
   - MySQL (enter host, user, password, database)
   - PostgreSQL (enter host, user, password, database)

2. Paste your Groq API key

3. Ask a question, such as:
   - “List all employees in the Marketing team”
   - “Show me the sales in Q1 2024”
   - “How many customers joined in the last 6 months?”

4. The app will:
   - Understand your question
   - Generate SQL
   - Execute the query
   - Show you a clean, human-readable answer and SQL explanation

🧠 Agents Behind the Scenes

- Schema Agent: Finds relevant tables and columns
- SQL Generator: Creates the SQL query using Groq AI
- Retriever: Executes SQL and fetches results
- Synthesizer: Converts raw results into a human-friendly response

⚠️ Error Handling

Gracefully manages:
- Table not found
- Invalid SQL
- No matching data

Shows helpful messages to guide you instead of crashing.

📦 Optional Improvements (Future Scope)

- Add vector database fallback if SQL fails
- Document (PDF) data querying support

👨‍💻 Made By

Rohan Gaikwad
gaikwadrohan8652@gmail.com
