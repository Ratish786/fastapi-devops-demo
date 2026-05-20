from fastapi import FastAPI
from db import Base , engine
from route import route
from model import model

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(route.router)




