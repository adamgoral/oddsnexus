import datetime as dt

import faust


ID = str
DateTime = dt.datetime

class Entity(faust.Record, abstract=True):
    id: ID
    ...
