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

#StringPromptValue to_string()
prompt_text=chat_prompt_template.invoke({"history":history_data}).to_string()
print(prompt_text)

model=ChatTongyi(model="qwen3-max")
res=model.invoke(input=prompt_text)
print(res.content,type(res))

