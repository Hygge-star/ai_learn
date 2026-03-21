"""
OpenAi是OpenAI公司发布的Python SDK，方便与编程调用其产品
"""

from openai import OpenAI
from pyexpat.errors import messages

#1.获取client对象，OpenAI类对象
client=OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-80fc678a86a24986b6be4b6749bc973e"
)
#2.调用模型
response=client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role":"system","content":"你是一个Python编程专家，并且不说废话简单回答"},
        {"role":"assistant","content":"好的。我是编程专家，并且话不多，你要问什么？"},
        {"role":"user","content":"输出1-10的数字，使用python代码"}
    ]
)
#3.处理结果
print(response.choices[0].message.content)