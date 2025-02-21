# 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
import os


from fastapi import FastAPI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes


os.environ["OPENAI_API_KEY"] = "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"
os.environ["https://proxy"] = "127.0.0.1:7890"
os.environ["https://proxy"] = "127.0.0.1:7890"
os.environ["LANGCAHIN__TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KE"]= "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"

# 调用大预言模型
LLM = ChatOpenAI(model="gpt")
message=[
    SystemMessage(content="请将一下内容翻译成英语"),
    HumanMessage(content="你好，我是小明")
]
prompt_template = ChatPromptTemplate.from_messages([
    ('system', "请将一下内容翻译成{language}"),
    ('user', "{text}")
])
parser = StrOutputParser()
chain = prompt_template | LLM | parser
chain.invoke({"language": "English", "text": "你好，我是小明"})


app = FastAPI(title='我的LLM',version='1.0',desecription='我的第一个基于OpenAI的LLM')

add_routes(
    app,
    chain,
    path="/chain",
)
#
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

