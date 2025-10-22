from contextlib import asynccontextmanager
from typing import AsyncGenerator

from examples.tasker_primitive_obsession.src.presentation.http.dependencies import (
    get_validate_token_use_case,
)
from examples.tasker_primitive_obsession.src.presentation.http.middlewares import (
    TokenHttpAuthMiddleware,
)
from examples.tasker_primitive_obsession.src.presentation.http.routes import (
    task_router,
    user_router,
)
from fastapi import FastAPI

from .exception_handlers import generic_error_handler


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print("🚀 Starting Tasker Primitives Example")
    yield
    print("🛑 Shutting down Tasker Primitives Example")


app = FastAPI(
    title="Tasker Primitives Example",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_exception_handler(Exception, generic_error_handler)

validate_token_use_case = get_validate_token_use_case()

app.add_middleware(
    TokenHttpAuthMiddleware,
    use_case=validate_token_use_case,
)


app.include_router(task_router)
app.include_router(user_router)
