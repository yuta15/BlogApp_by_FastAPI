import re


def parse_validate_search_requirements(model:any, input_requirements: list | None):
    """
    model
    requirements:List[List]
        rule
            key:>=value
                parsed -> key >= value
            key:<=value
                parsed -> key <= value
            key:>value
                parsed -> key > value
            key:<value
                parsed -> key < value
            key:=value
                parsed -> key == value
            key:value or valueのみ
                parsed -> like(f'%value%)
            key:[value1, value2]
                parsed -> between(value1, value2)
            key1:value key:value
                parsed -> where(and_(valu1, value2))
            key1:value or key:value
                parsed -> where(or_(valu1, value2))
    """
    is_and_condition =True
    requirements = []
    for requirement in input_requirements:
        if requirement == 'or':
            is_and_condition = False
            continue
        
        column = requirement.split(':')[0]
        search_value = requirement.split(':')[1]
        if re.match('=>.*', search_value):
        elif re.match('=<.*', search_value):
        elif re.match('=<.*', search_value):
        elif re.match('=.*', search_value):
        elif re.match('!=.*', search_value):
        elif re.match('>.*', search_value):
        elif re.match('<.*', search_value):
        elif re.match('[.*]', search_value):


