import re
from lxml import etree

class TemplateString(object):
    def __init__(self, opcua):
        self.__client = opcua

    def __resolve_value_template(self, xml):
        if xml.attrib['type'] == 'number':
            decimals = 4
            if xml.attrib['decimals'] != None:
                decimals = xml.attrib['decimals']
            return f'{xml.text:.{decimals}}'


    def __resolve_opcua_template(self, xml):
        node_val = self.__client.get_node(f'ns=2;s={xml.attrib["node"]}').get_value()
        decimals = 4
        if xml.attrib['decimals'] != None:
            decimals = xml.attrib['decimals']
        return f'{node_val:.{decimals}}'
        
    def is_template_string(templ):
        # Check if template string is present
        match_str = '<.*>'
        m = re.search(match_str, templ)
        if m == None:
            return False

        # Check if xml is valid
        try:
            xml = etree.XML(m.group())
        except Exception as ex:
            print(f'Given template string "{templ}" was not valid: {ex}')
            return False

        return True

    def resolve_template_string(self, templ):
        # Check if template string is present
        match_str = '<.*>'
        m = re.search(match_str, templ)
        if m == None:
            return templ

        xml = ''
        try:
            xml = etree.XML(m.group())
        except Exception as ex:
            print(f'Given template string "{templ}" was not valid: {ex}')
            return templ
    
        resolved_str = ''

        if xml.tag == 'value':
            resolved_str = self.__resolve_value_template(xml)

        if xml.tag == 'opcua':
            resolved_str = self.__resolve_opcua_template(xml)

        str_front = templ.split(m.group())[0]
        str_back  = templ.split(m.group())[1]
        return str_front + resolved_str + str_back
