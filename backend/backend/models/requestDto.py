from pydantic.dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class RequestDto:
    sensornode: Optional[str]
    sensorname: Optional[str]
    sensortyp: Optional[str]
    startTimestamp: Optional[datetime.datetime]
    endTimestamp: Optional[datetime.datetime]

async def convert_filter_params():
    
    param_dict = {}
    

RequestDto.__pydantic_model__.update_forward_refs()