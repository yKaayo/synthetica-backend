from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

posts = [
    {
        "title": "Pao",
        "description": "Pao gostosão",
        "author": "Kaayo"
    }
]

class Post(BaseModel):
    title: str
    description: str
    author: str

@app.post("/post")
def create_post(post: Post):
    posts.append(post)
    print(post)
    return {"Message": "Post adicionado com sucesso!", "post": post}

@app.get("/posts")
def get_all_posts():
    return posts
