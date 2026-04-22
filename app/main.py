from fastapi import FastAPI, HTTPException
from typing import List
from .database import conectarAoBanco
from .models import Categoria


app = FastAPI(title="TabAPI")


@app.get("/categoria", response_model=List[Categoria])  
def listarCategoria():
    banco = conectarAoBanco()
    cursor = banco.cursor()

    cursor.execute("SELECT idcategoria, nomecategoria from categoria order by idcategoria;")
    resultados = cursor.fetchall()

    cursor.close()
    banco.close()

    return resultados

@app.get("/categoria/{categoria_id}", response_model=Categoria)
def buscarCategoria(categoria_id: int):
    banco = conectarAoBanco()
    cursor = banco.cursor()

    cursor.execute("SELECT idcategoria, nomecategoria from categoria where idcategoria = %s", (categoria_id,))
    resultados = cursor.fetchall()

    cursor.close()
    banco.close()

    if not resultados:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return resultados