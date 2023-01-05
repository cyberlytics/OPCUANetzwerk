from pydantic.dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class Request_dto:
    sensornode: Optional[str]
    sensorname: Optional[str]
    sensortyp: Optional[str]
    startTimestamp: Optional[datetime.datetime]
    endTimestamp: Optional[datetime.datetime]

Request_dto.__pydantic_model__.update_forward_refs()