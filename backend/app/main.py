from fastapi import FastAPI
from app.routers import floods, subprefecture
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Flood Data API",
    description="API para consulta de dados de alagamentos e subprefeituras.",
    version="1.0.0",
    contact={
        "name": "Equipe Flood Data",
        "email": "fabricionl@al.insper.edu.br",
        "url": "https://flooddata.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens. Use uma lista específica para restringir.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos os cabeçalhos.
)

# Inclusão dos routers
app.include_router(floods.router, prefix="/api", tags=["floods"])
app.include_router(subprefecture.router, prefix="/api", tags=["subprefecture"])


@app.get("/is_alive")
def is_alive():
    return {"message": "alive"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flood Data API"}

