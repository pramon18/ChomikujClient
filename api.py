import json
from fastapi import FastAPI
from repositories import arquivo_repository
from schemas.arquivo_schema import ArquivoSchema


app = FastAPI()

@app.get("/")
async def root():
    list = arquivo_repository.get_all_arquivos()
    arquivo_schema = ArquivoSchema()
    return [arquivo_schema.dump(x) for x in list]