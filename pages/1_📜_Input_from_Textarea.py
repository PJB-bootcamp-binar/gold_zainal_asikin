import streamlit as st
import re
import pandas as pd
from io import StringIO
import chardet
import sqlite3
from sqlite3 import Connection

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()

import nltk
#nltk.download('stopwords')
stopword = nltk.corpus.stopwords.words('indonesian')

from nltk.tokenize.treebank import TreebankWordDetokenizer

############################################################

st.write("# Endpoint 1: Cleansing Text App from Textarea📜")

st.markdown(
    """
    Cleansing Text App is the process of preparing text data for further analysis or processing by removing or correcting irrelevant, incorrect, or noisy information. 

    The goal of text cleansing is to improve the quality and reliability of the data and to make it consistent, accurate, and ready for use. 

    This process involves tasks such as correcting spelling and grammar errors, removing punctuation, converting text to lowercase, removing stop words, and standardizing abbreviations.

    It may also involve transforming the text data into a structured format, such as transforming a list of text into a table, in order to facilitate further analysis.

    *Example:*   """)

st.code('aamiin USER USER Ngakunya org pintar dan beragama, emangnya agama mana yg memperbolehkan menista dan menghujat org lain???. '
    'Jgnkan orang bodoh, org yg ( maaf) sejak lahir idiot sekalipun dia, kita hrs hargain sebagai sesama ciptaan Tuhan. Ingat : iblis itu juga pintar dan sangat licik!!!', language='python')


def remove_punct(tweet):
    tweet = re.sub(r'[^\x00-\x7f]', ' ', str(tweet))
    tweet = re.sub(r'(\\u[0-9A-Fa-f]+)', ' ', str(tweet))
    tweet = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", ' ', str(tweet))
    tweet = re.sub(r'\\u\w\w\w\w', ' ', str(tweet))

    tweet = re.sub(r'http\S+', ' ', str(tweet))
    tweet = re.sub('@[^\s]+', ' ', str(tweet))
    tweet = re.sub(r'#([^\s]+)', ' ', str(tweet))
    tweet = re.sub(r"[.,:;+!\-_<^/=?\"'\(\)\d\*]", ' ', str(tweet))
    return tweet

def tokenization(tweet):
    tweet = re.split('\W+', tweet)
    return tweet

def normalisasi(tweet):
    kamusalay_dict = dict(df_uploaded_kamusalay.values)
    pattern = re.compile(r'\b( ' + '|'.join(kamusalay_dict.keys())+r')\b') # Search pola kata (contoh kpn -> kapan)
    content = []
    for kata in tweet:
        filteredSlang = pattern.sub(lambda x: kamusalay_dict[x.group()],kata) # Replace slangword berdasarkan pola review yg telah ditentukan
        content.append(filteredSlang.lower())
    tweet = content
    return tweet

def stemming(tweet):
    tweet = [stemmer.stem(word) for word in tweet]
    return tweet

def remove_stopwords(tweet):
    tweet = [word for word in tweet if word not in stopword]
    return tweet

URI_SQLITE_DB = "pages/data/data_cleansing.db"
#@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    return sqlite3.connect(path, check_same_thread=False)

def init_db(conn: Connection):
    conn.execute("""CREATE TABLE IF NOT EXISTS result (RAW_DATA, CLEANED_DATA);""")
    conn.commit()

def get_data(conn: Connection):
    dfr = pd.read_sql("SELECT CLEANED_DATA as CLEANED_SQLITE3_DATA FROM result", con=conn)
    return dfr

def display_data(conn: Connection):
    st.dataframe(get_data(conn))

############################################################

df_ori = st.text_area('*Input some text to analyze:*', '''    ''')
df = df_ori

uploaded_kamusalay = st.file_uploader("Upload slangword or *kamus_alay* CSV file", key = 'kamusalay')   #kamusalay = pd.read_csv('pages/new_kamusalay.csv', sep=',', encoding = "ISO-8859-1") # Membuka dictionary slangword
if uploaded_kamusalay is not None:
    df_uploaded_kamusalay = pd.read_csv(uploaded_kamusalay, encoding = "ISO-8859-1", sep=',')

df = remove_punct(df)   #df['text_only'] = df['Tweet'].str.replace(r'[^\w\s]|_', '', regex=True) #WORK
df = df.lower()
df = tokenization(df)
try:
    df = normalisasi(df)
except Exception:
    pass
df = stemming(df)
df = remove_stopwords(df)
df = TreebankWordDetokenizer().detokenize(df)
df = df.replace(r'\b\w\b', '').replace(r'\s+', ' ').replace('xf','')
st.write('*Here the result:* **:red[', df,']**')

data = {'ori':  [df_ori], 'clean': [df] }
df_csv = pd.DataFrame(data)
df_sql = df

#EXPORT TO CSV FILE
@st.cache
def convert_df(df_csv):
    return df_csv.to_csv().encode('utf-8')
csv = convert_df(df_csv)     
if df != '':
    st.download_button("Export result to CSV",csv,"cleaned_data.csv","text/csv",key='browser-data')

    #SAVE DATA TO SQLITE3
    if st.button("Save to database"):    
        conn = get_connection(URI_SQLITE_DB)
        init_db(conn)
        conn.execute(f"INSERT INTO result VALUES (?, ?)", (df_ori, df_sql))
        conn.commit()
        display_data(conn)































