import json
import psycopg2
from psycopg2.extras import RealDictCursor
import time


from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from models.post import Post
from db.models.posts import Posts
from db.connection import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



TODO: """'# Refactorizar para agregar por modulo y mantener su env""" ""
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="123456",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print(f"Database connection was successfull {cursor}!!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f"An exception occurred {error}")
        time.sleep(2)


@app.get("/")
def get_user():
    return {"Hello": "Mundo!!!"}

@app.get('/sqlalchemy')
def test_posts(db:Session =Depends(get_db)):
    posts = db.query(Posts).all()
    return {'status':"success",
            "data": posts
            }


# Get all posts
@app.get("/posts")
def get_posts(db:Session = Depends(get_db)):
    # cursor.execute("""Select * From posts""")
    # posts = cursor.fetchall()
    posts=db.query(Posts).all()
    print(posts)
    return {"data": posts}


# @app.post("/createposts")
# def create_post(payload: dict = Body(...)):
#     print(f"Esto es el body:{payload}")
#     return {"new_post": f"title:{payload['title']}, content:{payload['content']}"}


# Create Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(f"This is body:{post}")
    # post_dic = post.model_dump()
    # post_dic["id"] = randrange(0, 100000)
    # my_posts.append(post_dic)
    cursor.execute(
        """
                    INSERT INTO posts( title, content, published)
                    values (%s, %s, %s) RETURNING *
                   """,
        (
            post.title,
            post.content,
            post.published,
        ),
    )
    new_post = cursor.fetchone()
    conn.commit()
    print(f"This is dic: {json.dumps(new_post, indent=5, default=str)}")
    return {"message": "created post", "data": new_post}


# Get latest post
@app.get("/posts/latest")
def get_latest_post():
    cursor.execute(
        """
                    Select * From posts
                   """
    )
    posts = cursor.fetchall()
    post = posts[len(posts) - 1]
    return post


# Get post for id
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(
        """
                   Select * from posts where id = %s
                   """,
        (str(id),),
    )
    post = cursor.fetchone()
    # post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"post with id: {id} was not found"},
        )

    print(f"This is post id {post}")
    return {
        "post_detail": post,
    }


# Delete post
@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int):
    cursor.execute(
        """
            Delete from posts where id = %s returning*
        """,
        (str(id),),
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return ({"message": f"Post with id: {id} deleted successfully"},)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts SET title = %s, content = %s, published = %s Where id = %s RETURNING *
        """, (post.title, post.content, post.published, str(id))
    )
    
    updated_post = cursor.fetchone()
    conn.commit()
    print(f"This is dic: {json.dumps(updated_post, indent=5, default=str)}")

    #index = find_index_post(id)
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_dic = post.model_dump()
    # post_dic["id"] = id
    # my_posts[index] = post_dic
    return { "message":"Update Post", "data": post_dic}
