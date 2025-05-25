from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class PartidoUpdate(BaseModel):
    goles_local: Optional[int] = None
    goles_visitante: Optional[int] = None

class PartidoBase(BaseModel):
    temporada_id: int
    fecha: str
    hora: str
    estadio_id: int
    equipo_local: int
    equipo_visitante: int
    goles_local: Optional[int] = 0
    goles_visitante: Optional[int] = 0

class PartidoCreate(PartidoBase):
    pass

class Partido(PartidoBase):
    partido_id: int
    fecha: date
    hora: time
    class Config:
        orm_mode = True

class ParticipaBase(BaseModel):
    partido_id: int
    jugador_id: int

class ParticipaCreate(ParticipaBase):
    pass

class Participa(ParticipaBase):
    class Config:
        orm_mode = True

class GolBase(BaseModel):
    partido_id: int
    jugador_id: int
    minuto: int

class GolCreate(GolBase):
    pass

class Gol(GolBase):
    gol_id: int
    class Config:
        orm_mode = True

class AmonestacionBase(BaseModel):
    partido_id: int
    jugador_id: int
    minuto: int
    tipo: str

class AmonestacionCreate(AmonestacionBase):
    pass

class Amonestacion(AmonestacionBase):
    amonest_id: int
    class Config:
        orm_mode = True 