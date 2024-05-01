'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2024-05-01 15:09:23
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2024-05-01 15:25:33
FilePath: /core-LLM/data/gen_data.py
Description: 
'''
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from warnings import filterwarnings
from langchain_community.document_loaders import WikipediaLoader

filterwarnings("ignore")

# load data
docs = WikipediaLoader(query="La Salute è in voi", load_max_docs=2).load()
print(docs[0].page_content)