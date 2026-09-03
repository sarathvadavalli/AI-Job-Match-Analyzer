from fastapi import FastAPI
from myapp.routes import router as documents_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FIRST PROJECT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)