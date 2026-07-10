import pandas as pd

from src.etl.validation_rules import ValidationRules
from src.etl.validation_config import (
    DATASET_CONFIG,
    TOLERANCE
)
from src.etl.config import OUTPUT_DIR
from src.etl.logger import logger


class DataValidator:
    """
    Enterprise Data Quality Validator
    Sprint 1 - Day 3
    """

    def __init__(self):

        self.results = []

    # -------------------------------------------------------
    # Helper
    # -------------------------------------------------------

    def add_result(
        self,
        dataset,
        rule,
        severity,
        failures
    ):

        self.results.append({
            "dataset": dataset,
            "rule": rule,
            "severity": severity,
            "failures": failures
        })

    # -------------------------------------------------------
    # Validate One Dataset
    # -------------------------------------------------------

    def validate_dataset(
        self,
        dataset_name,
        df,
        datasets
    ):

        logger.info(
            f"Validating {dataset_name}"
        )

        config = DATASET_CONFIG.get(
            dataset_name,
            {}
        )

        # ===================================================
        # DQ-01
        # ===================================================

        if "primary_key" in config:

            failed = ValidationRules.check_primary_key(
                df,
                config["primary_key"]
            )

            self.add_result(
                dataset_name,
                "DQ-01",
                "CRITICAL",
                len(failed)
            )

        # ===================================================
        # DQ-02
        # ===================================================

        if "composite_key" in config:

            failed = ValidationRules.check_composite_key(
                df,
                config["composite_key"]
            )

            self.add_result(
                dataset_name,
                "DQ-02",
                "CRITICAL",
                len(failed)
            )

        # ===================================================
        # DQ-03
        # ===================================================

        if "foreign_key" in config:

            fk = config["foreign_key"]

            master = datasets[
                fk["master_dataset"]
            ]

            failed = ValidationRules.check_foreign_key(
                df,
                fk["column"],
                master,
                fk["master_key"]
            )

            self.add_result(
                dataset_name,
                "DQ-03",
                "CRITICAL",
                len(failed)
            )

        # ===================================================
        # DQ-04
        # ===================================================

        failed = ValidationRules.check_duplicate_rows(
            df
        )

        self.add_result(
            dataset_name,
            "DQ-04",
            "WARNING",
            len(failed)
        )

        # ===================================================
        # DQ-05
        # ===================================================

        if "mandatory" in config:

            failed = ValidationRules.check_mandatory_fields(
                df,
                config["mandatory"]
            )

            self.add_result(
                dataset_name,
                "DQ-05",
                "CRITICAL",
                len(failed)
            )

        # ===================================================
        # DQ-06
        # ===================================================

        if "sales" in df.columns:

            failed = ValidationRules.check_positive_sales(
                df
            )

            self.add_result(
                dataset_name,
                "DQ-06",
                "CRITICAL",
                len(failed)
            )

        # ===================================================
        # DQ-07
        # ===================================================

        if "operating_profit" in df.columns:

            failed = ValidationRules.check_operating_profit(
                df,
                TOLERANCE["operating_profit"]
            )

            self.add_result(
                dataset_name,
                "DQ-07",
                "WARNING",
                len(failed)
            )

        # ===================================================
        # DQ-08
        # ===================================================

        if "total_assets" in df.columns:

            failed = ValidationRules.check_balance_sheet(
                df,
                TOLERANCE["balance_sheet"]
            )

            self.add_result(
                dataset_name,
                "DQ-08",
                "CRITICAL",
                len(failed)
            )

        # ===================================================
        # DQ-09
        # ===================================================

        if "net_cash_flow" in df.columns:

            failed = ValidationRules.check_cash_flow(
                df,
                TOLERANCE["cash_flow"]
            )

            self.add_result(
                dataset_name,
                "DQ-09",
                "WARNING",
                len(failed)
            )

        # ===================================================
        # DQ-10
        # ===================================================

        if "tax_percentage" in df.columns:

            failed = ValidationRules.check_tax_rate(df)

            self.add_result(
                dataset_name,
                "DQ-10",
                "WARNING",
                len(failed)
            )

        # ===================================================
        # DQ-11
        # ===================================================

        if "dividend_payout" in df.columns:

            failed = ValidationRules.check_dividend(df)

            self.add_result(
                dataset_name,
                "DQ-11",
                "WARNING",
                len(failed)
            )

        # ===================================================
        # DQ-12
        # ===================================================

        if "eps" in df.columns:

            failed = ValidationRules.check_eps(df)

            self.add_result(
                dataset_name,
                "DQ-12",
                "WARNING",
                len(failed)
            )

        # ===================================================
        # DQ-13
        # ===================================================

        failed = ValidationRules.check_url(df)

        self.add_result(
            dataset_name,
            "DQ-13",
            "WARNING",
            len(failed)
        )

        # ===================================================
        # DQ-14
        # ===================================================

        # if "year" in df.columns:

        #     failed = ValidationRules.check_year(df)

        #     self.add_result(
        #         dataset_name,
        #         "DQ-14",
        #         "CRITICAL",
        #         len(failed)
        #     )

        if config.get("validate_year", False):

            failed = ValidationRules.check_year(df)

            self.add_result(
                dataset_name,
                "DQ-14",
                "CRITICAL",
                len(failed)
            )

        # ===================================================
        # DQ-15
        # ===================================================

        failed = ValidationRules.check_numeric(
            df,
            config.get("numeric_columns", [])
        )

        self.add_result(
            dataset_name,
            "DQ-15",
            "WARNING",
            len(failed)
        )

        # ===================================================
        # DQ-16
        # ===================================================

        if "company_id" in df.columns:

            failed = ValidationRules.check_company_coverage(df)

            self.add_result(
                dataset_name,
                "DQ-16",
                "WARNING",
                len(failed)
            )

        # -------------------------------------------------------
    # Validate All Datasets
    # -------------------------------------------------------

    def validate_all(self, datasets):
        """
        Execute all validation rules for every dataset and
        generate validation report.
        """

        logger.info("Starting Data Quality Validation...")

        self.results = []

        # Validate every dataset
        for dataset_name, df in datasets.items():

            self.validate_dataset(
                dataset_name=dataset_name,
                df=df,
                datasets=datasets
            )

        # ----------------------------
        # Create Report
        # ----------------------------

        report = pd.DataFrame(self.results)

        report.sort_values(
            by=["dataset", "rule"],
            inplace=True
        )

        report.to_csv(
            OUTPUT_DIR / "validation_failures.csv",
            index=False
        )

        logger.success(
            "Validation report saved successfully."
        )

        return report

    # -------------------------------------------------------
    # Validation Statistics
    # -------------------------------------------------------

    @staticmethod
    def validation_summary(report):
        """
        Return validation statistics.
        """

        total_rules = len(report)

        passed = len(
            report[
                report["failures"] == 0
            ]
        )

        failed = len(
            report[
                report["failures"] > 0
            ]
        )

        critical = len(
            report[
                (report["severity"] == "CRITICAL")
                &
                (report["failures"] > 0)
            ]
        )

        warning = len(
            report[
                (report["severity"] == "WARNING")
                &
                (report["failures"] > 0)
            ]
        )

        return {
            "total_rules": total_rules,
            "passed": passed,
            "failed": failed,
            "critical": critical,
            "warning": warning
        }

    # -------------------------------------------------------
    # Console Report
    # -------------------------------------------------------

    @staticmethod
    def print_summary(report):

        stats = DataValidator.validation_summary(report)

        print("\n")
        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)

        failed = report[
            report["failures"] > 0
        ]

        if failed.empty:

            print("\nNo validation failures found.\n")

        else:

            print(
                failed.to_string(index=False)
            )

        print("\n")
        print("=" * 80)
        print("VALIDATION STATISTICS")
        print("=" * 80)

        print(
            f"Total Rules Executed : {stats['total_rules']}"
        )

        print(
            f"Passed               : {stats['passed']}"
        )

        print(
            f"Failed               : {stats['failed']}"
        )

        print(
            f"Critical Issues      : {stats['critical']}"
        )

        print(
            f"Warnings             : {stats['warning']}"
        )

        print("=" * 80)

        print("\nGenerated Files")

        print("✓ output/validation_failures.csv")