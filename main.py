from src.etl.loader import ExcelLoader
from src.etl.config import ALL_DATASETS

loader = ExcelLoader()

datasets = loader.load_all(ALL_DATASETS)

print("\n")

print("=" * 80)
print("N100 FINANCIAL INTELLIGENCE PLATFORM")
print("SPRINT 1 - DAY 2")
print("=" * 80)

print()

for row in loader.audit:

    print(
        f"{row['dataset']:<25}"
        f"{row['rows']:>6} rows"
        f"{row['columns']:>6} cols"
        f"   {row['status']}"
    )

print()

print("=" * 80)

print("Load Audit Generated Successfully")

print("Location : output/load_audit.csv")

print("=" * 80)