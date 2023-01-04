create .env file with the following configs:
DATABASE_URL='postgresql+psycopg2://username:password@host:db_port/db'
secret=secret_word
algorithm=HS256

RUN:
navigate to the "src" folder
CMD: uvicorn app.main:app