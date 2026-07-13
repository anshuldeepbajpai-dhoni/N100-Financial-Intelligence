from datetime import datetime

import pandas as pd

from src.etl.config import (
    PROCESSED_DATA,
    OUTPUT_DIR
)

from src.etl.logger import logger


class ProcessedDataExporter:

    """
    Export normalized and validated datasets
    into the processed-data layer.
    """

    def __init__(self):

        self.export_audit = []


    # ======================================================
    # EXPORT ONE DATASET
    # ======================================================

    def export_dataset(
        self,
        dataset_name,
        df
    ):

        """
        Export one processed DataFrame as CSV.
        """

        start_time = datetime.now()

        output_name = (
            dataset_name
            .replace(
                ".xlsx",
                ".csv"
            )
        )

        output_path = (
            PROCESSED_DATA
            / output_name
        )

        try:

            # --------------------------------------------------
            # Validate DataFrame
            # --------------------------------------------------

            if df is None:

                raise ValueError(
                    "DataFrame is None."
                )

            if not isinstance(
                df,
                pd.DataFrame
            ):

                raise TypeError(
                    "Object is not a pandas DataFrame."
                )

            # --------------------------------------------------
            # Create processed directory
            # --------------------------------------------------

            PROCESSED_DATA.mkdir(
                parents=True,
                exist_ok=True
            )

            # --------------------------------------------------
            # Export processed CSV
            # --------------------------------------------------

            df.to_csv(
                output_path,
                index=False,
                encoding="utf-8"
            )

            # --------------------------------------------------
            # Verify exported file
            # --------------------------------------------------

            verification_df = (
                pd.read_csv(
                    output_path
                )
            )

            expected_rows = len(
                df
            )

            exported_rows = len(
                verification_df
            )

            if (
                expected_rows
                != exported_rows
            ):

                raise ValueError(

                    "Row-count mismatch. "

                    f"Expected "
                    f"{expected_rows}, "

                    f"exported "
                    f"{exported_rows}."

                )

            # --------------------------------------------------
            # Calculate export metadata
            # --------------------------------------------------

            end_time = (
                datetime.now()
            )

            export_time = (

                end_time
                - start_time

            ).total_seconds()

            file_size = (

                output_path
                .stat()
                .st_size

            )

            # --------------------------------------------------
            # Add successful audit record
            # --------------------------------------------------

            self.export_audit.append({

                "dataset": (
                    dataset_name
                ),

                "output_file": (
                    output_name
                ),

                "rows": (
                    len(df)
                ),

                "columns": (
                    len(
                        df.columns
                    )
                ),

                "file_size_bytes": (
                    file_size
                ),

                "export_time_sec": round(
                    export_time,
                    3
                ),

                "status": (
                    "SUCCESS"
                ),

                "error": (
                    ""
                )
            })

            logger.success(

                f"{dataset_name} exported "

                f"Rows={len(df)} "

                f"Columns="
                f"{len(df.columns)}"

            )

            return output_path


        except Exception as error:

            # --------------------------------------------------
            # Add failed audit record
            # --------------------------------------------------

            self.export_audit.append({

                "dataset": (
                    dataset_name
                ),

                "output_file": (
                    output_name
                ),

                "rows": 0,

                "columns": 0,

                "file_size_bytes": 0,

                "export_time_sec": 0,

                "status": (
                    "FAILED"
                ),

                "error": (
                    str(error)
                )
            })

            logger.error(

                f"Export failed: "

                f"{dataset_name} : "

                f"{error}"

            )

            return None


    # ======================================================
    # EXPORT ALL DATASETS
    # ======================================================

    def export_all(
        self,
        datasets
    ):

        """
        Export all cleaned datasets.
        """

        logger.info(

            "Starting processed-data export..."

        )

        exported_files = {}


        for (
            dataset_name,
            df

        ) in datasets.items():


            output_path = (

                self.export_dataset(

                    dataset_name,

                    df

                )

            )


            if output_path is not None:

                exported_files[

                    dataset_name

                ] = output_path


        # --------------------------------------------------
        # Generate export manifest
        # --------------------------------------------------

        self.generate_manifest()


        return exported_files


    # ======================================================
    # GENERATE EXPORT MANIFEST
    # ======================================================

    def generate_manifest(self):

        """
        Generate metadata report for all exports.
        """

        manifest = (

            pd.DataFrame(

                self.export_audit

            )

        )


        manifest_path = (

            OUTPUT_DIR

            / "processed_data_manifest.csv"

        )


        manifest.to_csv(

            manifest_path,

            index=False

        )


        logger.success(

            "Processed-data manifest saved: "

            f"{manifest_path}"

        )


        return manifest