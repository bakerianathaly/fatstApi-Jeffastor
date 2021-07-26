from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as cleaning_api #Se llama al __init__

def get_application():
    app = FastAPI(title="Phresh", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(cleaning_api, prefix='/api/v1')
    return app

app = get_application()

@app.get("/")
def read_root():
    return {"Hello": "World"}