### 要点
**为什么要创建虚拟环境？**
隔离项目运行环境，避免依赖冲突，保持全局环境的干净和稳定

**怎么运行FastAPI项目**
run项目
uvicorn main:app --reload
--reload:更改代码后自动重启服务器

**怎么访问FastAPI交互式文档？**
http://127.0.0:18000/docs

代码
```python
from fastapi import FastAPI
#创建FastAPI实例
app = FastAPI()

@app.get("/")
async def root(): #异步函数
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
```
