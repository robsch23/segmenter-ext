import json


def get_version():
    with open('../ppom.json', 'r') as ppom_file:
        ppom_info = json.loads(ppom_file.read())

    return ppom_info.get('version', '')

