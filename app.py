from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

import models
from database import engine, session
from schemas import Blog, ShowBlog, User

app_new = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
	db = session()
	try:
		yield db
	finally:
		db.close()


@app_new.post('/blog', status_code=status.HTTP_201_CREATED)
async def create(request: Blog, db: Session = Depends(get_db)):
	new_blog = models.Blog(title=request.title, body=request.body)
	db.add(new_blog)
	db.commit()
	db.refresh(new_blog)
	return new_blog


@app_new.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id, db: Session = Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	if not blog.first():
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'blog with id {id} not found')
	blog.delete()
	db.commit()
	return 'done'


@app_new.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: Blog, db: Session = Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	if not blog.first():
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'blog with id {id} not found')
	blog.update(request.dict())
	db.commit()
	return 'updated'


@app_new.get('/blog', response_model=List[ShowBlog])
async def get_all(db: Session = Depends(get_db)):
	blogs = db.query(models.Blog).all()
	return blogs


@app_new.get('/blog/{id}', status_code=200, response_model=ShowBlog)
async def show(id, response: Response, db: Session = Depends(get_db)):
	blog = db.query(models.Blog).where(models.Blog.id == id).first()
	if not blog:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'Blog with the id {id} is not available')

	return blog


@app_new.post('/user')
def create_user(request: User, db: Session = Depends(get_db)):
	new_user = models.User(
		name=request.name,
		email=request.email,
		password=request.password)
	
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return '[INFO] Create new_user was successfully'
