from sqlalchemy import Table, Column, Integer, String, BigInteger, Numeric, Date, Time, ForeignKey
from database import metadata

partido = Table(
    "partido",
    metadata,
    Column("partido_id", BigInteger, primary_key=True),
    Column("temporada_id", BigInteger, ForeignKey("temporada.temporada_id", ondelete="CASCADE"), nullable=False),
    Column("fecha", Date, nullable=False),
    Column("hora", Time, nullable=False),
    Column("estadio_id", BigInteger, ForeignKey("estadio.estadio_id", ondelete="RESTRICT"), nullable=False),
    Column("equipo_local", BigInteger, ForeignKey("equipo.equipo_id", ondelete="RESTRICT"), nullable=False),
    Column("equipo_visitante", BigInteger, ForeignKey("equipo.equipo_id", ondelete="RESTRICT"), nullable=False),
    Column("goles_local", Integer, nullable=False, default=0),
    Column("goles_visitante", Integer, nullable=False, default=0),
)

participa = Table(
    "participa",
    metadata,
    Column("partido_id", BigInteger, ForeignKey("partido.partido_id", ondelete="CASCADE"), primary_key=True),
    Column("jugador_id", BigInteger, ForeignKey("jugador.jugador_id", ondelete="CASCADE"), primary_key=True),
)

gol = Table(
    "gol",
    metadata,
    Column("gol_id", BigInteger, primary_key=True),
    Column("partido_id", BigInteger, ForeignKey("partido.partido_id", ondelete="CASCADE"), nullable=False),
    Column("jugador_id", BigInteger, ForeignKey("jugador.jugador_id", ondelete="CASCADE"), nullable=False),
    Column("minuto", Integer, nullable=False),
)

amonestacion = Table(
    "amonestacion",
    metadata,
    Column("amonest_id", BigInteger, primary_key=True),
    Column("partido_id", BigInteger, ForeignKey("partido.partido_id", ondelete="CASCADE"), nullable=False),
    Column("jugador_id", BigInteger, ForeignKey("jugador.jugador_id", ondelete="CASCADE"), nullable=False),
    Column("minuto", Integer, nullable=False),
    Column("tipo", String(50), nullable=False),
) 