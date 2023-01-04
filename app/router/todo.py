from fastapi import APIRouter, status, Depends
import logging
from config.logconf import LOGGER_NAME
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    dependencies=[ Depends(JWTBearer()) ],
    responses={404: {"description": "Not found"}},
)
log = logging.getLogger(LOGGER_NAME)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(db: Session = Depends(get_db), limit:int = 10):
    log.info("Todos retrieved")
    todos = db.query(models.Todo).limit(limit).all()
    return {"message": "Todo retrieved!", 'data': todos, 'success': True}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: schemas.TodoInsertSchema, db: Session = Depends(get_db)):
    new_todo = models.Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    log.info("Todo created")    
    return {"message": "Todo created successfully!", 'data': new_todo, 'success': True}


@router.patch("/{todoId}", status_code=status.HTTP_200_OK)
async def update_todo(todoId: str, todo: schemas.TodoInsertSchema, db: Session = Depends(get_db)):
    _todo = db.query(models.Todo).get(int(todoId))
    _todo.title = todo.title
    _todo.content = todo.content

    if todo is not None and todo.category is not None:
        _todo.category = todo.category
    
    db.add(_todo)
    db.commit()
    db.refresh(_todo)

    log.info("Todo updated")
    return {"message": "Todo updated successfully!", "data": _todo, 'success': True}


@router.get("/{todoId}", status_code=status.HTTP_200_OK)
async def get_todo(todoId: str, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(int(todoId))

    log.info("Todo fetched successfully")
    return {"message": "Todo retrieved successfully!", "data": todo, 'success': True}


@router.delete("/{todoId}", status_code=status.HTTP_200_OK)
async def delete_todo(todoId: str, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(int(todoId))

    db.delete(todo)
    db.commit()
    log.info("Todo deleted with ID:%d deleted".format(todoId))
    return {'message': "Todo deleted successfully!", "data": todoId, 'success': True}