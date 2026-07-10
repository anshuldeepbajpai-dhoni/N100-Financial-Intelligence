from src.etl.loader import ExcelLoader
from src.etl.validator import DataValidator
from src.etl.config import ALL_DATASETS


def main():

    print("=" * 80)
    print("N100 FINANCIAL INTELLIGENCE PLATFORM")
    print("SPRINT 1")
    print("DAY 2 & DAY 3")
    print("ETL LOADER + DATA QUALITY VALIDATION")
    print("=" * 80)

    # --------------------------------------------------
    # Load Datasets
    # --------------------------------------------------

    loader = ExcelLoader()

    datasets = loader.load_all(ALL_DATASETS)

    print("\n")
    print("=" * 80)
    print("LOAD AUDIT")
    print("=" * 80)

    for row in loader.audit:

        print(
            f"{row['dataset']:<25}"
            f"{row['rows']:>6} rows"
            f"{row['columns']:>6} cols"
            f"   {row['status']}"
        )

    print("=" * 80)
    print("Load Audit Generated Successfully")
    print("Location : output/load_audit.csv")
    print("=" * 80)

    # --------------------------------------------------
    # Data Validation
    # --------------------------------------------------

    validator = DataValidator()

    report = validator.validate_all(datasets)

    validator.print_summary(report)



    print("\nSprint 1 Day 3 Completed Successfully")

    print("=" * 80)



if __name__ == "__main__":
    main()