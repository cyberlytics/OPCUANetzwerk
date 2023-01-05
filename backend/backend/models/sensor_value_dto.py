from pydantic.dataclasses import dataclass
from typing import Optional, Union
import datetime

@dataclass
class Sensor_value_dto:
    sensornode: str
    sensorname: str
    sensortyp: str
    value: Union[float,bool] #Usually float but presence sensor has a boolean value in it 
    timestamp: datetime.datetime
    unit: str = "" #presence sensor has no unit


Sensor_value_dto.__pydantic_model__.update_forward_refs()