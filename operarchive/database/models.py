from datetime import date
from enum import Enum

from pydantic import BaseModel


class DateType(str, Enum):
    EXACT = "Exact"
    RANGE = "Range"
    UNKNOWN = "Unknown"


class DateModel(BaseModel):
    earliest: date
    latest: date
    before_certain_performance_key: str


class WorkType(Enum):
    "Enum for work type"
    OPERA = "opera"
    ORATORIO = "oratorio"
    OPERETTA = "operetta"
    MUSICAL = "musical"


class DBModel(BaseModel):
    key: str | None = None


class StageProducerModel(DBModel):
    name: str
    short_name: str


class WorkModel(DBModel):
    title: str
    work_type: WorkType
    composer: str
    written_year: int
    world_premiere_year: int
    version_year: int
    main_roles: list[str]


class ProductionModel(DBModel):
    producer_key: str
    work_key: str
    disambiguation: str
    premiere_year: int | None


class PerformanceModel(DBModel):
    """Performance model"""

    production_key: str
    visit_date: DateModel
    stage_key: str
    cast: dict[str, list[str]]
    leading_team: dict[str, list[str]]
    comments: str
