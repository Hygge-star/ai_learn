from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description="获取股票价格，输入股票名称")
def get_price(name: str) -> str:
    return f'股票{name}的价格是20元'

@tool(description="获取股票基本信息，输入股票名称")
def get_info(name: str) -> str:
    return f'股票{name},是一家A股上市公司，专注于IT职业教育。'

system_prompt = "你是一个股票信息智能助手。当用户询问股票价格，调用价格工具；询问股票信息，调用信息工具。回答时要说明调用工具的原因。"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_price, get_info],
    system_prompt=system_prompt
)

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "请告诉我传智教育的股价，并介绍一下这只股票"}]},
    stream_mode="values",
):
    last_message=chunk['messages'][-1]
    if last_message.content:
        print(type(last_message).__name__,last_message.content)
    try:
        if last_message.tool_calls:
            print(f"工具调用：{[tc['name'] for tc in last_message.tool_calls]}")

    except AttributeError as e:
        pass
