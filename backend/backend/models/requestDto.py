from pydantic.dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class RequestDto:
    sensornode: Optional[str]
    sensorname: Optional[str]
    sensortyp: Optional[str]
    startTimestamp: Optional[datetime.datetime]
    endTimestamp: Optional[datetime.datetime]

RequestDto.__pydantic_model__.update_forward_refs()