# 扫地机器人智能客服 —— RAG + Agent 驱动的大模型应用

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4+-orange.svg)](https://www.trychroma.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 一个基于 **大语言模型** 的智能客服系统，结合 **检索增强生成（RAG）** 与 **自主智能体（Agent）** 技术，旨在构建一个能够根据特定领域知识高效回答问题、提供解决方案的智能系统。
> 支持多格式文档问答、故障排查、选购建议，并提供友好的 **Streamlit** 可视化界面。

---

### 项目简介

本项目实现了一套完整的 **RAG + Agent** 架构的智能问答系统，以扫地机器人知识库为背景，展示了大模型在垂直领域的应用能力。系统包含以下核心模块：

- **RAG 模块**：对本地 PDF/TXT 文档进行向量化存储，通过语义检索增强生成内容的准确性和实时性。
- **Agent 模块**：基于 LangChain 的 ReAct 模式，智能体能够自主调用 RAG 检索工具、推理多步问题并给出最终答案。
- **前端界面**：使用 Streamlit 构建交互式聊天界面，支持用户输入问题、查看思考过程和历史记录。
- **模型工厂**：统一管理 LLM 调用，支持 OpenAI 及其他兼容接口，便于切换模型。
- **配置管理**：通过 YAML 文件集中管理模型参数、提示词模板、RAG 参数等，无需修改代码即可调优。
- **日志与监控**：完整的运行日志记录，便于调试和分析智能体行为。

项目旨在为开发者提供一个开箱即用的智能客服模板，可快速适配到其他产品文档或垂直领域。

---

### 技术栈

| 类别         | 技术                                                         |
| ------------ | ------------------------------------------------------------ |
| **前端界面** | Streamlit – 快速构建数据应用，提供友好的对话界面                          |
| **大模型**   | OpenAI GPT 系列（支持 qwen3-max、GPT-4o、GPT-4、GPT-3.5-turbo 等）      |
| **框架**     | LangChain – 构建 RAG 流水线、Agent 与工具调用                           |
| **向量数据库** | Chroma – 轻量级本地向量存储，支持高效相似度检索               |
| **文档处理** | PyPDF、LangChain 文档加载器、文本分割器                      |
| **配置管理** | PyYAML – 读取 YAML 配置文件                                  |
| **日志**     | Python logging 模块，支持文件与控制台输出                    |

---

### 核心特性

- **RAG 检索增强**：文档语义检索与生成结合，回答准确率更高
- **ReAct 智能体**：自主规划、调用工具、多步推理，处理复杂问题
- **多格式文档支持**：自动处理 PDF、TXT 文件，支持增量更新向量库
- **可视化交互**：Streamlit 前端，实时展示智能体思考过程
- **配置驱动**：所有参数（模型、分块大小、检索数量、提示词）通过 YAML 管理
- **模块化设计**：模型工厂、向量存储、工具、中间件解耦，易于扩展
- **中间件机制**：支持请求拦截、日志记录、结果后处理等
- **完整日志**：智能体每一步推理都有日志记录，便于调试

---

### 📁 项目结构

```
AI大模型RAG与智能体开发——Agent项目/
├── app.py                     # Streamlit 前端主程序
├── agent/                     # 智能体核心模块
│   ├── chroma_db/             # 智能体使用的向量库副本（可共享）
│   ├── tools/                 # 智能体可调用的工具
│   │   ├── chroma_db/         # 向量检索工具相关
│   │   ├── agent_tools.py     # 自定义工具（如检索知识库）
│   │   ├── middleware.py      # 智能体中间件
│   │   └── react_agent.py     # ReAct 智能体实现
├── chroma_db/                 # 全局向量数据库（持久化）
├── config/                    # 配置文件目录
│   ├── agent.yml              # 智能体配置（模型、迭代次数、工具列表）
│   ├── chroma.yml             # Chroma 配置（集合名、相似度阈值）
│   ├── prompts.yml            # 提示词配置（路径映射）
│   └── rag.yml                # RAG 配置（分块大小、检索数量）
├── data/                      # 原始数据
│   └── external/              # 扫地机器人知识文档
│       ├── 扫地机器人100问.pdf
│       ├── 扫地机器人100问2.txt
│       ├── 扫拖一体机器人100问.txt
│       ├── 故障排除.txt
│       ├── 维护保养.txt
│       └── 选购指南.txt
├── log/                       # 日志文件目录
├── model/                     # 模型层
│   └── factory.py             # 模型工厂（支持 OpenAI / 本地模型）
├── prompts/                   # 提示词模板文件
│   ├── main_prompt.txt        # 智能体主提示词
│   ├── rag_summarize.txt      # RAG 结果总结提示词
│   └── report_prompt.txt      # 最终报告提示词
├── rag/                       # RAG 检索模块
│   ├── chroma_db/             # 向量库操作封装
│   ├── rag_service.py         # RAG 服务主逻辑
│   └── vector_store.py        # 向量存储抽象类
├── utils/                     # 工具函数
│   ├── config_handler.py      # YAML 配置加载器
│   ├── file_handler.py        # 文件读取与预处理
│   ├── logger_handler.py      # 日志初始化
│   └── path_tool.py           # 跨平台路径处理
└── requirements.txt           # 项目依赖
```

---
### 快速开始

#### 1. 环境准备

- Python 3.9 或更高版本
- 推荐使用虚拟环境

```bash
git clone https://github.com/yourname/ai-rag-agent.git
cd ai-rag-agent
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. 配置 API 密钥

在 `config/agent.yml` 中设置模型参数，推荐通过环境变量管理密钥：

```yaml
# config/agent.yml
model:
  type: "openai"
  model_name: "gpt-4o-mini"
  temperature: 0
  openai_api_key: "${OPENAI_API_KEY}"   # 从环境变量读取
```

导出环境变量：

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

#### 3. 初始化向量数据库

首次运行需将 `data/external/` 下的文档导入 Chroma：

```bash
python -m rag.rag_service --build
```

或通过脚本（若提供）执行。该命令会分割文档、生成嵌入并存入 `chroma_db/` 目录。

#### 4. 启动 Streamlit 应用

```bash
streamlit run app.py
```

浏览器将自动打开 `http://localhost:8501`，即可与智能体进行对话。

#### 5. 命令行测试（可选）

也可以通过命令行直接调用智能体：

```bash
python -m agent.tools.react_agent --query "扫地机器人吸力下降怎么办？"
```

---

### 💬 使用示例

#### Streamlit 界面交互

1. 在输入框中输入问题，例如：“我的扫地机无法开机，请帮我排查原因”
2. 系统会展示智能体的思考过程（Thought → Action → Observation）
3. 最终返回结构化的答案，并附带参考来源

#### 代码调用示例

```python
from agent.tools.react_agent import ReActAgent
from utils.config_handler import load_config

config = load_config("config/agent.yml")
agent = ReActAgent(config)
response = agent.run("如何清理边刷？")
print(response)
```

#### RAG 单独调用

```python
from rag.rag_service import RAGService

rag = RAGService()
docs = rag.retrieve("激光导航 优点")
answer = rag.generate_answer("激光导航有什么优势？", docs)
print(answer)
```

---

### ⚙️ 配置说明

所有配置位于 `config/` 目录，采用 YAML 格式：

- **agent.yml**：智能体行为配置  
  - `max_iterations`：最大推理步数  
  - `tools`：智能体可使用的工具列表  
  - `model`：LLM 模型参数
- **rag.yml**：文档处理参数  
  - `chunk_size`：文本分块大小  
  - `chunk_overlap`：分块重叠  
  - `k`：检索返回的文档数量
- **chroma.yml**：向量数据库参数  
  - `persist_directory`：持久化路径  
  - `collection_name`：集合名称
- **prompts.yml**：提示词模板路径映射，便于切换不同提示词

修改配置后，部分组件（如 RAG 服务）需重启应用才能生效。

---

**🎉 立即体验智能客服，让大模型为你的产品赋能！**
```
