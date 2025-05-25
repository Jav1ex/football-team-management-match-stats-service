from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date, time

# Partidos
def get_partido(db: Session, partido_id: int):
    return db.query(models.partido).filter(models.partido.c.partido_id == partido_id).first()

def get_partidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.partido).offset(skip).limit(limit).all()

def create_partido(db: Session, partido: schemas.PartidoCreate):
    db_partido = dict(partido.dict())
    db_partido["fecha"] = date.fromisoformat(db_partido["fecha"])
    db_partido["hora"] = time.fromisoformat(db_partido["hora"])
    result = db.execute(models.partido.insert().values(**db_partido))
    db.commit()
    db_partido['partido_id'] = result.inserted_primary_key[0]
    return db_partido

def update_partido_score(db: Session, partido_id: int, partido: schemas.PartidoUpdate):
    db_partido = db.query(models.partido).filter(models.partido.c.partido_id == partido_id).first()
    if not db_partido:
        return None
    
    update_data = partido.dict(exclude_unset=True)
    
    if update_data:
        db.query(models.partido).filter(models.partido.c.partido_id == partido_id).update(update_data)
        db.commit()
        return db.query(models.partido).filter(models.partido.c.partido_id == partido_id).first()
    return None

def delete_partido(db: Session, partido_id: int):
    db_partido = get_partido(db, partido_id)
    if not db_partido:
        return False
    db.execute(models.partido.delete().where(models.partido.c.partido_id == partido_id))
    db.commit()
    return True

# Participa
def get_participa(db: Session, partido_id: int, jugador_id: int):
    return db.query(models.participa).filter(
        models.participa.c.partido_id == partido_id,
        models.participa.c.jugador_id == jugador_id
    ).first()

def get_participa_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.participa).offset(skip).limit(limit).all()

def create_participa(db: Session, participa: schemas.ParticipaCreate):
    db_participa = dict(participa.dict())
    db.execute(models.participa.insert().values(**db_participa))
    db.commit()
    return db_participa

def delete_participa(db: Session, partido_id: int, jugador_id: int):
    db_participa = get_participa(db, partido_id, jugador_id)
    if not db_participa:
        return False
    db.execute(models.participa.delete().where(
        (models.participa.c.partido_id == partido_id) &
        (models.participa.c.jugador_id == jugador_id)
    ))
    db.commit()
    return True

# Goles
def get_gol(db: Session, gol_id: int):
    return db.query(models.gol).filter(models.gol.c.gol_id == gol_id).first()

def get_goles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.gol).offset(skip).limit(limit).all()

def create_gol(db: Session, gol: schemas.GolCreate):
    db_gol = dict(gol.dict())
    result = db.execute(models.gol.insert().values(**db_gol))
    db.commit()
    db_gol['gol_id'] = result.inserted_primary_key[0]
    return db_gol

def delete_gol(db: Session, gol_id: int):
    db_gol = get_gol(db, gol_id)
    if not db_gol:
        return False
    db.execute(models.gol.delete().where(models.gol.c.gol_id == gol_id))
    db.commit()
    return True

# Amonestaciones
def get_amonestacion(db: Session, amonest_id: int):
    return db.query(models.amonestacion).filter(models.amonestacion.c.amonest_id == amonest_id).first()

def get_amonestaciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.amonestacion).offset(skip).limit(limit).all()

def create_amonestacion(db: Session, amonestacion: schemas.AmonestacionCreate):
    db_amonestacion = dict(amonestacion.dict())
    result = db.execute(models.amonestacion.insert().values(**db_amonestacion))
    db.commit()
    db_amonestacion['amonest_id'] = result.inserted_primary_key[0]
    return db_amonestacion

def delete_amonestacion(db: Session, amonest_id: int):
    db_amonestacion = get_amonestacion(db, amonest_id)
    if not db_amonestacion:
        return False
    db.execute(models.amonestacion.delete().where(models.amonestacion.c.amonest_id == amonest_id))
    db.commit()
    return True