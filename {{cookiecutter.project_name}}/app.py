from core.endpoints import auth
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

app = FastAPI(title="{{cookiecutter.project_name}}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routes = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)

routes.include_router(auth)
app.include_router(routes)


@app.get("/")
def redirect_to_swagger():
    return RedirectResponse(url="/docs")


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(*args, **kwargs):
    return auth.authjwt_exception_handler(*args, **kwargs)


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(
        "app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
    )
