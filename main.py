import hashlib
import logging
import pandas as pd
from datetime import datetime
import os

source =pd.read_csv(r"C:\Users\Haritha\PycharmProjects\taf_april_2026\taf_april_2026\input_files\customer_with_header.csv")

target = pd.read_csv(r"C:\Users\Haritha\PycharmProjects\taf_april_2026\taf_april_2026\input_files\customer_with_header_t.csv")
key_columns = ['CustomerID']
os.makedirs("logs", exist_ok=True)

log_file = f"logs/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

print("log file", log_file)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def generate_hash(row):
    """
    Generate SHA256 hash for a row.
    """
    row_string = "||".join(
        row.fillna("").astype(str).str.strip()
    )
    return hashlib.sha256(row_string.encode("utf-8")).hexdigest()


def data_compare(source_df, target_df, key_columns, num_records=10):
    """
    Compare source and target using row hash and then compare
    only mismatched rows column by column.
    """

    # ---------------------------------------------------------
    # Find common columns
    # ---------------------------------------------------------

    common_columns = sorted(
        list(set(source_df.columns).intersection(target_df.columns))
    )

    logging.info("Common Columns : %s", common_columns)

    # ---------------------------------------------------------
    # Generate Row Hash
    # ---------------------------------------------------------

    source = source_df.copy()
    target = target_df.copy()

    source["hash_key"] = source[common_columns].apply(generate_hash, axis=1)
    target["hash_key"] = target[common_columns].apply(generate_hash, axis=1)

    # ---------------------------------------------------------
    # Find missing hashes
    # ---------------------------------------------------------

    source_only = source.loc[
        ~source["hash_key"].isin(target["hash_key"])
    ].copy()

    source_only["datafrom"] = "SOURCE"

    target_only = target.loc[
        ~target["hash_key"].isin(source["hash_key"])
    ].copy()

    target_only["datafrom"] = "TARGET"

    failed_rows = pd.concat(
        [source_only, target_only],
        ignore_index=True
    )

    if failed_rows.empty:

        logging.info("===================================")
        logging.info("DATA COMPARE : PASS")
        logging.info("No mismatched rows found.")
        logging.info("===================================")

        return "PASS"

    logging.info("===================================")
    logging.info("DATA COMPARE : FAIL")
    logging.info("Total Failed Rows : %d", len(failed_rows))
    logging.info("===================================")

    logging.info(
        "\n%s",
        failed_rows.head(num_records).to_string(index=False)
    )

    # ---------------------------------------------------------
    # Get failed business keys
    # ---------------------------------------------------------

    failed_keys = (
        failed_rows[key_columns]
        .drop_duplicates()
    )

    # ---------------------------------------------------------
    # Filter source & target only for failed keys
    # ---------------------------------------------------------

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

    # Remove hash column before comparison
    source_failed = source_failed.drop(columns=["hash_key"])
    target_failed = target_failed.drop(columns=["hash_key"])

    # ---------------------------------------------------------
    # Compare failed rows column by column
    # ---------------------------------------------------------

    merged = source_failed.merge(
        target_failed,
        on=key_columns,
        how="outer",
        suffixes=("_source", "_target"),
        indicator=True
    )

    compare_columns = [
        c for c in common_columns
        if c not in key_columns
    ]

    for column in compare_columns:

        source_col = column + "_source"
        target_col = column + "_target"

        mismatch = merged[
            merged[source_col].fillna("").astype(str).str.strip()
            !=
            merged[target_col].fillna("").astype(str).str.strip()
        ]

        if not mismatch.empty:

            logging.info("")
            logging.info("-----------------------------------------")
            logging.info("Column : %s", column)
            logging.info("Mismatch Count : %d", len(mismatch))
            logging.info("-----------------------------------------")

            display_cols = (
                key_columns +
                [source_col, target_col]
            )

            logging.info(
                "\n%s",
                mismatch[display_cols]
                .head(num_records)
                .to_string(index=False)
            )

    logging.info("")
    logging.info("FINAL STATUS : FAIL")

    return "FAIL"


data_compare(source_df=source, target_df=target, key_columns=key_columns, num_records=10)