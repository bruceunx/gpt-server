from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import gemini as gemini_router  # type: ignore
from .routers import groq as groq_router  # type: ignore

app = FastAPI()


@app.get("/")
def main():
    return {"message": "Welcome to the GPT server!"}


# @app.on_event("startup")
# async def startup():
#     await DB.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await DB.disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gemini_router.router, prefix="/gemini", tags=["gemini"])
app.include_router(groq_router.router, prefix="/groq", tags=["groq"])
