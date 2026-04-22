from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

chaveAPI = os.getenv("CHAVE_API")

def verificarChaveAPI(chave: str= Header(...)):
    if chave != chaveAPI:
        raise HTTPException(status_code=401, detail="Chave da API invalida")