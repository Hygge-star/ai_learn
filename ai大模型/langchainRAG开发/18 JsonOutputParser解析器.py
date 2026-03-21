from langchain_classic.chains.summarize.refine_prompts import prompt_template
from langchain_community.llms.tongyi import Tongyi
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from sqlalchemy.testing.provision import setup_config

#创建所需的解析器
str_parser=StrOutputParser()
json_parser=JsonOutputParser()

#模型创建
model=ChatTongyi(model="qwen3-max")
first_prompt=PromptTemplate.from_template(
    "我邻居姓：{lastname},刚生了{gender},请起名，"
    "并封装为JSON格式返回给我。要求key是name,value就是你起的名字，请严格遵守格式。"
)

second_prompt=PromptTemplate.from_template(
    "姓名：{name},请帮我解析含义"
)

#构建链
chain=first_prompt|model|json_parser|second_prompt|model|str_parser

res=chain.stream({"lastname":"张","gender":"女儿"})

for chunk in res:
    print(chunk,end=" ",flush=True)