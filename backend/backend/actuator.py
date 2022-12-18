from typing import Protocol
from opcua import Client


dtype_lookup = {
    'String':str,
    'Double':float,
    'Boolean':bool,
}

dtype_to_string = {
    str:'string',
    int:'number',
    float:'number',
    bool:'boolean',
    (int,float):'number'
}

class BaseActuator:
    def __init__(self,node,sensornode_name):
        self.sensornode= sensornode_name
        self.sensor_descriptor= node.get_display_name().Text
        self.node = node
        self.acts = self.get_available_acts()

    def get_changable_acts(self):
        actuator_list = []
        for act in self.acts.values():
            actuator_list.append({
                'actuator_node':self.get_actuator_name(),
                'actuator_act': act['name'],
                'actuator_value':act['value'],
                'actuator_dtype':dtype_to_string.get(act['dtype'],'string')
            })
        return actuator_list

    def set_changable_act(self,act,val):
        obj = self.acts.get(act)
        if not obj: 
            return f"Actuator does not have the property {act}"
        #check if dtype is correct
        val = obj['dtype'](val)
        if not isinstance(val,obj['dtype']):
            return f'Value has not the right Dtype'
        #set value and update object
        obj['node'].set_value(val)
        obj['value'] = val
        self.acts[act] = obj
        return f'Value was set and is now: {val}'
    
    
    def get_actuator_name(self):
        return f'{self.sensornode}-{self.sensor_descriptor}'
    
    def get_available_acts(self):
        raise NotImplementedError


class A_1602A(BaseActuator):
    def get_available_acts(self):
        acts = {}
        for act in self.node.get_children():
            name = act.get_display_name().Text
            acts[name] = {
                'name':name,
                'value':act.get_value(),
                #dtype in opcua is a seperate type
                #we use the dtype_lookup dict to transform them to python types
                'dtype':dtype_lookup.get(act.get_data_type_as_variant_type().name,str),
                'node':act
            }
        return acts


class LED_Stripe(BaseActuator):
    def get_available_acts(self):
        acts = {}
        for act in self.node.get_children():
            name = act.get_display_name().Text
            #each LED-Node has a child, which controlls the state of the light
            #this child node is the one, we need to store to controll it
            status_node = act.get_children()[0]
            acts[name] = {
                'name' : name,
                'value': status_node.get_value(),
                #dtype in opcua is a seperate type
                #we use the dtype_lookup dict to transform them to python types
                'dtype': dtype_lookup.get(status_node.get_data_type_as_variant_type().name,str),
                'node' : status_node
            }
        return acts


class Piezo(BaseActuator):
    def get_available_acts(self):
        acts = {}
        for act in self.node.get_children():
            name = act.get_display_name().Text
            acts[name] = {
                'name' :name,
                'value':act.get_value(),
                #dtype in opcua is a seperate type
                #we use the dtype_lookup dict to transform them to python types
                'dtype':dtype_lookup.get(act.get_data_type_as_variant_type().name,str),
                'node' :act
            }
        return acts



def create_actuator(actuatorNode,sensornode_name:str):
    actTyp = actuatorNode.get_display_name().Text
    
    if actTyp == "1602A": 
        return A_1602A(node=actuatorNode,sensornode_name=sensornode_name)

    if actTyp.startswith("LED_Stripe_"):
        return LED_Stripe(node=actuatorNode,sensornode_name=sensornode_name)
    
    if actTyp.startswith("Piezo_"):
        return Piezo(node=actuatorNode,sensornode_name=sensornode_name)

    
    