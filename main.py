from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager
from exceptions import NotFoundException
from employee import router
from exceptions.handlers import register_exception_handlers
from middleware import configureMiddleware
from auth import auth_router
from department import dept_router
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_tables()
    yield



app = FastAPI(
    title="Employee CRUD Application",
    description="Simple Employee management software",
    version="1.0.0",
    # lifespan=lifespan
)


configureMiddleware(app)

register_exception_handlers(app)

app.include_router(router)

app.include_router(auth_router)
app.include_router(dept_router)


def main():
    print("Hello from employee-app!")


if __name__ == "__main__":
    main()
