from random import randrange

from fastapi import FastAPI, Response, status , HTTPException
from typing import Optional

from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/createpost")
# def root():
#     return {"message": "Succesfully recieved"}

#what it does is that it gets the data from the body,
# store it in a dict called payload and then Prints it.
@app.post("/createpost")
def root(payload: dict = Body(...)):
    print(payload)
    return {"message": "Succesfully recieved"}

# class specifies the data type for the input to the frontend. It can be str, int, bool etc

class Post(BaseModel):
    title : str
    content : str
    published : bool = True  # ie default value is true

@app.post("/createpost")
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data" : post}
#Output sample
# title='Hello' content='Yusuf' published=True
# {'title': 'Hello', 'content': 'Yusuf', 'published': True}

my_posts = [
                 {
                     "title" :  "Title 1",
                     "content": "Post 1 content",
                     "id" : 1
                 },
                 {
                     "title" : "title 2",
                     "content" : "Post 2 content",
                     "id" : 2
                 }
]

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data" : "Post added"}

#Getting post by id

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/posts/{id}")
# def get_post(id : int):
#     post = find_post(int(id))
#     return { "Post detail": post}

#Optimized way with exception handling if no post or wrong id input
def get_post(id : int, response : Response):
    post = find_post(int(id))

    if not post:
        # Response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message" : f"Post not available with {id}"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post not available with {id}")

    return {"Post": post}

#Deleting a post
#For deleting a post we have to specify an id or index for the post to be deleted.
#Default 204 for delete

def find_post_index(id):
    for i , p in enumerate (my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post not available with {id}")

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update Post

@app.put("/posts/{id}")
def update_post(id :int, post : Post):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post not available with {id}")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"Data " : "Post updated"}
    






