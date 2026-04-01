## 查询
### 数据库操作-查询
核心语句：await db.execute(select(模型类))，返回一个ORM对象

**获取所有数据：**
scalars().all()
**获取单条数据**
scalars().first()

get(模型类，主键类)

```Python
@app.get("/book/books")
async def get_book_list(db:AsyncSession=Depends(get_database)):
  #result=await db.execute(select(Book)) #ORM对象
  #book=result.scalars().all()  #获取所有
  #book=result.scalars().first() #获取单条
  book=await db.get(Book,5)    #获取单条->根据主键
  return book
```
---
### 数据库操作-查询条件
select(Book).where(条件1，条件2，...)

<img width="317" height="222" alt="image" src="https://github.com/user-attachments/assets/3119a9ae-cf2d-465c-8c1b-7df8e7fe27ff" />

#### 查询条件-比较判断
```Python
#查询路径参数 书籍id
@app.get("/book/{book_id}")
async def get_book_list(book_id:int,db:AsyncSession=Depends(get_database))
  result=await db.execute(select(Book).where(Book.id==book_id))
  book=result.scalar_one_or_none()
  return book

#需求：条件 价格大于等于200
@app.get("/book/{book_id}")
async def get_book_list(book_id:int,db:AsyncSession=Depends(get_database))
  result=await db.execute(select(Book).where(Book.price>=200))
  books=result.scalars().all()
  return books
```

#### 查询条件-模糊查询
模糊查询：like %:零个、一个或多个字符
_:一个单个字符
```Python
@app.get("/book/{book_id}")
async def get_book_list(book_id:int,db:AsyncSession=Depends(get_database))
  #result=await db.execute(select(Book).where(Book.author.like("曹%"))
  #result=await db.execute(select(Book).where(Book.author.like("曹_"))
  #result=await db.execute(select(Book).where((Book.author.like("曹%"))&(Book.price>100))
  #result=await db.execute(select(Book).where((Book.author.like("曹%"))|(Book.price>100))
  #需求：书籍id列表，数据库里面的id如果在id数据id列表里面 就返回
  id_list=[1,3,5,7]
  result=await db.execute(select(Book).where(Book.id.in_(id_list)))
  book=result.scalars().all()
  return book
```
---
### 数据库操作-聚合查询
<img width="298" height="223" alt="image" src="https://github.com/user-attachments/assets/8e3e4a3d-73f8-4328-9641-320726ea2e8a" />

select(func.方法名（模型类.属性）)

```Python
@app.get("/book/count")
async def get_book_list(book_id:int,db:AsyncSession=Depends(get_database))
  #result=await db.execute(select(func.count(Book.id)))
  #result=await db.execute(select(func.max(Book.price)))
  #result=await db.execute(select(func.sum(Book.price)))
  result=await db.execute(select(func.avg(Book.price)))
  count=result.scalar() #用来提取一个标量值
  return book
```
---

### 数据库操作-分页查询

<img width="300" height="114" alt="image" src="https://github.com/user-attachments/assets/499d46ec-d1db-478f-8513-b8ef91a86cf5" />

<img width="424" height="191" alt="image" src="https://github.com/user-attachments/assets/6fe34410-4459-4201-94de-bb708b607d78" />

offest值=（当前页码-1）*每页数量limit
```Python
@app.get("/book/get_books")
async def get_book_lidt(
  page:int=1, #要第几页
  page_size:int=3, #每页数据量
  db:AsyncSession=Depends(get_database)
):
  skip=(page-1)*page_size
  stmt=select(Book).offset(skip).limit(page_size)
  result=await db.execute(stmt)
  books=result.scalars().all()
  return {"books":books}
```
---
### 总结
从ORM对象获取数据的方式

<img width="398" height="231" alt="image" src="https://github.com/user-attachments/assets/7dcc43cd-c3b3-4f5c-963a-12c9cd3ceaa8" />


## 新增
核心步骤：定义ORM对象->添加对象到事务：add(对象)->commit 提交到数据库

```Python
from pydantic import BaseModel
#用户输入->参数->请求体
class BooKBase(BaseModel)
  id:int
  bookname:str
  author:str
  price:float
  publisher:str

@app.post("/book/add_book")
async def dd_book(book:BookBase,db:AsyncSession=Depends(get_database)):
  #获取 book 参数
  #ORM对象->add->commit
  book_obj=Book(**book.__dict__)
  db.add(book_obj)
  await db.commit()
  return book
```

## 更新
核心步骤：查询get->属性重新赋值->commit 提交到数据库
```Python
#设计思路：路径参数书籍id:作用是查找；请求体参数：作用是新数据
class BookUpdate(BaseModel):
  bookname:str
  author:str
  price:float
  publisher:str

@app.put("/book/update_book/{book_id}")
async def update_book(book_id:int,data:BookUpdate,db:AsyncSession=Depends(get_database)):
  #1.查询
  book=await db.get(Book,book_id)
  if book is None:
    raise HTTPException(statu_code=404,detail="Book not found")
  #2.修改属性
  book.bookname=data.bookname
  book.author=data.author
  book.price=data.price
  #3.提交
  await db.commit()
  return book
```

## 删除
核心步骤：查询get->delete删除->commit提交到数据库
```Python
@app.delete("/book/delete_book/{book_id}")
aasync def delete_book(book_id:int,db:AsyncSession=Depends(get_database)):
  db_book=await db.get(Book,book_id)
  if db_book is None:
    raise HTTPException(status_code=404,detail="Book not found")
  await db.delete(db_book)
  await db.commit()
  return {"messagq":"Book deleted"}
```
