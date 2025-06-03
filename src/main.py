from fastapi import FastAPI
from .app.api import router

app = FastAPI(
    title="Proyecto Final Entregable Henry - Capacitacion Accenture",
    version="1.0"
)

app.include_router(router)