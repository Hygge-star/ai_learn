from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
chat_prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system","你是一个边塞诗人，可以作诗"),
        MessagesPlaceholder("history"),
        ("human","请再来一首唐诗"),

    ]
)

history_data=[
    ("human","你来写一个唐诗"),
    ("ai","床")
]

#prompt_value=chat_prompt_template.invoke({"history":history_data}).to_string()
#print(prompt_value)


model=ChatTongyi(model="qwen-max")

#组成链，要求每一个组件都是Runnable接口的子类
chain=chat_prompt_template | model
#通过链调用invoke或stream
res=chain.invoke({"history":history_data})
print(res.content)

#通过stream流式输出
for chunk in chain.stream({"history":history_data}):
    print(chunk.content,end=" ",flush=True)
    