# Multi-Agent-RAG-System-for-Natural-Language-Querying-of-a-Relational-Database


🧠 Multi-Agent RAG System – Chat with Your Database
This is a simple web app where you can ask questions in English, and it will talk to your database (PostgreSQL, MySQL, or SQLite) and give you answers using AI (Groq + LangChain).

✅ What This App Can Do
Ask questions like “How many customers joined last year?”

Works with SQLite, MySQL, or PostgreSQL

Breaks the task into smart steps (agents):

Find the right tables

Write the SQL query

Run the query

Turn the result into a human answer

Shows helpful messages if something goes wrong

Easy-to-use web interface using Streamlit

🛠️ How to Set Up
1. Clone this project
bash
Copy
Edit
git clone https://github.com/your-username/multi-agent-rag-sql.git
cd multi-agent-rag-sql
2. Create and activate a virtual environment
bash
Copy
Edit
python -m venv venv
# For Windows
venv\Scripts\activate
# For Mac/Linux
source venv/bin/activate
3. Install required packages
bash
Copy
Edit
pip install -r requirements.txt
Your requirements.txt should include:

php
Copy
Edit
streamlit
langchain
langchain_groq
sqlalchemy
psycopg2-binary
mysql-connector-python
4. Run the app
bash
Copy
Edit
streamlit run app.py
🔑 How to Get the Groq API Key
Go to https://console.groq.com/keys

Sign up or log in

Click on Create API Key

Copy the key and paste it into the sidebar in the app where it says Groq API Key

💬 How to Use
Select your database from the sidebar:

SQLite (default)

MySQL (enter host, user, password, db name)

PostgreSQL (enter host, user, password, db name)

Paste your Groq API key in the input box

Type a question like:

“List all employees in the Marketing team”

“Show me the sales in Q1 2024”

“How many customers joined in the last 6 months?”

The app will:

Understand the question

Generate SQL

Run it

Show you a clean answer + SQL steps

🧠 Behind the Scenes (Agents Used)
🧩 Schema Agent – finds which tables and columns to use

💡 SQL Generator – writes the SQL query using Groq AI

🧮 Retriever – runs the query and gets results

📄 Synthesizer – gives you a nice human answer

⚠️ Handles Errors Like
Table not found

Bad SQL

No data found

And shows a helpful message instead of crashing.

🧪 Example Data for PostgreSQL
Create 3–5 tables like:

customers

sales

projects

employees

Each with 100–1000 fake records. You can use websites like https://mockaroo.com to create fake data.

📦 Optional Improvements
Add vector database fallback if SQL fails

Add support for PDFs or documents

🧑‍💻 Made By
Rohan Gaikwad
📧 rohang@example.com
🔗 LinkedIn
