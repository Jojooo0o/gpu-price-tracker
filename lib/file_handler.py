import json
from os import path

def file_exists(filepath):
    '''
    Validate whether a file exists before trying to open it
    '''
    return True if path.exists(filepath) else False


def write_data(filename, data):
    '''
    Write the collected data to a json file
    '''
    with open(filename, 'w', encoding='utf_8') as file:
        json.dump(data, file, indent=4)


def read_existing_data(filename):
    '''
    Reads historical data from json
    '''
    with open(filename, 'r', encoding='utf_8') as file:
        data = json.load(file)
    return data