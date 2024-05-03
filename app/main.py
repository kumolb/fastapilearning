from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(host="localhost", database = "fastapi", user = "postgres", password="kumol254", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connect db successfull")
        break
    except Exception as error: 
        print("Error while connect db")
        print(error)
        time.sleep(2)


app = FastAPI()
mypost = [{"title": "Title 1", "content": "Content of post 1", "id": 1}]
class Item(BaseModel):
    price: int
    title: str | None = Field(default = None, title="The description of the item")
    quantity: int | None = 0

class Post(BaseModel):
    title: str | None = ""
    content: str | None = Field(default="h", content = "String required")
    published: bool = True

@app.post("/post/{item_id}")
async def savePost(item_id: int, item: Annotated[Item, Body(embed=True)]):
    return item

@app.get("/posts")
async def getPosts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {
        "success": True,
        "status": 200,
        "body": posts
    }
@app.post("/createpost")
async def createPost(post: Post): #dict = Body(...)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    newPost = cursor.fetchone()
    conn.commit()
    return {
        "success": True,
        "status": 200,
        "body": newPost
    }

@app.get("/posts/{id}")
async def getPost(id:int):
    post = None
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if post: 
        return {
            "success": True,
            "status": 200,
            "body": post
        }
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"NO content found by this id = {id}")
    

@app.delete("/posts/{id}")
async def deletePost(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()

    if post:
        return {
            "success": True,
            "status": 200,
            "body": post
        }
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No content found by this id = {id}")
    
@app.put("/posts/{id}")
async def updatePost(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
    newPost = cursor.fetchone()
    conn.commit()
    if newPost:
        return{
            "success": True,
            "status": 200,
            "body": newPost
        }
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"There is an error while updating posts by id ${id}") 
    #4:47