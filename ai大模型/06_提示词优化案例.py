
# 导入必要的库
# 这里导入的 responses 实际上在代码中未使用，可能是原代码计划后续使用但未实现
from http.client import responses
# 导入 tkinter 的 scrolledtext 模块中的 example，不过这里导入的 example 未在代码中使用，可能是原代码有误
# 导入 OpenAI 库，用于与大模型进行交互
from openai import OpenAI
# 导入 pyexpat 模块中的 errors 下的 messages，不过这里导入的 messages 后续被重新定义，原导入的 messages 未使用
from pyexpat.errors import messages

# 1. 获取 client 对象，OpenAI 类对象
# 创建 OpenAI 客户端实例，指定 base_url 和 api_key
# base_url 指向阿里云的兼容模式 API 地址
# api_key 是访问阿里云大模型服务的凭证
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-80fc678a86a24986b6be4b6749bc973e"
)

# 定义消息列表，用于与大模型进行交互
# 系统消息，告知大模型其角色和分类任务
messages = [
    {"role": "system", "content": "你是金融专家，将文本分类为['新闻报道', '财务报道', '公司公告', '分析师报告'],不清楚的分类为不清楚类别"}
]

# 假设 examples_data 是一个字典，包含了需要分类的文本数据
# 这里需要补充 examples_data 的定义，例如：
examples_data = {
    "user": "这是一条关于公司的新闻报道内容示例",
    # 可以添加更多的文本数据
}

# 将 examples_data 中的数据添加到 messages 列表中
for key, value in examples_data.items():
    messages.append({"role": key, "content": value})

# 遍历 messages 列表，对每个消息进行分类
for q in messages:
    if q["role"] == "user":  # 只对用户消息进行分类
        try:
            # 调用大模型进行文本分类
            response = client.chat.completions.create(
                model="qwen3-max",
                # 将系统消息、已有消息和当前用户消息合并
                messages=messages + [{"role": "user", "content": q["content"]}]
            )
            # 打印大模型返回的分类结果
            print(response.choices[0].message.content)
        except Exception as e:
            # 处理可能出现的异常，例如网络问题、API 调用失败等
            print(f"请求出错: {e}")

