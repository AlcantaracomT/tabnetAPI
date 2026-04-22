from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Categoria(BaseModel):
    idcategoria: int
    nomecategoria: str

class CriarCategoria(BaseModel):
    nomecategoria: str

class TipoCategoria(BaseModel):
    idtipocategoria: int
    nometipocategoria: str
    codcategoria: int

class CriarTipoCategoria(BaseModel):
    nometipocategoria: str
    codcategoria: int

class ProdutoHospitalar(BaseModel):
    id: Optional[int] = None  
    municipio: str
    aih_aprovadas: Optional[int] = None
    internacoes: Optional[int] = None
    valor_total: Optional[float] = None
    valorservicoshospitalares: Optional[float] = None
    valormediointern: Optional[float] = None
    dias_permanencia: Optional[int] = None
    media_permanencia: Optional[float] = None
    obitos: Optional[int] = None
    taxa_mortalidade: Optional[float] = None
    ano: Optional[int] = None
    idtipocategoria: Optional[int] = None

class FiltrosProducaoHospitalar(BaseModel):
    municipio: Optional[str] = None
    ano: Optional[int] = None
    min_internacoes: Optional[int] = None
    max_internacoes: Optional[int] = None
    min_obitos: Optional[int] = None
    max_obitos: Optional[int] = None