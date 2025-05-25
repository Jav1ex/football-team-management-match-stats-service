from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .database import database
from . import models, schemas
from datetime import date, time
from .schemas import PartidoUpdate

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

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Partidos
@partidos_router.post("/", response_model=schemas.Partido)
async def create_partido(partido: schemas.PartidoCreate):
    data = partido.dict()
    data["fecha"] = date.fromisoformat(data["fecha"])
    data["hora"] = time.fromisoformat(data["hora"])
    query = models.partido.insert().values(**data)
    last_id = await database.execute(query)
    return {**partido.dict(), "partido_id": last_id}

@partidos_router.get("/", response_model=List[schemas.Partido])
async def read_partidos():
    query = models.partido.select()
    return await database.fetch_all(query)

@partidos_router.get("/{partido_id}", response_model=schemas.Partido)
async def read_partido(partido_id: int):
    query = models.partido.select().where(models.partido.c.partido_id == partido_id)
    partido = await database.fetch_one(query)
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@partidos_router.delete("/{partido_id}")
async def delete_partido(partido_id: int):
    query = models.partido.delete().where(models.partido.c.partido_id == partido_id)
    result = await database.execute(query)
    return {"deleted": result}

@partidos_router.patch("/{partido_id}", response_model=schemas.Partido)
async def update_partido(partido_id: int, partido: schemas.PartidoUpdate):
    query = models.partido.select().where(models.partido.c.partido_id == partido_id)
    db_partido = await database.fetch_one(query)
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    update_data = partido.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    update_query = (
        models.partido.update()
        .where(models.partido.c.partido_id == partido_id)
        .values(**update_data)
    )
    await database.execute(update_query)
    # Devolver el partido actualizado
    query = models.partido.select().where(models.partido.c.partido_id == partido_id)
    return await database.fetch_one(query)

# Participa
@participa_router.post("/", response_model=schemas.Participa)
async def create_participa(participa: schemas.ParticipaCreate):
    query = models.participa.insert().values(**participa.dict())
    await database.execute(query)
    return participa

@participa_router.get("/", response_model=List[schemas.Participa])
async def read_participa():
    query = models.participa.select()
    return await database.fetch_all(query)

@participa_router.get("/{partido_id}/{jugador_id}", response_model=schemas.Participa)
async def read_participa_item(partido_id: int, jugador_id: int):
    query = models.participa.select().where(
        (models.participa.c.partido_id == partido_id) &
        (models.participa.c.jugador_id == jugador_id)
    )
    participa = await database.fetch_one(query)
    if participa is None:
        raise HTTPException(status_code=404, detail="Participa no encontrado")
    return participa

@participa_router.delete("/{partido_id}/{jugador_id}")
async def delete_participa(partido_id: int, jugador_id: int):
    query = models.participa.delete().where(
        (models.participa.c.partido_id == partido_id) &
        (models.participa.c.jugador_id == jugador_id)
    )
    result = await database.execute(query)
    return {"deleted": result}

# Goles
@goles_router.post("/", response_model=schemas.Gol)
async def create_gol(gol: schemas.GolCreate):
    query = models.gol.insert().values(**gol.dict())
    last_id = await database.execute(query)
    return {**gol.dict(), "gol_id": last_id}

@goles_router.get("/", response_model=List[schemas.Gol])
async def read_goles():
    query = models.gol.select()
    return await database.fetch_all(query)

@goles_router.get("/{gol_id}", response_model=schemas.Gol)
async def read_gol(gol_id: int):
    query = models.gol.select().where(models.gol.c.gol_id == gol_id)
    gol = await database.fetch_one(query)
    if gol is None:
        raise HTTPException(status_code=404, detail="Gol no encontrado")
    return gol

@goles_router.delete("/{gol_id}")
async def delete_gol(gol_id: int):
    query = models.gol.delete().where(models.gol.c.gol_id == gol_id)
    result = await database.execute(query)
    return {"deleted": result}

# Amonestaciones
@amonestaciones_router.post("/", response_model=schemas.Amonestacion)
async def create_amonestacion(amonestacion: schemas.AmonestacionCreate):
    query = models.amonestacion.insert().values(**amonestacion.dict())
    last_id = await database.execute(query)
    return {**amonestacion.dict(), "amonest_id": last_id}

@amonestaciones_router.get("/", response_model=List[schemas.Amonestacion])
async def read_amonestaciones():
    query = models.amonestacion.select()
    return await database.fetch_all(query)

@amonestaciones_router.get("/{amonest_id}", response_model=schemas.Amonestacion)
async def read_amonestacion(amonest_id: int):
    query = models.amonestacion.select().where(models.amonestacion.c.amonest_id == amonest_id)
    amonestacion = await database.fetch_one(query)
    if amonestacion is None:
        raise HTTPException(status_code=404, detail="Amonestación no encontrada")
    return amonestacion

@amonestaciones_router.delete("/{amonest_id}")
async def delete_amonestacion(amonest_id: int):
    query = models.amonestacion.delete().where(models.amonestacion.c.amonest_id == amonest_id)
    result = await database.execute(query)
    return {"deleted": result}

# Incluir routers
app.include_router(partidos_router)
app.include_router(participa_router)
app.include_router(goles_router)
app.include_router(amonestaciones_router) 