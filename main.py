from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

posts = [
    {
        "id": 1,
        "title": "Pao",
        "description": "Paozao",
        "author": "Kaayo",
        "content": "ABC",
        "category": "IA na Arte e Cultura",
        "image_url": '/uploads/bread.jpg'
    },
    {
        "id": 2,
        "title": "Pao",
        "description": "Paozao",
        "author": "Kaayo",
        "content": "ABC",
        "category": "IA na Arte e Cultura",
        "image_url": '/uploads/bread.jpg'
    },
    {
        "id": 3,
        "title": "Pao",
        "description": "Paozao",
        "author": "Kaayo",
        "content": "ABC",
        "category": "IA na Arte e Cultura",
        "image_url": '/uploads/bread.jpg'
    },
    ]

class PostBase(BaseModel):
    title: str
    description: str
    author: str
    content: str
    category: str
    image_url: Optional[str] = None

@app.post("/post")
async def create_post(
    title: str = Form(...),
    description: str = Form(...),
    author: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    image: Optional[UploadFile] = File(None)
):

    image_url = None
    if image:
        file_ext = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as buffer:
            buffer.write(await image.read())
        
        image_url = f"/uploads/{filename}"

    new_id = posts[-1]["id"] + 1 if posts else 1
    new_post = {
        "id": new_id,
        "title": title,
        "description": description,
        "author": author,
        "content": content,
        "category": category,
        "image_url": image_url
    }
    
    posts.append(new_post)
    
    return {
        "message": "Post criado com sucesso!",
        "post": new_post
    }

@app.get("/posts")
def get_all_posts():
    return posts

@app.put("/post/{post_id}")
def update_post(post_id: int, updated_data: dict):
    post_to_update = next((p for p in posts if p["id"] == post_id), None)
    
    for key, value in updated_data.items():
        if key in post_to_update:
            post_to_update[key] = value
    
    return {"message": "Post atualizado com sucesso", "post": post_to_update}

@app.delete("/post/{post_id}")
def delete_post(post_id: int):
    post_index = next((i for i, p in enumerate(posts) if p["id"] == post_id), None)
    
    if post_index is not None:
        deleted_post = posts.pop(post_index)
        return {
            "message": "Post deletado com sucesso",
            "deleted_post": deleted_post
        }
    return {"message": "Post não encontrado"}
