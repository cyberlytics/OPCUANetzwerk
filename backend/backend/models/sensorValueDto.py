from pydantic.dataclasses import dataclass
import datetime

@dataclass
class SensorValueDto:
    sensornode: str
    sensorname: str
    sensortyp: str
    unit: str
    value: float
    timestamp: datetime.datetime


SensorValueDto.__pydantic_model__.update_forward_refs()