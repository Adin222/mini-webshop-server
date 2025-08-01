from fastapi import FastAPI
from .routes import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "https://vocal-blini-e77de3.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         
    allow_credentials=True,       
    allow_methods=["*"],  
    allow_headers=["*"],           
)

app.include_router(api_router)
