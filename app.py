from fastapi import FastAPI
from db import Base , engine
from route import route
from model import model

Base.metadata.create_all(engine)

app = FastAPI(title="Ratish DevOps CI/CD API")
app.include_router(route.router)




