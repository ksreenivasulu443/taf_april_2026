
def test_count(read_data):
    source,target,_ = read_data
    assert len(source)==len(target)


def test_duplicate(read_data):
    source, target,config_data = read_data
    keycolumn = config_data['validation']['keycolumn']
    assert len(target.groupby(keycolumn).size().reset_index(name='count').query("count>1")) == 0


#source count and target count
# source dataframe and target dataframe
# source and target configuration(file name and their details , database and creds)