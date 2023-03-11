
from oddsnexus.domain.common import UniqueId, valueobject


@valueobject
class Event:
    id: UniqueId
    sports_event_id: UniqueId
