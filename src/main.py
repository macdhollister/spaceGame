from fastapi import FastAPI

from src.routes import *

app = FastAPI()

app.include_router(ships.router)
app.include_router(factions.router)
app.include_router(turn.router)
