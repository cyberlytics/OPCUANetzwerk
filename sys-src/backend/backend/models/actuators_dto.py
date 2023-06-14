from pydantic.dataclasses import dataclass
from typing import Optional, Union

@dataclass
class actuator_change_dto:
    actuator_node : str
    actuator_act :str
    new_value : Union[str,float,bool]

@dataclass
class actuator_list_dto:
    actuator_node : str
    actuator_act  : str
    actuator_value: Union[str,float,bool,None]
    actuator_dtype: str


actuator_change_dto.__pydantic_model__.update_forward_refs()
actuator_list_dto.__pydantic_model__.update_forward_refs()