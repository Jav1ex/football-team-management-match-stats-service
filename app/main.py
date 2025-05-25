from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import get_db

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
partidos_router = APIRouter(prefix="/partidos", tags=["Partidos"])
participa_router = APIRouter(prefix="/participa", tags=["Participa"])
goles_router = APIRouter(prefix="/goles", tags=["Goles"])
amonestaciones_router = APIRouter(prefix="/amonestaciones", tags=["Amonestaciones"])

# Partidos
@partidos_router.post("/", response_model=schemas.Partido)
async def create_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    return crud.create_partido(db=db, partido=partido)

@partidos_router.get("/", response_model=List[schemas.Partido])
async def read_partidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    partidos = crud.get_partidos(db, skip=skip, limit=limit)
    return partidos

@partidos_router.get("/{partido_id}", response_model=schemas.Partido)
async def read_partido(partido_id: int, db: Session = Depends(get_db)):
    partido = crud.get_partido(db, partido_id=partido_id)
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@partidos_router.delete("/{partido_id}")
async def delete_partido(partido_id: int, db: Session = Depends(get_db)):
    if crud.delete_partido(db, partido_id=partido_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Partido no encontrado")

@partidos_router.patch("/{partido_id}", response_model=schemas.Partido)
async def update_partido(partido_id: int, partido: schemas.PartidoUpdate, db: Session = Depends(get_db)):
    updated_partido = crud.update_partido_score(db, partido_id=partido_id, partido=partido)
    if updated_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado o no hay datos para actualizar")
    return updated_partido

# Participa
@participa_router.post("/", response_model=schemas.Participa)
async def create_participa(participa: schemas.ParticipaCreate, db: Session = Depends(get_db)):
    return crud.create_participa(db=db, participa=participa)

@participa_router.get("/", response_model=List[schemas.Participa])
async def read_participa(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_participa_list(db, skip=skip, limit=limit)

@participa_router.get("/{partido_id}/{jugador_id}", response_model=schemas.Participa)
async def read_participa_item(partido_id: int, jugador_id: int, db: Session = Depends(get_db)):
    participa = crud.get_participa(db, partido_id=partido_id, jugador_id=jugador_id)
    if participa is None:
        raise HTTPException(status_code=404, detail="Participa no encontrado")
    return participa

@participa_router.delete("/{partido_id}/{jugador_id}")
async def delete_participa(partido_id: int, jugador_id: int, db: Session = Depends(get_db)):
    if crud.delete_participa(db, partido_id=partido_id, jugador_id=jugador_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Participa no encontrado")

# Goles
@goles_router.post("/", response_model=schemas.Gol)
async def create_gol(gol: schemas.GolCreate, db: Session = Depends(get_db)):
    return crud.create_gol(db=db, gol=gol)

@goles_router.get("/", response_model=List[schemas.Gol])
async def read_goles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    goles = crud.get_goles(db, skip=skip, limit=limit)
    return goles

@goles_router.get("/{gol_id}", response_model=schemas.Gol)
async def read_gol(gol_id: int, db: Session = Depends(get_db)):
    gol = crud.get_gol(db, gol_id=gol_id)
    if gol is None:
        raise HTTPException(status_code=404, detail="Gol no encontrado")
    return gol

@goles_router.delete("/{gol_id}")
async def delete_gol(gol_id: int, db: Session = Depends(get_db)):
    if crud.delete_gol(db, gol_id=gol_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Gol no encontrado")

# Amonestaciones
@amonestaciones_router.post("/", response_model=schemas.Amonestacion)
async def create_amonestacion(amonestacion: schemas.AmonestacionCreate, db: Session = Depends(get_db)):
    return crud.create_amonestacion(db=db, amonestacion=amonestacion)

@amonestaciones_router.get("/", response_model=List[schemas.Amonestacion])
async def read_amonestaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    amonestaciones = crud.get_amonestaciones(db, skip=skip, limit=limit)
    return amonestaciones

@amonestaciones_router.get("/{amonest_id}", response_model=schemas.Amonestacion)
async def read_amonestacion(amonest_id: int, db: Session = Depends(get_db)):
    amonestacion = crud.get_amonestacion(db, amonest_id=amonest_id)
    if amonestacion is None:
        raise HTTPException(status_code=404, detail="Amonestación no encontrada")
    return amonestacion

@amonestaciones_router.delete("/{amonest_id}")
async def delete_amonestacion(amonest_id: int, db: Session = Depends(get_db)):
    if crud.delete_amonestacion(db, amonest_id=amonest_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Amonestación no encontrada")

# Incluir routers
app.include_router(partidos_router)
app.include_router(participa_router)
app.include_router(goles_router)
app.include_router(amonestaciones_router) 