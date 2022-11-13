from operarchive.database.deta_interface import Collection
from operarchive.database.models import (
    PerformanceModel,
    ProductionModel,
    StageProducerModel,
    WorkModel,
)

PerformanceDatabase = Collection("performances", PerformanceModel)
WorkDatabase = Collection("works", WorkModel)
StageProducerDatabase = Collection("stages_producers", StageProducerModel)
ProductionsDatabase = Collection("productions", ProductionModel)
