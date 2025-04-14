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
        "id": 1,
        "title": "Pao",
        "description": "Pao gostosão",
        "author": "Kaayo",
        "content": "ABC",
        "category": 0
    }
]

class Post(BaseModel):
    title: str
    description: str
    author: str
    content: str
    category: int

@app.post("/post")
def create_post(post: Post):
    new_id = posts[-1]["id"] + 1 if posts else 1
    new_post = post.model_dump()
    new_post["id"] = new_id
    posts.append(new_post)
    print(post)
    print(new_post)
    print(posts)
    return {"Message": "Post adicionado com sucesso!", "post": post}

@app.get("/posts")
def get_all_posts():
    return posts

@app.patch("/post/{post_id}")
def update_post(post_id: int, updated_data: dict):
    post_to_update = next((p for p in posts if p["id"] == post_id), None)
    
    for key, value in updated_data.items():
        if key in post_to_update:
            post_to_update[key] = value
    
    return {"message": "Post atualizado com sucesso", "post": post_to_update}

@app.delete("/post/{post_id}")
def delete_post(post_id: int):
    post_index = next((i for i, p in enumerate(posts) if p["id"] == post_id), None)
    print(post_index)
    
    deleted_post = posts.pop(post_index)
    
    return {
        "message": "Post deletado com sucesso",
        "deleted_post": deleted_post
    }
