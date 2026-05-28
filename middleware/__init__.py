from middleware.logging import RequestLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware

def configureMiddleware(FastApi)->None:
    FastApi.add_middleware(RequestLoggingMiddleware)
    FastApi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)