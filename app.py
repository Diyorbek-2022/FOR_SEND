import redis
from fastapi import FastAPI
from sqladmin import Admin, ModelView

from DataBase.database import engine
# from fastapi_jwt_auth import AuthJWT

from schemas import Settings
# Redis ulanishi

app = FastAPI()
admin = Admin(app, engine)

# @AuthJWT.load_config
# def load_config():
#     return Settings()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)