import re

# pattern1 = ['key:=value']
# pattern2 = ['key:>value']
# pattern3 = ['key:<value']
# pattern4 = ['key:!value']
# pattern5 = ['key:[value,value]']
# pattern6 = ['key:value']

# pattern7 = ['value']
# pattern8 = ['key:value', 'key:value']
# pattern9 = ['key:value', 'or', 'key:value']

# # (
# #     is_and_conditions,
# #     [column, val1, val2]
# # )

input_requirements = [
    'username:=user1',
    'or',
    'is_admin:=True',
    'create_at:<2024-10-12'
]


def test(input_requirements):
    condition = True
    requirements = []
    for requirement in input_requirements:
        if requirement == 'or':
            condition = False
            continue
        elif not requirement.find(':'):
            requirements.append([column,])
            
        column = requirement.split(':')[0]
        value = requirement.split(':')[1]
        operator = 'like'
        
        if re.match('=.*', value):
            operator = '=='
            value = value[1:]
            requirements.append([column, operator, value])
        elif re.match('>.*', value):
            operator = '>'
            value = value[1:]
            requirements.append([column, operator, value])
        elif re.match('<.*', value):
            operator = '<'
            value = value[1:]
            requirements.append([column, operator, value])
        elif re.match('!.*', value):
            operator = '!='
            value = value[1:]
            requirements.append([column, operator, value])
        elif re.match('[.*]', value):
            operator = 'between'
            value1 = value[1:-1].split(',')[0]
            value2 = value[1:-1].split(',')[1]
            requirements.append([column, operator, value1, value2])
        elif re.match('.*', value):
            operator = 'like'
            requirements.append([column, operator, value])
            
    return condition, requirements
            
print(test(input_requirements))


