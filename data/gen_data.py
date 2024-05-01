'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2024-05-01 15:09:23
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2024-05-01 16:16:38
FilePath: /core-LLM/data/gen_data.py
Description: 
'''
from yaml import safe_load
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from warnings import filterwarnings
from langchain_community.document_loaders import WikipediaLoader

filterwarnings("ignore")

# load data
docs = WikipediaLoader(query="Kāneiolouma Complex", load_max_docs=1).load()
print(docs[0].page_content)