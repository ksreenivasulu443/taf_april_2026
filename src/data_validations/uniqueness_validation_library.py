import logging


def uniqueness_check(df, unique_columns):
    """
    Validate that specified columns have unique values.
    """
    duplicate_counts = {}

    for column in unique_columns:
        duplicate_rows = (
            df.groupby(column)
              .size()
              .reset_index(name="count")
              .query("count > 1")
        )

        count_duplicates = len(duplicate_rows)
        duplicate_counts[column] = count_duplicates

        if count_duplicates > 0:
            logging.info(f"Duplicate values found in column: {column}")
            logging.info(
                "\n%s",
                duplicate_rows.head(10).to_string(index=False)
            )
        else:
            logging.info(f"No duplicate values found in column: {column}")

    logging.info("Duplicate counts per column: %s", duplicate_counts)

    status = "PASS" if all(count == 0 for count in duplicate_counts.values()) else "FAIL"

    logging.info("Uniqueness Check Status: %s", status)

    return status