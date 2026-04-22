from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from psycopg2.extras import RealDictCursor

from .database import conexao, liberarConexao
from .models import Categoria, TipoCategoria, ProdutoHospitalar
from .auth import verificarChaveAPI

app = FastAPI(dependencies=[Depends(verificarChaveAPI)], title="TabAPI")


@app.get("/categoria", response_model=List[Categoria])  
def listarCategoria():
    banco = conexao()
    cursor = banco.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT idcategoria, nomecategoria FROM categoria ORDER BY idcategoria;")
    resultados = cursor.fetchall()

    cursor.close()
    liberarConexao(banco)

    return resultados

@app.get("/categoria/{categoria_id}", response_model=Categoria)
def buscarCategoria(categoria_id: int):
    banco = conexao()
    cursor = banco.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT idcategoria, nomecategoria FROM categoria WHERE idcategoria = %s", (categoria_id,))
    resultados = cursor.fetchall()

    cursor.close()
    liberarConexao(banco)

    if not resultados:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return resultados

@app.get("/tipoCategoria", response_model=List[TipoCategoria])
def listarTipoCategoria():
    banco = conexao()
    cursor = banco.cursor(cursor_factory=RealDictCursor)

    cursor.execute("" \
        "SELECT tc.idtipocategoria, tc.nometipocategoria, tc.codcategoria, c.nomecategoria as categoria_nome " \
        "FROM tipo_categoria tc " \
        "JOIN categoria c ON tc.codcategoria = c.idcategoria " \
        "ORDER BY tc.idtipocategoria"
    )

    resultados = cursor.fetchall()

    cursor.close()
    liberarConexao(banco)

    return resultados

@app.get("/tipoCategoria/{tipo_id}", response_model=TipoCategoria)
def buscarTipoCategoria(tipo_id: int):
    banco = conexao()
    cursor = banco.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT idtipocategoria, nometipocategoria, codcategoria FROM tipo_categoria WHERE idtipocategoria= %s", (tipo_id,))
    resultados = cursor.fetchall()

    cursor.close()
    liberarConexao(banco)

    if not resultados:
        raise HTTPException(status_code= 404, detail= "Tipo de categoria não encontrado")
    return resultados

@app.get("/producaoHospitalar", response_model=List[ProdutoHospitalar])
def listarProducaoHospitalar(
    limit: int = Query(100, ge=1, le=419),
    offset: int= Query(0, ge=0),
    municipio: Optional[str] = None,
    ano: Optional[int] = None,
    min_internacoes: Optional[int] = None,
    max_internacoes: Optional[int] = None
):
    banco = conexao()
    cursor = banco.cursor(cursor_factory=RealDictCursor)

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
    liberarConexao(banco)

    return resultados

@app.get("/producaoHospitalar/{municipio}")
def buscarMunicipio(municipio: str):
    banco = conexao()
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
    liberarConexao(banco)

    if not resultados:
        raise HTTPException(status_code=404, detail=f"Muncipio {municipio} não encontrado")
    return resultados

