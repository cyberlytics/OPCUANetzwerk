from pydantic.dataclasses import dataclass


@dataclass
class SensorValueDto:
    sensornode: str
    sensorname: str
    sensortyp: str
    unit: str
    value: float
    timestamp: str


SensorValueDto.__pydantic_model__.update_forward_refs()