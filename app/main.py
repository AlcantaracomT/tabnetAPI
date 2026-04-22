from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from .database import conectarAoBanco
from .models import Categoria, TipoCategoria, ProdutoHospitalar


app = FastAPI(title="TabAPI")


@app.get("/categoria", response_model=List[Categoria])  
def listarCategoria():
    banco = conectarAoBanco()
    cursor = banco.cursor()

    cursor.execute("SELECT idcategoria, nomecategoria FROM categoria ORDER BY idcategoria;")
    resultados = cursor.fetchall()

    banco.close()
    cursor.close()

    return resultados

@app.get("/categoria/{categoria_id}", response_model=Categoria)
def buscarCategoria(categoria_id: int):
    banco = conectarAoBanco()
    cursor = banco.cursor()

    cursor.execute("SELECT idcategoria, nomecategoria FROM categoria WHERE idcategoria = %s", (categoria_id,))
    resultados = cursor.fetchall()

    banco.close()
    cursor.close()

    if not resultados:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return resultados

@app.get("/tipoCategoria", response_model=List[TipoCategoria])
def listarTipoCategoria():
    banco= conectarAoBanco()
    cursor= banco.cursor()

    cursor.execute("" \
        "SELECT tc.idtipocategoria, tc.nometipocategoria, tc.codcategoria, c.nomecategoria as categoria_nome " \
        "FROM tipo_categoria tc " \
        "JOIN categoria c ON tc.codcategoria = c.idcategoria " \
        "ORDER BY tc.idtipocategoria"
    )

    resultados = cursor.fetchall()

    cursor.close()
    banco.close()

    return resultados

@app.get("/tipoCategoria/{tipo_id}", response_model=TipoCategoria)
def buscarTipoCategoria(tipo_id: int):
    banco = conectarAoBanco()
    cursor = banco.cursor()

    cursor.execute("SELECT idtipocategoria, nometipocategoria, codcategoria FROM tipo_categoria WHERE idtipocategoria= %s", (tipo_id))
    resultados = cursor.fetchall()

    cursor.close()
    banco.close()

    if not resultados:
        raise HTTPException(status_code= 404, detail= "Tipo de categoria não encontrado")
    return resultados

@app.get("/producaoHospitalar", response_model=List[ProdutoHospitalar])
def listarProducaoHospitalar(
    limit: int = Query(100, ge=1, le=100),
    offset: int= Query(0, ge=0),
    municipio: Optional[str] = None,
    ano: Optional[int] = None,
    min_internacoes: Optional[int] = None,
    max_internacoes: Optional[int] = None
):
    banco = conectarAoBanco()
    cursor = banco.cursor()

    query= """
        SELECT id, municipio, aih_aprovadas, internacoes, valor_total,
        valorservicoshospitalares, valormediointern, dias_permanencia,
        media_permanencia, obitos, taxa_mortalidade, ano, idtipocategoria
        FROM producao_hospitalar 
        WHERE 1=1
        """
    
    parametro = []

    if municipio:
        query += " AND municipio ILIKE %s"
        parametro.append(f"%{municipio}%")

    if ano:
        query += " AND ano = %s"
        parametro.append(ano)

    if min_internacoes:
        query += " AND internacoes >= %s"
        parametro.append(min_internacoes)

    if max_internacoes:
        query += " AND internacoes <= %s"
        parametro.append(max_internacoes)

    query += " ORDER BY municipio LIMIT %s OFFSET %s"
    parametro.append(limit)
    parametro.append(offset)

    cursor.execute(query, parametro)
    resultados = cursor.fetchall()

    cursor.close()
    banco.close()

    return resultados

@app.get("/producaoHospitalar/{municipio}")
def buscarMunicipio(municipio: str):
    banco = conectarAoBanco()
    cursor= banco.cursor()

    cursor.execute("""
        SELECT id, municipio, aih_aprovadas, internacoes, valor_total,
        valorservicoshospitalares, valormediointern, dias_permanencia,
        media_permanencia, obitos, taxa_mortalidade, ano
        FROM producao_hospitalar
        WHERE municipio ILIKE %s;
        """, (f"%{municipio}%",)
    )

    resultados = cursor.fetchall()

    cursor.close()
    banco.close()

    if not resultados:
        raise HTTPException(status_code=404, detail=f"Muncipio {municipio} não encontrado")
    return resultados

