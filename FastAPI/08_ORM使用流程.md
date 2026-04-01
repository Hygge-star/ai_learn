## ORM简介
ORM是一种编程技术，用于在面向对象编程语言和关系型数据库之间建立映射。它允许开发者通过操作对象的方式与数据库进行交互，而无需直接编写复杂的SQL语句

**优势：**
减少重复的SQL代码
代码更简洁易读

**使用流程**
1.安装

2.建库、建表、

3.操作数据

安装
 pip install "sqlalchemy[asyncio]" aiomysql

建表
<img width="985" height="276" alt="image" src="https://github.com/user-attachments/assets/87cc4514-c224-417d-9b46-035c476be739" />

ORM-创建数据库引擎

使用create_async_engine创建异步引擎
```Python
from sqlalchemy.ext.asyncio import create_async_engine
#root:mysql密码
ASYNC_DATABASE_URL="mysql+aiomysql://root:123456@llocalhost:3306/fastapi_test??charset=utf8"
#创建异步引擎
async_engine=create_async_engine(
  ASYNC_DATABASE_URL,
  echo=True,      #可选，输出SQL日志
  pool_size=10,   #设置连接池中保持的持久连接数
  max_overflow=20 #设置连接池允许创建的额外连接数
)
```

ORM-定义模型类

1.基类：集成DeclarativeBase(包含通用属性和字段映射)

2.定义数据库表对应的模型类
```Python
class Base(DeclarativeBase):
  create_time:Mapped[datatime]=mapped_column(
    DataTime,insert_default=func.now(),deefault=datetime.now,commenet="创建时间")
  update_time:Mapped[datatime]=mapped_column(
    DataTime,insert_default=func.now(),onupdate=func.now(),default=datetime.now,comment"修改时间")

class Book(Base):
  __tablename__="book"

  id:Mapped[int]=mapped_column(primary_key=True,comment="书名id")
  bookname:Mapped[str]=apped_column(String(255),comment="书名")
  author:Mapped[str]=mapped_column(String(255)，comment=“作者”)
  price:Mapped[float]=mapped_column(String(255),comment="出版社")
```

ORM-建表
```Python
#建表：定义函数建表->FastAPI 启动的时候调用建表的函数
async def create_tables():
 #获取数据库异步引擎，创建事务，建表
 async_with async_engine.begin() as conn:
   await conn.run_sync(Base.metadata.create_all) #Base 模型类的源数据创建

@app.on_event("startup") #装饰器
async def startup_event(): #定义函数
 await create_tables()
```

ORM-路由匹配中使用ORM
核心：创建依赖项，使用Depend注入到处理函数
```Python
#需求：查询功能的接口，查询图书->依赖注入:创建依赖项获取数据库会话+Depends 注入路由处理函数
#创建异步会话工厂
from sqlalchemy.ext.asyncic import create_async_engine
AsyncSessionLocal=async_sessionmaker(
 bind=async_engine,#绑定数据库引擎
 class=AsyncSession,#指定会话类
 expire_on_commit=Fasle #会话对象不过期，不重新查询数据库
)

#依赖项，用于获取数据库会话
async def get_database():
 async with AsyncSessionLocal() as session:
  try:
    yield session # 返回数据库会话给路由处理函数
    await session.commit() #无异常，提交事务
  except Exception:
    await session.rollback() #有异常则回滚
    raise
  finally:
    await session.close() #关闭会话

@app.get("/book/books")
async def get_book_list(
  db:AsyncSession=Depends(get_database)
):
  #查询所有书籍
  result=await db.execute(select(Book)) #Boook 模型类
  book=result.scalars().all()
  return book
```
