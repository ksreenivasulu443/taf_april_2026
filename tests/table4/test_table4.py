from src.data_validations.count_validation_library import count_check

def test_count(read_data):
    source,target,config_data = read_data
    key_column = config_data["validation"]["key_column"]
    status = count_check(source=source,target=target, key_column=key_column)
    assert status ,"Count check"
