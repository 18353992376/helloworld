import os

from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import chat_agent_executor

"sk-726ae67e535f416bb9cef7c94504f400"
os.environ["TAVILY_API_KEY"] = "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"

chatLLM = ChatOpenAI(
    api_key="sk-726ae67e535f416bb9cef7c94504f400",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)
search = TavilySearchResults(max_results=2)
# 让模型绑定工具
model_with_tools = chatLLM.bind_tools([search])
#创建代理
agent_executor = chat_agent_executor.create_tool_calling_executor(chatLLM, [search])
res= agent_executor.invoke({'messages': [HumanMessage(content="请用中文回答，你认为中国未来10年会如何发展？")]})
print(res["messages"][1].content)
