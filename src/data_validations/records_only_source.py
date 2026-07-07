import pandas as pd

#
def record_only_source(source,target,key_column):
    failed_df = (source[key_column].merge(target[key_column],
                     on=key_column, how='left', indicator=True).query("_merge == 'left_only'")
                      .drop(columns='_merge'))

    if len(failed_df) == 0:
        status = True
    else:
        status = False

    return failed_df, status





