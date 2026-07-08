from src.data_validations.count_validation_library import count_check
from src.data_validations.duplicate_validation_library import duplicate_check
from src.data_validations.uniqueness_validation_library import uniqueness_check
from src.data_validations.not_null_validation_library import null_value_check

import logging
def test_count(read_data):
    source,target,config_data = read_data
    key_column = config_data["validation"]["key_column"]
    logging.info("Source DataFrame Shape: %s", source.shape)
    logging.info("Source DataFrame:\n%s", source.head(10).to_string(index=False))
    status = count_check(source=source,target=target, key_column=key_column)
    assert status ,"Count check"

def test_duplicate(read_data):
    _,target,config_data = read_data
    key_column = config_data["validation"]["key_column"]
    status = duplicate_check(df=target,key_column=key_column)
    assert status == 'PASS',"Duplicate check"

def test_unique(read_data):
    _,target,config_data = read_data
    unique_columns = config_data["validation"]["unique_columns"]
    status = uniqueness_check(df=target,unique_columns=unique_columns)
    assert status == 'PASS',"unique check"


def test_not_null(read_data):
    _,target,config_data = read_data
    not_null_columns = config_data["validation"]["not_null_columns"]
    status = null_value_check(df=target,not_null_columns=not_null_columns)
    assert status == 'PASS',"null check"



