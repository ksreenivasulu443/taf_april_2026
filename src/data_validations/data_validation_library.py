
import hashlib
import logging
import pandas as pd
import os
from datetime import datetime

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", 2000)
pd.set_option("display.width", 1000)

source =pd.read_csv(r"C:\Users\Haritha\PycharmProjects\taf_april_2026\taf_april_2026\input_files\source_1M.csv")

target = pd.read_csv(r"C:\Users\Haritha\PycharmProjects\taf_april_2026\taf_april_2026\input_files\target_1M.csv")

key_columns = ['CustomerID']

os.makedirs("logs", exist_ok=True)

log_file = f"C:\\Users\\Haritha\\PycharmProjects\\taf_april_2026\\taf_april_2026\\logs\\log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

print("log file", log_file)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
#
# print(source.compare(target))
#
# print("source == target", source == target)

# print("source.eq(target)", source.eq(target))

# 1M -- 100 ==> 1M * 100 ==> 100M

# def data_compare(source_df, target_df,key_columns, num_records = 10):
#     # Using sqldf data comparison
#     # failed = sqldf("""select * from (select * from source_df except select * from target_df )
#     #                     union
#     #                     select * from (select * from target_df except select * from source_df)
#     #                """)
#     #
#     # print(failed)
#
#     source_only = (source_df[key_columns].merge(target_df, how='left', on=key_columns, indicator=True).
#                     query("_merge == 'left_only' ").drop(columns='_merge'))
#
#     source_only['data_from'] = "SOURCE"
#
#     target_only = (target_df[key_columns].merge(source_df, how='left', on=key_columns, indicator=True).
#                     query("_merge == 'left_only' ").drop(columns='_merge'))
#     target_only['data_from'] = "TARGET"
#
#     failed =  pd.concat([source_only, target_only], ignore_index=True)
#
#     print("failed: ", failed)
#
#     if len(failed)>0:
#         status ='FAIL'
#         merged  = source_df.merge(target_df, how='inner', on=key_columns, indicator=True, suffixes=('_source', '_target'))
#         print(merged)
#         non_key_columns =[]
#         for col in source_df.columns:
#             if col not in key_columns:
#                 non_key_columns.append(col)
#
#         print("non_key_columns: ", non_key_columns)
#         for column in non_key_columns:
#             mismatch = merged[
#                 merged[f"{column}_source"].fillna("").astype(str)
#                 !=
#                 merged[f"{column}_target"].fillna("").astype(str)
#                 ]
#
#
#             print("="*100)
#             print("column: ", column)
#             print("mismatch: ")
#             print(mismatch[key_columns + [f"{column}_source", f"{column}_target"] ] )
#             print("=" * 100)
#
#     else:
#         status = 'PASS'
#
#     return status






def generate_hash(row):
    """
    Generate SHA256 hash for a row.
    """
    row_string = "||".join(
        row.fillna("").astype(str).str.strip()
    )
    return hashlib.sha256(
        row_string.encode("utf-8")
    ).hexdigest()


def data_compare(source_df, target_df, key_columns, num_records=10):

    status = "PASS"

    # ==========================================================
    # Common Columns
    # ==========================================================

    common_columns = sorted(
        list(
            set(source_df.columns).intersection(target_df.columns)
        )
    )

    logging.info("Common Columns : %s", common_columns)

    # ==========================================================
    # Create Copy
    # ==========================================================

    source = source_df.copy()
    target = target_df.copy()

    # ==========================================================
    # Generate Row Hash
    # ==========================================================

    source["hash_key"] = source[common_columns].apply(
        generate_hash,
        axis=1
    )

    target["hash_key"] = target[common_columns].apply(
        generate_hash,
        axis=1
    )

    # ==========================================================
    # Find Different Rows Using Hash
    # ==========================================================

    source_only = source.loc[
        ~source["hash_key"].isin(target["hash_key"])
    ].copy()

    source_only["data_from"] = "SOURCE"

    target_only = target.loc[
        ~target["hash_key"].isin(source["hash_key"])
    ].copy()

    target_only["data_from"] = "TARGET"

    failed = pd.concat(
        [source_only, target_only],
        ignore_index=True
    )

    # ==========================================================
    # PASS
    # ==========================================================

    if failed.empty:

        logging.info("=" * 80)
        logging.info("DATA COMPARE : PASS")
        logging.info("=" * 80)

        return "PASS"

    status = "FAIL"

    logging.info("=" * 80)
    logging.info("DATA COMPARE : FAIL")
    logging.info("Failed Rows : %d", len(failed))
    logging.info("=" * 80)

    logging.info(
        "\n%s",
        failed.head(num_records).to_string(index=False)
    )

    # ==========================================================
    # Failed Business Keys
    # ==========================================================

    failed_keys = pd.concat(
        [
            source_only[key_columns],
            target_only[key_columns]
        ]
    ).drop_duplicates()

    # ==========================================================
    # Filter Only Failed Rows
    # ==========================================================


    # source - 100 - 2 (customerid 2, 9)
    # target - 100 - 2 ( customerid2,11)
    source_failed = source.merge(
        failed_keys,
        on=key_columns,
        how="inner"
    )

    target_failed = target.merge(
        failed_keys,
        on=key_columns,
        how="inner"
    )

    source_failed.drop(
        columns="hash_key",
        inplace=True
    )

    target_failed.drop(
        columns="hash_key",
        inplace=True
    )

    # ==========================================================
    # Merge Failed Rows
    # ==========================================================

    merged = source_failed.merge(
        target_failed,
        on=key_columns,
        how="outer",
        suffixes=("_source", "_target"),
        indicator=True
    )

    non_key_columns = [
        col
        for col in common_columns
        if col not in key_columns
    ]

    # ==========================================================
    # Compare Only Failed Rows
    # ==========================================================

    for column in non_key_columns:

        source_col = f"{column}_source"
        target_col = f"{column}_target"

        mismatch = merged[
            merged[source_col]
            .fillna("")
            .astype(str)
            .str.strip()
            !=
            merged[target_col]
            .fillna("")
            .astype(str)
            .str.strip()
        ]

        if mismatch.empty:
            continue

        logging.info("")
        logging.info("-" * 80)
        logging.info("Column : %s", column)
        logging.info(
            "Mismatch Count : %d",
            len(mismatch)
        )
        logging.info("-" * 80)

        logging.info(
            "\n%s",
            mismatch[
                key_columns +
                [
                    source_col,
                    target_col
                ]
            ]
            .head(num_records)
            .to_string(index=False)
        )

    logging.info("")
    logging.info("=" * 80)
    logging.info("FINAL STATUS : %s", status)
    logging.info("=" * 80)

    return status




data_compare(source_df=source, target_df=target, key_columns=key_columns)