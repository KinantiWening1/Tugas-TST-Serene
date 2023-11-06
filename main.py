from fastapi import FastAPI
from user_crud import router as user_router
from psychologist_crud import router as psy_router
from schedule import router as sched_router


app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(psy_router, prefix="/psychologist")
app.include_router(sched_router, prefix="/schedule")

@app.get("/")
async def read_item():
    return {"message": "Welcome to Serene App"}