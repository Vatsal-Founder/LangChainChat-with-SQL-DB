import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from langchain_community.agent_toolkits import create_sql_agent
from langchain.prompts import PromptTemplate
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import openai
from langchain.prompts import ChatPromptTemplate
from langchain.utilities import SQLDatabase
from langchain.agents import initialize_agent, Tool


st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")



LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

options=["Connect SQLLite 3 DB","Connect MySQL Database "]

select_options=st.sidebar.radio(label="Please select the required Database",options=options)

if options.index(select_options)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MySQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL password",type="password")
    mysql_db=st.sidebar.text_input("MySQL database")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input(label="Open AI API Key",type="password")


if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the open ai api key")

## LLM model
openai.api_key=api_key
llm=ChatOpenAI(model="gpt-4o")

@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"sales.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))   
    
if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_uri)

toolkit=SQLDatabaseToolkit(db=db,llm=llm)




# Define your custom tool (generate SQL only)
def generate_sql_only(question: str) -> str:
    sql = toolkit.llm_chain.run(question)
    return f"Answer (simulated): [Imagine the result here based on the SQL query]\n\nSQL Query:\n{sql}"

custom_tool = Tool(
    name="GenerateSQL",
    func=generate_sql_only,
    description="Use this to generate SQL for a question without executing it. Shows the SQL only."
)



    




agents= create_sql_agent(llm=llm,
                         toolkit=toolkit,
                         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                         verbose=True,
                         handle_parsing_errors=True
                         )



if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agents.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)