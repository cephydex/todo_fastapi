from fastapi import APIRouter, status, Depends
import logging
from config.logconf import LOGGER_NAME
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from app.auth.auth_bearer import JWTBearer
from typing import List
from config.conf import settings

router = APIRouter(
    dependencies=[ Depends(JWTBearer()) ],
    responses={404: {"description": "Not found"}},
)
log = logging.getLogger(LOGGER_NAME)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_assignments(db: Session = Depends(get_db)):
    
    todos = (
        db.query(models.Todo, models.User)
            .with_entities(
                models.User.id.label('user_id')
                , models.Todo.id.label('todo_id')
                , models.Todo.title
                , models.Todo.content
                , models.Todo.category
                , models.Todo.created_at
            )
            .filter(
                models.user_todo.c.todo_id == models.Todo.id,
                models.user_todo.c.user_id == models.User.id
            )        
            .order_by(models.Todo.created_at)
            .all()
    )

    log.info("Todo assignments retrieved")
    return {"message": "Todo assignments retrieved!", 'data': todos, 'success': True}


@router.get("/{userId}", status_code=status.HTTP_200_OK)
async def get_user_todos(userId: str, db: Session = Depends(get_db)):
    
    result = (
        db.query(models.Todo, models.User)
        .with_entities(
            models.User.id.label('user_id')
            , models.Todo.id.label('todo_id')
            , models.Todo.title
            , models.Todo.content
            , models.Todo.category
            , models.Todo.created_at
        )
        .filter(
            models.user_todo.c.user_id == userId, 
            models.user_todo.c.todo_id == models.Todo.id,
            models.user_todo.c.user_id == models.User.id
        )        
        .order_by(models.Todo.created_at)
        .all()
    )

    log.info("Todo assignments retrieved for user: "+ userId)
    return {"message": "Todo assignments retrieved!", 'data': result, 'success': True}


@router.post("/{userId}", status_code=status.HTTP_201_CREATED)
async def assign_todo(userId: str, data: List[str], db: Session = Depends(get_db)):
    user = db.query(models.User).get(int(userId))
    max_assign = int(settings.max_assigned)
    data_count = len(data)
    message = "Sorry assignment not completed"
    # todoId = int(todoId)
    # log.warn("MA assign: {max_assign}")
    # return {"data": max_assign}

    if data_count <= max_assign and data_count > 1:
        # remove assignments
        user.todos = []
        db.commit()

        for todoId in data:
            todo = db.query(models.Todo).get(todoId)
            
            # check for empty todo object
            if todo is not None:
                user.todos .append(todo)
                
        db.add(user)
        db.commit()
        db.refresh(user)
        log.info(f"Todos asigned to {user} successfully")
        message = "Todo updated successfully!"
    else:
        message = "Sorry assignment has reached max limit"

    return {"message": message, 'success': True}


@router.delete("/{userId}", status_code=status.HTTP_200_OK)
async def unassign_todo(userId: str, db: Session = Depends(get_db)):
    user = (
                db.query(models.User)
                    .filter(models.User.id == userId)
                    .first()
            )
    # reset mapping
    user.todos = []
    db.commit()

    log.info("Assigned todos removed for user with Id: {userId}")
    return {'message': "Todos removed successfully!", "data": user, 'success': True}