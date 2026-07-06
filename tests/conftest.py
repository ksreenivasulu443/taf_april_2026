import pandas as pd
import pytest
import yaml
import os
from src.utility.read_file_library import read_file
from src.utility.read_db_library import read_db

@pytest.fixture(scope='module')
def read_config(request):

    dir_path = request.node.fspath.dirname
    print("dir path", dir_path)
    config_path = os.path.join(dir_path,"config.yml")
    print("config_path ", config_path)
    with open(config_path,"r") as file:
        config_data = yaml.safe_load(file)
        print("config data", config_data)
    return config_data


@pytest.fixture(scope='module')
def read_data(read_config,request):
    config_data = read_config
    source_config_data = config_data['source']
    target_config_data = config_data['target']
    validation_config_data = config_data['validation']
    dir_path = request.node.fspath.dirname

    if source_config_data['type'] == 'sqlserver':
        source = read_db(config_data= source_config_data,dir_path=dir_path)
    else:
        source =  read_file(config_data = source_config_data)

    if target_config_data['type'] == 'sqlserver':
        target = read_db(config_data= target_config_data,dir_path=dir_path)
    else:
        target =  read_file(config_data = target_config_data)

    print("="*100)
    print(source)
    print("=" * 100)
    print(target)
    return source, target, config_data