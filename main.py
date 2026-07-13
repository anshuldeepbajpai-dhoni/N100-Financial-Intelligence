from src.etl.loader import ExcelLoader
from src.etl.validator import DataValidator
from src.etl.exporter import ProcessedDataExporter

from src.etl.config import (
    ALL_DATASETS,
    OUTPUT_DIR
)


# ==========================================================
# REUSABLE PRINT SECTION
# ==========================================================

def print_section(title):

    print("\n" + "=" * 80)

    print(title)

    print("=" * 80)


# ==========================================================
# MAIN APPLICATION
# ==========================================================

def main():

    # ------------------------------------------------------
    # Application Header
    # ------------------------------------------------------

    print_section(
        "N100 FINANCIAL INTELLIGENCE PLATFORM\n"
        "SPRINT 1 — DAY 4\n"
        "PROCESSED DATA EXPORT AND DATA MANIFEST"
    )


    # ======================================================
    # STEP 1 — LOAD DATASETS
    # ======================================================

    print_section(
        "STEP 1 — DATASET LOADING"
    )


    loader = ExcelLoader()


    datasets = loader.load_all(
        ALL_DATASETS
    )


    # ======================================================
    # STEP 2 — LOAD AUDIT
    # ======================================================

    print_section(
        "LOAD AUDIT"
    )


    for row in loader.audit:

        print(

            f"{row['dataset']:<28}"

            f"{row['rows']:>7} rows"

            f"{row['columns']:>7} cols"

            f"   {row['status']}"

        )


    successful_loads = sum(

        1

        for row in loader.audit

        if row["status"].upper()
        == "SUCCESS"

    )


    failed_loads = (

        len(loader.audit)

        - successful_loads

    )


    print("-" * 80)

    print(

        f"Successfully loaded : "
        f"{successful_loads}"

    )

    print(

        f"Failed to load      : "
        f"{failed_loads}"

    )

    print(

        f"Datasets available  : "
        f"{len(datasets)}"

    )


    print("\nLoad audit generated successfully.")

    print(

        "Location: "

        f"{OUTPUT_DIR / 'load_audit.csv'}"

    )


    # ------------------------------------------------------
    # Stop pipeline if no dataset was loaded
    # ------------------------------------------------------

    if not datasets:

        print_section(
            "PIPELINE TERMINATED"
        )

        print(

            "No datasets were loaded. "
            "Processed-data export cannot continue."

        )

        return


    # ======================================================
    # STEP 3 — DATA QUALITY VALIDATION
    # ======================================================

    print_section(
        "STEP 2 — DATA QUALITY VALIDATION"
    )


    validator = DataValidator()


    report = validator.validate_all(
        datasets
    )


    # ======================================================
    # STEP 4 — PROCESSED DATA EXPORT
    # ======================================================

    print_section(
        "STEP 3 — PROCESSED DATA EXPORT"
    )


    exporter = ProcessedDataExporter()


    exported_files = exporter.export_all(
        datasets
    )


    # ======================================================
    # EXPORT AUDIT
    # ======================================================

    print_section(
        "PROCESSED DATA EXPORT AUDIT"
    )


    for audit_row in exporter.export_audit:

        print(

            f"{audit_row['dataset']:<28}"

            f"{audit_row['rows']:>7} rows"

            f"{audit_row['columns']:>7} cols"

            f"   {audit_row['status']}"

        )


    successful_exports = sum(

        1

        for row in exporter.export_audit

        if row["status"].upper()
        == "SUCCESS"

    )


    failed_exports = (

        len(exporter.export_audit)

        - successful_exports

    )


    print("-" * 80)


    print(

        f"Successful exports : "
        f"{successful_exports}"

    )


    print(

        f"Failed exports     : "
        f"{failed_exports}"

    )


    print(

        f"Export completion  : "
        f"{len(exported_files)}"
        f"/{len(datasets)} datasets"

    )


    # ======================================================
    # STEP 5 — VALIDATION SUMMARY
    # ======================================================

    print_section(
        "STEP 4 — FINAL DATA QUALITY RESULTS"
    )


    validator.print_summary(
        report
    )


    # ======================================================
    # GENERATED FILES
    # ======================================================

    print_section(
        "GENERATED OUTPUT REPORTS"
    )


    generated_reports = [

        "load_audit.csv",

        "validation_failures.csv",

        "processed_data_manifest.csv"

    ]


    for filename in generated_reports:

        file_path = (

            OUTPUT_DIR

            / filename

        )


        if file_path.exists():

            print(

                f"✓ {file_path}"

            )

        else:

            print(

                f"✗ Not generated: "
                f"{file_path}"

            )


    # ======================================================
    # FINAL PIPELINE STATUS
    # ======================================================

    print_section(
        "DAY 4 PIPELINE STATUS"
    )


    if (

        successful_exports
        == len(datasets)

        and

        failed_exports == 0

    ):

        print(

            "Status: SUCCESS"

        )

        print(

            "All loaded datasets were exported "
            "to the processed-data layer."

        )


    else:

        print(

            "Status: COMPLETED WITH EXPORT ISSUES"

        )

        print(

            f"{failed_exports} dataset export(s) "
            "require investigation."

        )


    print(

        "\nProcessed data location:"

    )

    print(

        "data/processed/"

    )


    print(

        "\nSprint 1 Day 4 "
        "Completed Successfully"

    )


    print("=" * 80)


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    main()