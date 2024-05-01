'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2024-05-01 15:09:23
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2024-05-01 17:17:54
FilePath: /core-LLM/data/gen_data.py
Description: 
'''
from yaml import safe_load
from datatype import Question, Answer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from warnings import filterwarnings
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

filterwarnings("ignore")

# # load data
# docs = WikipediaLoader(query="Kāneiolouma Complex", load_max_docs=1).load()
# print(docs[0].page_content)

QUESTION_PARSER = JsonOutputParser(pydantic_object=Question)
ANSWER_PARSER = JsonOutputParser(pydantic_object=Answer)

QUESTION_PROMPTS_TEXT = """You are a highly sophisticated algorithm designed to generate questions from articles. Ensure that each question can be answered based solely on the information provided in the article.
eg.

Organ (biology)

== abstract ==
In a multicellular organism, an organ is a collection of tissues joined in a structural unit to serve a common function. In the hierarchy of life, an organ lies between tissue and an organ system. Tissues are formed from same type cells to act together in a function. Tissues of different types combine to form an organ which has a specific function. The intestinal wall for example is formed by epithelial tissue and smooth muscle tissue. Two or more organs working together in the execution of a specific body function form an organ system, also called a biological system or body system.

== question ==
What is an organ in a multicellular organism?
What does an organ consist of in terms of tissues?
What is the relationship between an organ and an organ system?"""

PROMPTS = {
    "gen_question_json": PromptTemplate(
        template=QUESTION_PROMPTS_TEXT + "\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": QUESTION_PARSER.get_format_instructions()},
    )
}

if __name__ == "__main__":
    try:
        # setting up basic conponents
        config = safe_load(open("./config.yaml", "r"))

    except Exception as e:
        print(e)
        raise e