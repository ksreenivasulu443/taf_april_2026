import pandas as pd

import logging
def record_only_source(source,target,key_column):
    failed_df = (source[key_column].merge(target[key_column],
                     on=key_column, how='left', indicator=True).query("_merge == 'left_only'")
                      .drop(columns='_merge'))
    logging.info("failed df DataFrame:\n%s", failed_df.head(10).to_string(index=False))

    if len(failed_df) == 0:
        status = True
        logging.info("no failed records")
    else:
        status = False
        logging.warning("test cases failed")
        logging.info("failed df DataFrame:\n%s", failed_df.head(10).to_string(index=False))

    return failed_df, status





