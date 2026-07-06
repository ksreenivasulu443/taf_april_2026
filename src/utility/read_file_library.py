import pandas as pd
def read_file(config_data):
    file_type = config_data['type'].lower()
    if file_type in ( 'csv', 'txt'):
        df = pd.read_csv(filepath_or_buffer=config_data['file_path'],
                         header=config_data['header'],
                         sep=config_data['sep'])

    elif file_type == 'excel':
        df = pd.read_excel(io=config_data['file_path'],
                           header=config_data['header']
                           )
    elif file_type == 'parquet':
        df = pd.read_parquet(path=config_data['file_path'])

    elif file_type == "json":
        df = pd.read_json(
            path_or_buf=config_data['file_path']
        )

    else:
        raise ValueError(
            f"Unsupported file type '{file_type}'. "
            "Supported types are: csv, txt, excel, parquet, json."
        )


    return df
