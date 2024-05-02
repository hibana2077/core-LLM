'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2024-05-01 15:09:23
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2024-05-02 14:52:16
FilePath: /core-LLM/data/gen_data.py
Description: 
'''

import pandas as pd
import logging

from time import sleep
from typing import List
from yaml import safe_load
from datatype import Question, Answer
from warnings import filterwarnings

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO)

# Ignore warnings
filterwarnings("ignore")

# Load config
config = safe_load(open("./config.yaml", "r"))

QUESTION_PARSER = JsonOutputParser(pydantic_object=Question)
ANSWER_PARSER = JsonOutputParser(pydantic_object=Answer)

QUESTION_PROMPTS_TEXT = """You are a highly sophisticated algorithm designed to generate questions from articles. Ensure that each question can be answered based solely on the information provided in the article.
eg.

Organ (biology)

== abstract ==
In a multicellular organism, an organ is a collection of tissues joined in a structural unit to serve a common function. In the hierarchy of life, an organ lies between tissue and an organ system. Tissues are formed from same type cells to act together in a function. Tissues of different types combine to form an organ which has a specific function. The intestinal wall for example is formed by epithelial tissue and smooth muscle tissue. Two or more organs working together in the execution of a specific body function form an organ system, also called a biological system or body system.

== question == (In json format)
What is an organ in a multicellular organism?
What does an organ consist of in terms of tissues?
What is the relationship between an organ and an organ system?
"""

ANSWER_PROMPTS_TEXT = """You are an advanced algorithm designed to generate answers from articles. Your task is to provide responses to questions using information directly from the article.
eg.

Organ (biology)

== abstract ==
In a multicellular organism, an organ is a collection of tissues joined in a structural unit to serve a common function. In the hierarchy of life, an organ lies between tissue and an organ system. Tissues are formed from same type cells to act together in a function. Tissues of different types combine to form an organ which has a specific function. The intestinal wall for example is formed by epithelial tissue and smooth muscle tissue. Two or more organs working together in the execution of a specific body function form an organ system, also called a biological system or body system.

== question ==
What is an organ in a multicellular organism?
What does an organ consist of in terms of tissues?

== answer == (In json format)
In a multicellular organism, an organ is a collection of tissues joined in a structural unit to serve a common function.
An organ consists of tissues of different types that combine to form an organ which has a specific function.

== format_instructions ==
- The response should not start with "Here is the answer in JSON format:" or any other introductory text.
"""

REJECT_TEXT = """The question is not relevant to the article. Please generate a new question based on the information provided in the article."""

PROMPTS = {
    "gen_question_json": PromptTemplate(
        template=QUESTION_PROMPTS_TEXT + "\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": QUESTION_PARSER.get_format_instructions()},
    ),
    "gen_answer_json": PromptTemplate(
        template=ANSWER_PROMPTS_TEXT + "\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": ANSWER_PARSER.get_format_instructions()},
    )
}

llm_dict = {
    "groq": ChatGroq(groq_api_key=config["llm_setting"]["llm_api_token"]),
}

llm = llm_dict[config["llm_setting"]["llm_provider"]]
llm.model_name = config["llm_setting"]["llm_model"]
llm.temperature = 0
# llm.groq_api_key = config["llm_setting"]["llm_api_token"]
llm.max_tokens = config["llm_setting"]["llm_max_tokens"]

def gen_data(target:str, data:pd.DataFrame, config:dict):
    print(f"Generating data for {target}")
    docs = WikipediaLoader(query = target,load_max_docs=1).load()
    Q_query = f"""{target} == abstract == {docs[0].page_content}"""
    A_query = """{target} == abstract == {abstract} == question == {questions}"""
    Q_chain = PROMPTS["gen_question_json"] | llm | QUESTION_PARSER
    Q_result = Q_chain.invoke({"query": Q_query}) # get questions and its difficulty in list[dict]
    print("=====================================")
    print(Q_result)
    print("=====================================")
    sleep(1)
    A_chain = PROMPTS["gen_answer_json"] | llm | ANSWER_PARSER
    for question in Q_result:
        A_result = A_chain.invoke({"query": A_query.format(target=target, abstract=docs[0].page_content, questions=question['question'])})
        sleep(1)
        print(A_result)
        print("\n")
        tmp_data = pd.DataFrame({"prompt":question["question"],"chosen":A_result["answer"],"rejected":REJECT_TEXT,"diffculty":question["difficulty"],"theme":target,"reference":docs[0].page_content},index=[0])
        data = pd.concat([data,tmp_data],ignore_index=True)
    return data

if __name__ == "__main__":
    try:
        # setting up basic conponents
        config = safe_load(open("./config.yaml", "r"))
        datasets = pd.read_csv(config["data_setting"]["data_path"])
        targets:List[str] = config["target"]
        new_df = pd.DataFrame(columns=["prompt","chosen","rejected","diffculty","theme","reference"])
        for target in targets:
            new_df = gen_data(target, new_df, config)
        new_df.to_csv(config["data_setting"]["save_data_path"], index=False)
    except Exception as e:
        print(e)
        new_df.to_csv(config["data_setting"]["save_data_path"], index=False)
        raise e