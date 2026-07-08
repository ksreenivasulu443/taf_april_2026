import logging
def duplicate_check(df, key_column):
    duplicate_rows = df.groupby(key_column).size().reset_index(name='count').query("count>1")

    if len(duplicate_rows)>0:
        status = 'FAIL'
        logging.info(f"Duplicate rows\n%s", duplicate_rows.head(10).to_string(index=False))
    else:
        status = 'PASS'
        logging.info("no duplicate rows")

    return status