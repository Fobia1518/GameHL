from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import videos, feedback

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Gameplay Highlights API",
    description="Sistema automático de generación de highlights para videos de gameplay",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix="/videos", tags=["Videos"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])

@app.get("/docs", include_in_schema=False)
async def custom_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Gameplay Highlights API",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "monokai",
            "layout": "BaseLayout",
            "docExpansion": "list",
        },
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.17.14/swagger-ui.css",
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.17.14/swagger-ui-bundle.js",
    )

@app.get("/")
def root():
    return {
        "message": "Gameplay Highlights API funcionando",
        "docs": "/docs",
        "version": "1.0.0"
    }