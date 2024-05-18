# Importando as bibliotecas necessárias
import openai
import streamlit as st
#from streamlit_option_menu import option_menu
import pandas as pd
import time
import shelve
import openai
from langchain import*
import sqlite3
import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_experimental.sql import SQLDatabaseChain

# --------------------------------------------------------------------------
# Inicialização da instância do cliente OpenAI com chave de API e acessos BD
# --------------------------------------------------------------------------
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

username = st.secrets["username"]
password = st.secrets["password"]
host = st.secrets["host"]
port = st.secrets["port"]
database = st.secrets["database"]

mysql_url = f'mysql+mysqldb://{username}:{password}@{host}:{port}/{database}'

# Configurando com langchain
input_db = SQLDatabase.from_uri(mysql_url)
llm_1 = OpenAI(temperature=1)
db_agent = SQLDatabaseChain(llm = llm_1, database =input_db, verbose=True)

# -----------------------------------------------------------------
# Funções para geração de resposta
# -----------------------------------------------------------------
def generate_response(message_body, db_agent=db_agent):
    response = db_agent.run(message_body)
    return response

# -----------------------------------------------------------------
# Inicializando estado da sessão:
# -----------------------------------------------------------------

# Initialization
if 'in_chat' not in st.session_state:
    st.session_state['in_chat'] = None

# Inicializa a lista de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título da interface de Streamlit
st.title("GPT Analítico")

# Aqui, ele itera sobre todas as mensagens e as exibe (ORIGINAL)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Criação de campo de entrada para a mensagem do usuário
if prompt := st.chat_input("Escreva aqui:"):
    #for i in range(len(st.session_state.messages)):
    #    aux = st.session_state.messages[i]["role"]
    #    with st.chat_message(aux):
    #        st.markdown(st.session_state.messages[i]["content"])

    # A mensagem do usuário é adicionada à lista de mensagens
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Aqui, passa a resposta do usuário para o assistente OpenAI e gera a resposta do assistente
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        #response = st.write_stream(stream)
        st.write(response)
        
    # A resposta do assistente é adicionada à lista de mensagens
    st.session_state.messages.append({"role": "assistant", "content": response})