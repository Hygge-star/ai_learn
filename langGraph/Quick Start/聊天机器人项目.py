"""
一个 StateGraph 对象将我们的聊天机器人结构定义为“状态机”。
添加 节点 来表示 LLM 和聊天机器人可以调用的函数，
并添加 边 来指定机器人应如何在这些函数之间进行转换
"""
import os
from typing import Annotated
from langchain_community.chat_models import ChatTongyi
from langgraph.constants import END
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition   # 导入预构建组件
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display
from langgraph.types import interrupt,Command
from langchain_core.tools import tool

# ========== 配置密钥 ==========
API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-max"
os.environ["TAVILY_API_KEY"] = "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"

# ========== 定义状态 ==========
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ========== 构建图 ==========
graph_builder = StateGraph(State)

llm = ChatTongyi(model=MODEL, api_key=API_KEY, api_base=BASE_URL)
@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tool = TavilySearch(max_results=2)
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert(len(message.tool_calls) <= 1)
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# ========== 流式输出函数（支持记忆） ==========
def stream_graph_updates(user_input: str, config: dict):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config,
    ):
        if "__interrupt__" in event:
            # 获取中断对象
            interrupt_obj = event["__interrupt__"]

            # 递归提取真实数据（兼容列表、元组、Interrupt 对象）
            def extract_value(obj):
                if isinstance(obj, (list, tuple)) and obj:
                    return extract_value(obj[0])
                if hasattr(obj, "value"):
                    return extract_value(obj.value)
                return obj

            real_data = extract_value(interrupt_obj)

            # 尝试获取提示文本
            if isinstance(real_data, dict):
                prompt = real_data.get("query", real_data.get("message", "需要人工协助"))
            else:
                prompt = str(real_data)

            print(f"\n[系统] {prompt}")
            answer = input("请输入人工回答: ")

            # 恢复执行（根据工具定义，可能期望 {"data": answer} 或直接 answer）
            # 如果你的工具 human_assistance 中 interrupt 返回的是字符串，则直接传 answer
            # 这里假设返回字典格式，与原始调用匹配
            for resume_event in graph.stream(Command(resume={"data": answer}), config=config):
                if "__interrupt__" in resume_event:
                    continue
                for v in resume_event.values():
                    if "messages" in v:
                        print("Assistant:", v["messages"][-1].content)
            return
        else:
            for v in event.values():
                if "messages" in v:
                    print("Assistant:", v["messages"][-1].content)

# ========== 交互循环 ==========
config = {"configurable": {"thread_id": "1"}}   # 同一会话保持记忆

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input, config)
        # 如果需要绘制图，可以取消注释，但建议放在循环外
        # display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception as e:
        print(f"错误: {e}")
        break