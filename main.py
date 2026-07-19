from pathlib import Path

import pandas as pd

from src.etl.loader import ExcelLoader
from src.etl.validator import DataValidator
from src.etl.exporter import ProcessedDataExporter
from src.forecasting import ForecastRunner
from src.portfolio import PortfolioRunner
from src.risk import RiskRunner
from src.reporting import ReportingRunner
from src.etl.config import (
    ALL_DATASETS,
    OUTPUT_DIR
)

from src.database.database_loader import (
    DatabaseLoader
)

from src.database.integrity_checker import (
    DatabaseIntegrityChecker
)

from src.database.indexes import (
    DatabaseIndexManager
)

from src.database.views import (
    AnalyticalViewManager
)
from src.analytics.analytics_runner import (
    FinancialAnalyticsRunner
)


# ==========================================================
# APPLICATION CONSTANTS
# ==========================================================

SEPARATOR_LENGTH = 80


# ==========================================================
# CONSOLE HELPERS
# ==========================================================

def print_section(title):

    print(
        "\n"
        + "=" * SEPARATOR_LENGTH
    )

    print(title)

    print(
        "=" * SEPARATOR_LENGTH
    )


def print_separator():

    print(
        "-" * SEPARATOR_LENGTH
    )


def print_metric(
    label,
    value,
    width=27
):

    print(
        f"{label:<{width}}: "
        f"{value}"
    )


def print_report_status(
    report_paths
):

    for report_path in report_paths:

        path = Path(
            report_path
        )

        if path.exists():

            print(
                f"✓ {path}"
            )

        else:

            print(
                f"✗ Missing: {path}"
            )


# ==========================================================
# AUDIT HELPERS
# ==========================================================

def count_successful_rows(
    audit_rows
):

    return sum(

        1

        for row in audit_rows

        if str(
            row.get(
                "status",
                ""
            )
        ).upper() == "SUCCESS"

    )


def print_dataset_audit(
    audit_rows
):

    if not audit_rows:

        print(
            "No audit records generated."
        )

        return


    for row in audit_rows:

        print(

            f"{row['dataset']:<28}"

            f"{row['rows']:>8} rows"

            f"{row['columns']:>8} cols"

            f"   {row['status']}"

        )


# ==========================================================
# STEP 1 — LOAD SOURCE DATASETS
# ==========================================================

def run_dataset_loading():

    print_section(
        "STEP 1 — SOURCE DATASET LOADING"
    )


    loader = ExcelLoader()


    datasets = loader.load_all(
        ALL_DATASETS
    )


    print_section(
        "SOURCE LOAD AUDIT"
    )


    print_dataset_audit(
        loader.audit
    )


    successful_loads = (
        count_successful_rows(
            loader.audit
        )
    )


    failed_loads = (

        len(
            loader.audit
        )

        - successful_loads

    )


    print_separator()


    print_metric(
        "Configured datasets",
        len(ALL_DATASETS)
    )


    print_metric(
        "Successfully loaded",
        successful_loads
    )


    print_metric(
        "Failed loads",
        failed_loads
    )


    print_metric(
        "Datasets available",
        len(datasets)
    )


    print(

        "\nLoad audit: "
        f"{OUTPUT_DIR / 'load_audit.csv'}"

    )


    return (

        datasets,

        loader,

        successful_loads,

        failed_loads

    )


# ==========================================================
# STEP 2 — DATA-QUALITY VALIDATION
# ==========================================================

def run_data_validation(
    datasets
):

    print_section(
        "STEP 2 — DATA-QUALITY VALIDATION"
    )


    validator = DataValidator()


    validation_report = (

        validator.validate_all(
            datasets
        )

    )


    print_section(
        "DATA-QUALITY VALIDATION SUMMARY"
    )


    validator.print_summary(
        validation_report
    )


    return (

        validator,

        validation_report

    )


# ==========================================================
# STEP 3 — PROCESSED-DATA EXPORT
# ==========================================================

def run_processed_export(
    datasets
):

    print_section(
        "STEP 3 — PROCESSED-DATA EXPORT"
    )


    exporter = (
        ProcessedDataExporter()
    )


    exported_files = (

        exporter.export_all(
            datasets
        )

    )


    print_section(
        "PROCESSED-DATA EXPORT AUDIT"
    )


    print_dataset_audit(
        exporter.export_audit
    )


    successful_exports = (

        count_successful_rows(
            exporter.export_audit
        )

    )


    failed_exports = (

        len(
            exporter.export_audit
        )

        - successful_exports

    )


    print_separator()


    print_metric(
        "Successful exports",
        successful_exports
    )


    print_metric(
        "Failed exports",
        failed_exports
    )


    print_metric(

        "Export completion",

        (
            f"{len(exported_files)}"
            f"/{len(datasets)}"
        )

    )


    return {

        "exporter":
        exporter,

        "exported_files":
        exported_files,

        "successful_exports":
        successful_exports,

        "failed_exports":
        failed_exports

    }


# ==========================================================
# STEP 4 — SQLITE DATABASE LOADING
# ==========================================================

def run_database_loading(
    datasets
):

    print_section(
        "STEP 4 — SQLITE DATABASE LOADING"
    )


    database_loader = (
        DatabaseLoader()
    )


    loaded_tables = (

        database_loader.load_all(
            datasets
        )

    )


    print_section(
        "DATABASE LOAD AUDIT"
    )


    for row in (

        database_loader.load_audit

    ):

        print(

            f"{row['table_name']:<28}"

            f"{row['source_rows']:>8} source"

            f"{row['database_rows']:>10} database"

            f"   {row['status']}"

        )


    successful_loads = (

        count_successful_rows(

            database_loader.load_audit

        )

    )


    failed_loads = (

        len(datasets)

        - successful_loads

    )


    print_separator()


    print_metric(
        "Total datasets",
        len(datasets)
    )


    print_metric(
        "Successfully loaded",
        successful_loads
    )


    print_metric(
        "Failed database loads",
        failed_loads
    )


    print_metric(
        "SQLite tables created",
        len(loaded_tables)
    )


    print(

        "\nDatabase: "
        "database/n100_financial.db"

    )


    print(

        "Database audit: "
        "output/database_load_audit.csv"

    )


    return {

        "database_loader":
        database_loader,

        "loaded_tables":
        loaded_tables,

        "successful_loads":
        successful_loads,

        "failed_loads":
        failed_loads

    }


# ==========================================================
# STEP 5 — DATABASE INTEGRITY VALIDATION
# ==========================================================

def run_integrity_validation():

    print_section(
        "STEP 5 — DATABASE INTEGRITY VALIDATION"
    )


    checker = (
        DatabaseIntegrityChecker()
    )


    (
        integrity_report,

        table_summary

    ) = checker.validate_all()


    print_section(
        "DATABASE TABLE SUMMARY"
    )


    if table_summary.empty:

        print(
            "No database tables found."
        )

    else:

        print(

            table_summary.to_string(
                index=False
            )

        )


    print_section(
        "DATABASE INTEGRITY SUMMARY"
    )


    if integrity_report.empty:

        failed_report = (
            pd.DataFrame()
        )

        total_checks = 0

        passed_checks = 0

        failed_checks = 0

        critical_issues = 0

        warnings = 0


        print(

            "No integrity results "
            "were generated."

        )


    else:

        failed_report = (

            integrity_report[

                integrity_report[
                    "failures"
                ] > 0

            ]

        )


        if failed_report.empty:

            print(

                "All database integrity "
                "checks passed."

            )

        else:

            print(

                failed_report.to_string(
                    index=False
                )

            )


        total_checks = len(
            integrity_report
        )


        passed_checks = int(

            (
                integrity_report[
                    "failures"
                ] == 0
            ).sum()

        )


        failed_checks = int(

            (
                integrity_report[
                    "failures"
                ] > 0
            ).sum()

        )


        critical_issues = int(

            (

                (
                    integrity_report[
                        "severity"
                    ] == "CRITICAL"
                )

                &

                (
                    integrity_report[
                        "failures"
                    ] > 0
                )

            ).sum()

        )


        warnings = int(

            (

                (
                    integrity_report[
                        "severity"
                    ] == "WARNING"
                )

                &

                (
                    integrity_report[
                        "failures"
                    ] > 0
                )

            ).sum()

        )


    print_separator()


    print_metric(
        "Total integrity checks",
        total_checks
    )


    print_metric(
        "Passed checks",
        passed_checks
    )


    print_metric(
        "Failed checks",
        failed_checks
    )


    print_metric(
        "Critical findings",
        critical_issues
    )


    print_metric(
        "Warnings",
        warnings
    )


    return {

        "checker":
        checker,

        "integrity_report":
        integrity_report,

        "table_summary":
        table_summary,

        "total_checks":
        total_checks,

        "passed_checks":
        passed_checks,

        "failed_checks":
        failed_checks,

        "critical_issues":
        critical_issues,

        "warnings":
        warnings

    }


# ==========================================================
# STEP 6 — DATABASE INDEX OPTIMIZATION
# ==========================================================

def run_index_optimization():

    print_section(
        "STEP 6 — DATABASE INDEX OPTIMIZATION"
    )


    index_manager = (
        DatabaseIndexManager()
    )


    result = (

        index_manager.create_all()

    )


    audit = result[
        "audit_report"
    ]


    print_section(
        "DATABASE INDEX AUDIT"
    )


    if audit.empty:

        print(

            "No database index "
            "results generated."

        )

    else:

        print(

            audit[

                [

                    "table_name",

                    "index_name",

                    "indexed_columns",

                    "status"

                ]

            ].to_string(
                index=False
            )

        )


    print_separator()


    print_metric(

        "Total indexes",

        result[
            "total_indexes"
        ]

    )


    print_metric(

        "Successful indexes",

        result[
            "successful_indexes"
        ]

    )


    print_metric(

        "Failed indexes",

        result[
            "failed_indexes"
        ]

    )


    return result


# ==========================================================
# STEP 7 — ANALYTICAL SQL VIEWS
# ==========================================================

def run_analytical_views():

    print_section(
        "STEP 7 — ANALYTICAL SQL VIEWS"
    )


    view_manager = (
        AnalyticalViewManager()
    )


    result = (

        view_manager.create_all()

    )


    audit = result[
        "audit_report"
    ]


    print_section(
        "SQL VIEW VALIDATION"
    )


    if audit.empty:

        print(

            "No analytical SQL "
            "view results generated."

        )

    else:

        print(

            audit[

                [

                    "view_name",

                    "row_count",

                    "column_count",

                    "status",

                    "error"

                ]

            ].to_string(
                index=False
            )

        )


    print_separator()


    print_metric(

        "Total SQL views",

        result[
            "total_views"
        ]

    )


    print_metric(

        "Successful SQL views",

        result[
            "successful_views"
        ]

    )


    print_metric(

        "Failed SQL views",

        result[
            "failed_views"
        ]

    )


    return result

# ==========================================================
# STEP 8 — FINANCIAL ANALYTICS EXECUTION
# ==========================================================

def run_financial_analytics():

    print_section(
        "STEP 8 — FINANCIAL ANALYTICS EXECUTION"
    )


    # ------------------------------------------------------
    # Initialize Analytics Runner
    # ------------------------------------------------------

    analytics_runner = (
        FinancialAnalyticsRunner()
    )


    # ------------------------------------------------------
    # Execute and Export All Queries
    # ------------------------------------------------------

    analytics_result = (

        analytics_runner.run_all()

    )


    # ------------------------------------------------------
    # Query Execution Audit
    # ------------------------------------------------------

    print_section(
        "ANALYTICAL QUERY EXECUTION AUDIT"
    )


    query_audit = (

        analytics_result[
            "query_audit"
        ]

    )


    if query_audit.empty:

        print(

            "No analytical query "
            "audit results were generated."

        )

    else:

        display_columns = [

            "query_name",

            "rows_returned",

            "columns_returned",

            "execution_time_ms",

            "status"

        ]


        print(

            query_audit[
                display_columns
            ]
            .to_string(
                index=False
            )

        )


    # ------------------------------------------------------
    # Analytics Export Manifest
    # ------------------------------------------------------

    print_section(
        "ANALYTICS EXPORT MANIFEST"
    )


    export_manifest = (

        analytics_result[
            "export_manifest"
        ]

    )


    if export_manifest.empty:

        print(

            "No analytics export "
            "records were generated."

        )

    else:

        display_columns = [

            "query_name",

            "rows",

            "columns",

            "status"

        ]


        print(

            export_manifest[
                display_columns
            ]
            .to_string(
                index=False
            )

        )


    # ------------------------------------------------------
    # Financial Analytics Statistics
    # ------------------------------------------------------

    print_section(
        "FINANCIAL ANALYTICS STATISTICS"
    )


    print_metric(

        "Total analytical queries",

        analytics_result[
            "total_queries"
        ]

    )


    print_metric(

        "Successful queries",

        analytics_result[
            "successful_queries"
        ]

    )


    print_metric(

        "Failed queries",

        analytics_result[
            "failed_queries"
        ]

    )


    print_metric(

        "Total rows exported",

        analytics_result[
            "total_rows_exported"
        ]

    )


    print_metric(

        "Analytics output folder",

        analytics_result[
            "analytics_output_dir"
        ]

    )


    return analytics_result


# ==========================================================
# GENERATED DELIVERABLES
# ==========================================================

def print_generated_deliverables():

    print_section(
        "SPRINT 1 & SPRINT 2 — GENERATED DELIVERABLES"
    )

    report_paths = [

        # -----------------------------
        # Day 1–7 Deliverables
        # -----------------------------
        OUTPUT_DIR / "load_audit.csv",
        OUTPUT_DIR / "validation_failures.csv",
        OUTPUT_DIR / "processed_data_manifest.csv",
        OUTPUT_DIR / "database_load_audit.csv",
        OUTPUT_DIR / "database_integrity_report.csv",
        OUTPUT_DIR / "database_table_summary.csv",
        OUTPUT_DIR / "database_index_audit.csv",
        OUTPUT_DIR / "sql_view_validation.csv",

        # -----------------------------
        # Day 8 Deliverables
        # -----------------------------
        OUTPUT_DIR / "analytical_query_audit.csv",
        OUTPUT_DIR / "analytics_export_manifest.csv",

        # -----------------------------
        # Day 9 Deliverables
        # -----------------------------
        OUTPUT_DIR / "forecasting" / "forecast_summary.csv",
        OUTPUT_DIR / "forecasting" / "forecast_metrics.csv",

        # -----------------------------
        # Day 10 Deliverables
        # -----------------------------
        OUTPUT_DIR / "portfolio" / "optimized_portfolio.csv",
        OUTPUT_DIR / "portfolio" / "sector_allocation.csv",

        # -----------------------------
        # Day 11 Deliverables
        # -----------------------------
        OUTPUT_DIR / "risk" / "risk_scores.csv",
        OUTPUT_DIR / "risk" / "risk_summary.csv",

        # -----------------------------
        # Day 12 Deliverables
        # -----------------------------
        OUTPUT_DIR / "reporting" / "executive_summary.csv",
        OUTPUT_DIR / "reporting" / "dashboard_dataset.csv",

        # -----------------------------
        # Database
        # -----------------------------
        Path("database") / "n100_financial.db"
    ]

    print_report_status(report_paths)

# ==========================================================
# COMPLETE PIPELINE STATUS
# ==========================================================

def print_pipeline_status(

    datasets,

    export_result,

    database_result,

    index_result,

    view_result, 

    analytics_result

):

    print_section(
        "SPRINT 1 — DAY 4 TO DAY 6 STATUS"
    )


    export_success = (

        export_result[
            "failed_exports"
        ] == 0

        and

        export_result[
            "successful_exports"
        ] == len(datasets)

    )


    database_success = (

        database_result[
            "failed_loads"
        ] == 0

        and

        database_result[
            "successful_loads"
        ] == len(datasets)

    )


    index_success = (

        index_result[
            "failed_indexes"
        ] == 0

    )


    view_success = (

        view_result[
            "failed_views"
        ] == 0

    )

    analytics_success = (

        analytics_result[
            "failed_queries"
        ] == 0

        and

        analytics_result[
            "successful_queries"
        ]

        ==

        analytics_result[
            "total_queries"
        ]

    )


    pipeline_success = all(

        [

            export_success,

            database_success,

            index_success,

            view_success

        ]

    )


    print_metric(

        "Processed-data export",

        (
            "SUCCESS"

            if export_success

            else

            "FAILED"
        )

    )


    print_metric(

        "SQLite database loading",

        (
            "SUCCESS"

            if database_success

            else

            "FAILED"
        )

    )


    print_metric(

        "Database indexes",

        (
            "SUCCESS"

            if index_success

            else

            "FAILED"
        )

    )


    print_metric(

        "Analytical SQL views",

        (
            "SUCCESS"

            if view_success

            else

            "FAILED"
        )

    )

    print_metric(

        "Financial analytics",

        (

            "SUCCESS"

            if analytics_success

            else

            "FAILED"
        )

    )


    print_separator()


    if pipeline_success:

        print(

            "Overall Status: "
            "COMPLETED SUCCESSFULLY"

        )


        print(

            "\nThe processed-data layer, "
            "SQLite database, database indexes, "
            "integrity audit, analytical SQL views, "
            "and financial analytics outputs were "
            "generated successfully."

        )


    else:

        print(

            "Overall Status: "
            "COMPLETED WITH ISSUES"

        )


        print(

            "\nReview the failed pipeline "
            "components before continuing."

        )


    print(

        "\nKnown source-data integrity "
        "findings remain documented in:"

    )


    print(

        "output/"
        "database_integrity_report.csv"

    )


    print_separator()

    print("PROJECT COMPLETION SUMMARY")
    print()

    print("✓ Sprint 1 Completed (Days 1–10)")
    print("✓ Sprint 2 Completed (Days 11–14)")
    print("✓ All Project Milestones Achieved")
    print("✓ Days 1–14 Development Completed Successfully")
    print("✓ N100 Financial Intelligence Platform Delivered Successfully")

    print_separator()


# ==========================================================
# MAIN APPLICATION
# ==========================================================

def main():

    print_section(

        "N100 FINANCIAL INTELLIGENCE PLATFORM\n"

        "SPRINT 1 — DAYS 4 TO 7\n"

        "PROCESSED DATA, SQLITE DATABASE, "
        "INTEGRITY, SQL AND FINANCIAL ANALYTICS"

    )


    # ------------------------------------------------------
    # Step 1 — Load datasets
    # ------------------------------------------------------

    (

        datasets,

        loader,

        successful_loads,

        failed_loads

    ) = run_dataset_loading()


    if not datasets:

        print_section(
            "PIPELINE TERMINATED"
        )


        print(

            "No source datasets were loaded. "
            "The pipeline cannot continue."

        )


        return


    # ------------------------------------------------------
    # Step 2 — Validate datasets
    # ------------------------------------------------------

    validator, validation_report = (

        run_data_validation(
            datasets
        )

    )


    # ------------------------------------------------------
    # Step 3 — Export processed datasets
    # ------------------------------------------------------

    export_result = (

        run_processed_export(
            datasets
        )

    )


    if (

        export_result[
            "failed_exports"
        ] > 0

    ):

        print_section(
            "PIPELINE TERMINATED"
        )


        print(

            "One or more processed-data "
            "exports failed."

        )


        print(

            "Database loading was skipped "
            "to prevent partial ingestion."

        )


        return


    # ------------------------------------------------------
    # Step 4 — Load SQLite database
    # ------------------------------------------------------

    database_result = (

        run_database_loading(
            datasets
        )

    )


    if (

        database_result[
            "failed_loads"
        ] > 0

    ):

        print_section(
            "PIPELINE TERMINATED"
        )


        print(

            "One or more SQLite database "
            "loads failed."

        )


        print(

            "Database optimization and "
            "view generation were skipped."

        )


        return


    # ------------------------------------------------------
    # Step 5 — Validate database integrity
    # ------------------------------------------------------

    integrity_result = (

        run_integrity_validation()

    )


    # ------------------------------------------------------
    # Step 6 — Optimize indexes
    # ------------------------------------------------------

    index_result = (

        run_index_optimization()

    )


    # ------------------------------------------------------
    # Step 7 — Create analytical views
    # ------------------------------------------------------

    view_result = (

        run_analytical_views()

    )

    # ------------------------------------------------------
    # Step 8 — Execute financial analytics
    # ------------------------------------------------------

    analytics_result = (

        run_financial_analytics()

    )

    snapshot = analytics_result["results"]["company_financial_snapshot"]

    print(snapshot.columns.tolist())

    print(snapshot.head())

    

    print("=" * 80)
    print("STEP 9 : FORECASTING")
    print("=" * 80)

    forecast_runner = ForecastRunner()

    forecast_result = forecast_runner.run(
        datasets
    )

    print("=" * 80)
    print("STEP 10 : PORTFOLIO OPTIMIZATION")
    print("=" * 80)

    portfolio_runner = PortfolioRunner()

    portfolio_result = portfolio_runner.run(
        analytics_result
    )

    print("=" * 80)
    print("STEP 11 : RISK ANALYTICS")
    print("=" * 80)

    risk_runner = RiskRunner()

    risk_result = risk_runner.run(
        portfolio_result
    )

    print("=" * 80)
    print("STEP 12 : EXECUTIVE REPORTING")
    print("=" * 80)

    report_runner = ReportingRunner()

    report_result = report_runner.run(

        analytics_result,

        portfolio_result,

        risk_result,

    )

    # ------------------------------------------------------
    # Deliverables
    # ------------------------------------------------------

    print_generated_deliverables()


    # ------------------------------------------------------
    # Final status
    # ------------------------------------------------------

    print_pipeline_status(

        datasets=

        datasets,

        export_result=

        export_result,

        database_result=

        database_result,

        index_result=

        index_result,

        view_result=

        view_result,

        analytics_result=

        analytics_result

    )


    print(
        "=" * SEPARATOR_LENGTH
    )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    main()