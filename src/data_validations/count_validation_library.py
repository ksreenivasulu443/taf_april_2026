from src.data_validations.records_only_source import record_only_source
from src.data_validations.records_only_target import record_only_target
import logging
def count_check(source, target, key_column):
    src_cnt = len(source)
    tgt_cnt = len(target)
    if src_cnt == tgt_cnt:

        logging.info("Count is matching between source and target")
        failed_rows_target, status1 =  record_only_source(source=source, target=target, key_column=key_column)
        logging.info("missing row DataFrame:\n%s", failed_rows_target.head(10).to_string(index=False)  )

        failed_rows_source, status2 = record_only_target(source=source, target=target, key_column=key_column)
        logging.info("missing row DataFrame:\n%s", failed_rows_source.head(10).to_string(index=False))
        if status1 and status2:
            final_status = True
        else:
            final_status = False
    else:
        print(f"""Count is not matching between source and target
                  source count is {src_cnt} and target count is {tgt_cnt}
                  Difference is {abs(src_cnt-tgt_cnt)}  """)
        failed_rows_target, status1 = record_only_source(source=source, target=target, key_column=key_column)
        logging.info("missing row DataFrame:\n%s", failed_rows_target.head(10).to_string(index=False))

        failed_rows_source, status2 = record_only_target(source=source, target=target, key_column=key_column)
        logging.info("missing row DataFrame:\n%s", failed_rows_source.head(10).to_string(index=False))
        if status1 and status2:
            final_status = True
        else:
            final_status = False

    return final_status
