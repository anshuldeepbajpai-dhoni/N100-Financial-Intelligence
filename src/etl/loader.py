import pandas as pd
from datetime import datetime

from src.etl.config import (
    RAW_DATA,
    SUPPLEMENTARY_DATA,
    CORE_DATASETS,
    OUTPUT_DIR
)

from src.etl.normalizer import DataNormalizer
from src.etl.logger import logger


class ExcelLoader:
    """
    Generic Excel Loader
    """

    def __init__(self):

        self.datasets = {}

        self.audit = []

    def load(self, filename):

        if filename in CORE_DATASETS:
            path = RAW_DATA / filename
            header = 1
        else:
            path = SUPPLEMENTARY_DATA / filename
            header = 0

        start = datetime.now()

        try:

            logger.info(f"Loading {filename}")

            df = pd.read_excel(
                path,
                header=header
            )

            df = DataNormalizer.clean(df)

            self.datasets[filename] = df

            end = datetime.now()

            self.audit.append({
                "dataset": filename,
                "rows": len(df),
                "columns": len(df.columns),
                "status": "Loaded",
                "load_time_sec": round(
                    (end - start).total_seconds(),
                    3
                )
            })

            logger.success(
                f"{filename} Loaded "
                f"Rows={len(df)} "
                f"Columns={len(df.columns)}"
            )

            return df

        except Exception as e:

            logger.error(f"{filename} : {e}")

            self.audit.append({
                "dataset": filename,
                "rows": 0,
                "columns": 0,
                "status": "Failed",
                "load_time_sec": 0
            })

    def load_all(self, file_list):

        for file in file_list:
            self.load(file)

        self.generate_audit()

        return self.datasets

    def generate_audit(self):

        audit = pd.DataFrame(self.audit)

        audit.to_csv(
            OUTPUT_DIR / "load_audit.csv",
            index=False
        )

        logger.success(
            f"Load audit saved to {OUTPUT_DIR/'load_audit.csv'}"
        )