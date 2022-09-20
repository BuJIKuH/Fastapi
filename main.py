from typing import Optional

import uvicorn
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
	# oly get 10 published blogs

	if published:
		return {'data': f'{limit} published blog from the db'}
	else:
		return {'data': f'{limit} blogs from the db'}


@app.get('/blog/unpublished')
def unpublished():
	return {'data': 'all unpublished blog'}


@app.get('/blog/{id}')
def show(id: int):
	# fetch blog with id = id
	return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id, limit=10):
	# fetch comments of blog with id = id
	return {'data':
		{'id':
			{
				'like': 'like',
				'dislike': 'dislike'
			}
		}
	}


class Blog(BaseModel):
	title: str
	body: str
	published_at: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
	return {'data': f'Blog is created with as {blog.title}'}


if __name__ == "__main__":
	uvicorn.run(app, host='127.0.0.1', port=8000)
