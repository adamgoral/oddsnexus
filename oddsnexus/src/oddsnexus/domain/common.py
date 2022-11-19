from dataclasses import dataclass
import datetime as dt

import faust


ID = str
DateTime = dt.datetime

valueobject = dataclass(frozen=True, eq=True)

class Entity(faust.Record, abstract=True):
    id: ID
    ...

class Aggregate(Entity, abstract=True):
    ...