from pydantic.dataclasses import dataclass
import datetime

@dataclass
class Sensor_value_dto:
    sensornode: str
    sensorname: str
    sensortyp: str
    unit: str
    value: float
    timestamp: datetime.datetime


Sensor_value_dto.__pydantic_model__.update_forward_refs()