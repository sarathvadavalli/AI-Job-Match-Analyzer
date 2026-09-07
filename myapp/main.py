from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from myapp.routes.auth_routes import router as auth_router
from myapp.core.db import close_db, init_db
from myapp.routes.page_routes import router as pages_router
from myapp.routes.document_routes import router as documents_router

app = FastAPI(title="JD Extractor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(documents_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.on_event("shutdown")
def on_shutdown():
    close_db()
