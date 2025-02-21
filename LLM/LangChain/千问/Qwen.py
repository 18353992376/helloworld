from getpass import getpass

from fastapi import FastAPI
from langchain_community.llms import Tongyi
import os

from langchain_core.prompts import PromptTemplate
from langserve import add_routes

os.environ["DASHSCOPE_API_KEY"] = "sk-726ae67e535f416bb9cef7c94504f400"

llm = Tongyi()
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

chain = prompt | llm

question = "给我讲一个笑话"

print(chain.invoke({"question": question}))

app = FastAPI(title='我的LLM',version='1.0',desecription='我的第一个基于OpenAI的LLM')

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

