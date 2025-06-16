import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import psycopg2
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("Chat with SQL DB - Rohan")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"
POSTGRES = "USE_POSTGRES"

radio_opt = [
    "Use SQLLite 3 Database- Student.db",
    "Connect to your MySQL Database",
    "Connect to your PostgreSQL Database"
]

selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat", options=radio_opt)

db_uri = None
mysql_host = mysql_user = mysql_password = mysql_db = ""
postgres_host = postgres_user = postgres_password = postgres_db = ""

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
elif radio_opt.index(selected_opt) == 2:
    db_uri = POSTGRES
    postgres_host = st.sidebar.text_input("PostgreSQL Host")
    postgres_user = st.sidebar.text_input("PostgreSQL User")
    postgres_password = st.sidebar.text_input("PostgreSQL Password", type="password")
    postgres_db = st.sidebar.text_input("PostgreSQL Database")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the Groq API key")

# LLM Setup
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None,
                 postgres_host=None, postgres_user=None, postgres_password=None, postgres_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite://", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    elif db_uri == POSTGRES:
        if not (postgres_host and postgres_user and postgres_password and postgres_db):
            st.error("Please provide all PostgreSQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"))

if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
elif db_uri == POSTGRES:
    db = configure_db(db_uri, postgres_host=postgres_host, postgres_user=postgres_user, postgres_password=postgres_password, postgres_db=postgres_db)
else:
    db = configure_db(db_uri)

#  Toolkit and Agent 
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

#  Multi-Agent 
def get_schema_info_pg():
    try:
        conn = psycopg2.connect(
            host=postgres_host,
            user=postgres_user,
            password=postgres_password,
            dbname=postgres_db
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
        """)
        schema_info = cur.fetchall()
        conn.close()
        return schema_info
    except Exception as e:
        st.error(f"Error retrieving schema: {e}")
        return []

def generate_sql_pg(nl_query, schema_info):
    try:
        schema_str = "\n".join([f"{table}.{col}" for table, col in schema_info])
        prompt = PromptTemplate(
            input_variables=["query", "schema"],
            template="""
            You are an AI SQL generator.
            Given this schema:
            {schema}

            Convert this natural language query to SQL:
            {query}
            """
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run({"query": nl_query, "schema": schema_str})
        return result.strip()
    except Exception as e:
        st.error(f"SQL generation failed: {e}")
        return None

def execute_sql_pg(sql):
    try:
        conn = psycopg2.connect(
            host=postgres_host,
            user=postgres_user,
            password=postgres_password,
            dbname=postgres_db
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows if rows else ["No matching records found."]
    except Exception as e:
        st.error(f"Query execution error: {e}")
        return [f"Execution failed: {e}"]

def synthesize_answer_pg(nl_query, sql, rows):
    try:
        prompt = PromptTemplate(
            input_variables=["query", "sql", "results"],
            template="""
            You are a helpful AI assistant.
            Given the original question: {query},
            the SQL query: {sql},
            and these results: {results},
            provide a human-readable answer.
            """
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run({"query": nl_query, "sql": sql, "results": str(rows)})
    except Exception as e:
        return f"Could not synthesize answer due to: {e}"

#Chat UI 
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())

        if db_uri == POSTGRES:
            schema = get_schema_info_pg()
            if not schema:
                response = "Schema not found or unreadable."
            else:
                sql_query = generate_sql_pg(user_query, schema)
                if not sql_query:
                    response = "Failed to generate SQL from the query."
                else:
                    results = execute_sql_pg(sql_query)
                    response = synthesize_answer_pg(user_query, sql_query, results)
        else:
            try:
                response = agent.run(user_query, callbacks=[streamlit_callback])
            except Exception as e:
                response = f"Error processing query: {e}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
