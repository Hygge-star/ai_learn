from langchain_classic.chains.summarize.refine_prompts import prompt_template
from langchain_community.llms.tongyi import Tongyi
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

#创建所需的解析器
str_parser=StrOutputParser()

#模型创建
model=ChatTongyi(model="qwen3-max")
first_prompt=PromptTemplate.from_template(
    "我邻居姓：{lastname},刚生了{gender},请起名,仅告知我名字，不要额外信息"
)

second_prompt=PromptTemplate.from_template(
    "姓名：{name},请帮我解析含义"
)

#函数的入参，AIMessage->dic({"name":"xxx})
my_func=RunnableLambda(lambda ai_msg:{"name":ai_msg.content})
#构建链
chain=first_prompt|model|my_func|second_prompt|model|str_parser

res=chain.stream({"lastname":"张","gender":"女儿"})

for chunk in res:
    print(chunk,end=" ",flush=True)