import random
import numpy as np
import pandas as pd
from faker import Faker
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

NUM_RECORDS = 1_000_000
NUM_UPDATED = 500
NUM_DELETED = 250
NUM_NEW = 250

OUTPUT_FOLDER = r"C:\ETL_Test_Data"

# ==========================================================
# Faker Initialization
# ==========================================================

fake = Faker("en_IN")

Faker.seed(42)
random.seed(42)
np.random.seed(42)

# ==========================================================
# Generate Source Data
# ==========================================================

print("=" * 80)
print("Generating Source Data...")
print("=" * 80)

source_df = pd.DataFrame({
    "CustomerID": np.arange(1, NUM_RECORDS + 1),
    "CustomerName": [fake.name() for _ in range(NUM_RECORDS)],
    "Email": [fake.email() for _ in range(NUM_RECORDS)],
    "City": [fake.city() for _ in range(NUM_RECORDS)],
    "Country": ["India"] * NUM_RECORDS
})

print("Source Generated Successfully")
print(source_df.head())

# ==========================================================
# Create Target
# ==========================================================

print("\nCreating Target Data...")

target_df = source_df.copy()

target_df["create_date"] = "2026-07-12"

# ==========================================================
# Update Few Records
# ==========================================================

print(f"\nUpdating {NUM_UPDATED} Records...")

updated_rows = np.random.choice(
    target_df.index,
    NUM_UPDATED,
    replace=False
)

target_df.loc[updated_rows, "CustomerName"] = [
    fake.name() for _ in range(NUM_UPDATED)
]

target_df.loc[updated_rows, "Email"] = [
    fake.email() for _ in range(NUM_UPDATED)
]

# ==========================================================
# Delete Few Records
# ==========================================================

print(f"Deleting {NUM_DELETED} Records...")

remaining_rows = target_df.index.difference(updated_rows)

deleted_rows = np.random.choice(
    remaining_rows,
    NUM_DELETED,
    replace=False
)

target_df = target_df.drop(deleted_rows)

# ==========================================================
# Add New Records
# ==========================================================

print(f"Adding {NUM_NEW} New Records...")

new_df = pd.DataFrame({
    "CustomerID": np.arange(
        NUM_RECORDS + 1,
        NUM_RECORDS + NUM_NEW + 1
    ),
    "CustomerName": [fake.name() for _ in range(NUM_NEW)],
    "Email": [fake.email() for _ in range(NUM_NEW)],
    "City": [fake.city() for _ in range(NUM_NEW)],
    "Country": ["India"] * NUM_NEW,
    "create_date": ["2026-07-12"] * NUM_NEW
})

target_df = pd.concat(
    [target_df, new_df],
    ignore_index=True
)

# ==========================================================
# Shuffle Target Records
# ==========================================================

target_df = target_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# ==========================================================
# Save CSV Files
# ==========================================================

output_path = Path(OUTPUT_FOLDER)
output_path.mkdir(parents=True, exist_ok=True)

source_file = output_path / "source_1M.csv"
target_file = output_path / "target_1M.csv"

print("\nSaving CSV Files...")

source_df.to_csv(
    source_file,
    index=False
)

target_df.to_csv(
    target_file,
    index=False
)

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 80)
print("DATA GENERATION COMPLETED")
print("=" * 80)

print(f"Source Records       : {len(source_df):,}")
print(f"Target Records       : {len(target_df):,}")
print(f"Updated Records      : {NUM_UPDATED:,}")
print(f"Deleted Records      : {NUM_DELETED:,}")
print(f"New Records          : {NUM_NEW:,}")

print("\nSource File")
print(source_file)

print("\nTarget File")
print(target_file)

print("\nSource Sample")
print(source_df.head())

print("\nTarget Sample")
print(target_df.head())

print("\nDone.")