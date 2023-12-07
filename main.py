from fastapi import Depends, FastAPI
from user_crud import router as user_router
from psychologist_crud import router as psy_router
from pairing import router as sched_router
from appointment import router as app_router
from recommendation import router as rec_router
import auth

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")
app.include_router(psy_router, prefix="/psychologist")
app.include_router(sched_router, prefix="/schedule")
app.include_router(app_router, prefix="/appointment")
app.include_router(rec_router, prefix="/recommendation")
app.include_router(auth.router)

@app.get("/")
async def read_item():
    return {"message": "Welcome to Serene App"}
