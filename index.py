
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  

from routes.user import user

app = FastAPI()

app.include_router(user)
