"""Hora civil escolar explícita, independiente de TZ del proceso."""
from datetime import datetime
from zoneinfo import ZoneInfo

ZONA_ESCOLAR = ZoneInfo('America/Santiago')


def ahora_chile(instante=None):
    if instante is None:
        return datetime.now(ZONA_ESCOLAR)
    if instante.tzinfo is None or instante.utcoffset() is None:
        raise ValueError('El instante debe incluir zona horaria')
    return instante.astimezone(ZONA_ESCOLAR)


def hoy_chile():
    return ahora_chile().date()
