from fastapi import FastAPI, APIRouter
from routers.user import router as user_router
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router=user_router, prefix="/api/v1/user")
