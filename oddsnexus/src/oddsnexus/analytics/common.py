
from oddsnexus.domain.common import ID, valueobject


@valueobject
class Event:
    id: ID
    sports_event_id: ID
