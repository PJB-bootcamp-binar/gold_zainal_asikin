import streamlit as st

st.set_page_config(
    page_title="Gold Challenge App",
    page_icon="👋",
)

st.write("# Welcome to Gold Challenge App 👋")

st.sidebar.success("Select menu above")

st.markdown(
    """
    Gold Challenge App is an app to convert non natural language to natural language for pre-processing data.
    **👈 Select a menu from the sidebar** to see app endpoints.

    ### What is Natural Language Processing (NLP)?
    Natural language processing (NLP) is a field of computer science, artificial intelligence, and linguistics concerned with the interactions between computers and 
    human (natural) languages. The goal of NLP is to enable computers to understand, interpret, and generate human language in a way that is both meaningful and useful.

    NLP tasks include sentiment analysis, machine translation, text classification, and named entity recognition, among others. These tasks require a deep understanding of the 
    structure, meaning, and context of natural language, and they often involve complex algorithms and models that are trained on large amounts of data.

    NLP is an interdisciplinary field that draws on techniques from computer science, linguistics, mathematics, and psychology. It is used in a variety of applications, 
    including language translation, virtual assistants, and customer service chatbots, among others.

    So, let's try it!!! 

    *Choose menu on the left side to start...*
    
"""
)

# import chardet
# import pandas as pd

# with open('pages/new_kamusalay.csv', 'rb') as f:
#     enc = chardet.detect(f.read())  # or readline if the file is large

# st.write("enc=", enc)

# import pandas as pd
# import sqlite3
# from sqlite3 import Connection

# URI_SQLITE_DB = "test.db"

# @st.cache(hash_funcs={Connection: id})
# def get_connection(path: str):
#     return sqlite3.connect(path, check_same_thread=False)

# def init_db(conn: Connection):
#     conn.execute("""CREATE TABLE IF NOT EXISTS test (INPUT1 INT, INPUT2 INT);""")
#     conn.commit()

# def get_data(conn: Connection):
#     df = pd.read_sql("SELECT * FROM test", con=conn)
#     return df

# def display_data(conn: Connection):
#     if st.checkbox("Display data in sqlite databse"):
#         st.dataframe(get_data(conn))

# conn = get_connection(URI_SQLITE_DB)
# init_db(conn)

# input1 = st.sidebar.slider("Input 1", 0, 100)
# input2 = st.sidebar.slider("Input 2", 0, 100)

# if st.sidebar.button("Save to database"):
#     conn.execute(f"INSERT INTO test (INPUT1, INPUT2) VALUES ({input1}, {input2})")
#     conn.commit()

# display_data(conn)

