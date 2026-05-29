from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager
from exceptions import NotFoundException
from employee import router
from exceptions.handlers import register_exception_handlers
from middleware import configureMiddleware


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





def main():
    print("Hello from employee-app!")


if __name__ == "__main__":
    main()
