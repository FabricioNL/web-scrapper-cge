from fastapi import FastAPI
from app.routers import floods
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens. Use uma lista específica para restringir.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos os cabeçalhos.
)

app.include_router(floods.router, prefix="/api", tags=["floods"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flood Data API"}
