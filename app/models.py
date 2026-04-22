from pydantic import BaseModel
from typing import Optional

class Categoria(BaseModel):
    idcategoria: int
    nomecategoria: str


class TipoCategoria(BaseModel):
    idtipocategoria: int
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
