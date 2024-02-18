import streamlit as st
from langchain_side_api import create_vector_db, get_ask_chain
from smart_home_control import search_for_api

st.title("智慧家電 🌱")
btn = st.button("Create Knowledgebase")
if btn:
    create_vector_db()

question = st.text_input("Question: ")

if question:
    chain = get_ask_chain()
    response = chain.invoke(question)

    st.header("Answer: ")
    st.write(response['result'])
    st.write(search_for_api(response['result']))
    