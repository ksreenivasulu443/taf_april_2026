import os
def read_query(dir_path):
    query_path = os.path.join(dir_path, 'transformation_query.sql')
    with open(query_path, 'r') as f:
        query= f.read()
    return query
