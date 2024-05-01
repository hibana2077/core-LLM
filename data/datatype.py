'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2024-05-01 17:06:22
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2024-05-01 17:07:48
FilePath: /core-LLM/data/datatype.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from langchain_core.pydantic_v1 import BaseModel, Field

# Define your desired data structure.
class Question(BaseModel):
    question: str = Field(description="question to ask")
    category: str = Field(description="category of the question")

class Answer(BaseModel):
    answer: str = Field(description="answer to the question")
    category: str = Field(description="category of the answer")