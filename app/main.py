from fastapi import FastAPI, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from logging.config import dictConfig
from app.router import todo, user, assign
from config.logconf import log_config, LOGGER_NAME
from config.conf import settings
# from fastapi_redis_cache import FastApiRedisCache, cache
from sqlalchemy.orm import Session
from .database import db_init

dictConfig(log_config)
app = FastAPI(title="Fast with Docker", debug=True)

app = FastAPI()
log = logging.getLogger(LOGGER_NAME)

# handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(todo.router, tags=['Todos'], prefix='/api/todos')
app.include_router(assign.router, tags=['Tasks', ], prefix='/api/assign')
app.include_router(user.router, tags=['Auth', ], prefix='/api/auth')

@app.get("/")
# @cache()
async def index() -> dict:
    return {"message": "Hello you are home"}

@app.get("/api/")
# @cache()
async def index() -> dict:
    return {"message": "Hello you are home"}


@app.get("/api/ping/", status_code=status.HTTP_200_OK)
def get_ping():
    dtime = datetime.now()
    return {"message": "Hello! pong", "time": "time: {}".format(dtime) }


@app.on_event('startup')
async def startup():
    db_init()
    # log.debug(settings.db_url)
    # if not database.is_connected:
    #     await database.connect()
    #     log.info("DB connected successfully")
    
    # await TUser.objects.get_or_create(email='jane123@mail.com')

    # redis_cache = FastApiRedisCache()
    # redis_cache.init(
    #     host_url=settings.redis_url,
    #     # host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
    #     prefix="todo-cache",
    #     response_header="X-MyAPI-Cache",
    #     ignore_arg_types=[Request, Response, Session]
    # )
    pass


@app.on_event('shutdown')
async def shutdown():
    # if database.is_connected():
    #     await database.disconnect()
    #     log.info("DB disconnected successfully")
    pass