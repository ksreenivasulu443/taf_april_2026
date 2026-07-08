import logging
import pandas as pd


def null_value_check(df, not_null_columns, failed_records=5):
    """
    Validate that specified columns have no null, empty, or invalid values.
    """

    failures = []

    invalid_values = ["NA", "NULL", "NONE", "N/A", "UNKNOWN"]

    for column in not_null_columns:
        logging.info("Checking column: %s", column)

        failing_rows = df[
            df[column].isna()
            | (df[column].astype(str).str.strip() == "")
            | (df[column].astype(str).str.upper().isin(invalid_values))
        ]

        null_count = len(failing_rows)

        if null_count > 0:
            sample_failed_records = (
                failing_rows.head(failed_records)
                .to_dict(orient="records")
            )

            failures.append({
                "column": column,
                "null_count": null_count,
                "sample_failed_records": sample_failed_records
            })

            logging.info(
                "Column '%s' has %d invalid/null records.",
                column,
                null_count
            )
            logging.info(
                "\n%s",
                failing_rows.head(failed_records).to_string(index=False)
            )
        else:
            logging.info("Column '%s' has no null or invalid values.", column)

    if failures:
        status = "FAIL"
        logging.info("Null Value Check Status: %s", status)
        logging.info("Failures: %s", failures)
    else:
        status = "PASS"
        logging.info("Null Value Check Status: %s", status)
        logging.info("No null values found.")

    return status