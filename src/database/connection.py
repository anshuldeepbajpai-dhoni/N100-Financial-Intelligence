import sqlite3

from contextlib import contextmanager

from src.etl.config import (
    DATABASE_PATH
)

from src.etl.logger import logger


# ==========================================================
# DATABASE CONNECTION MANAGER
# ==========================================================

class DatabaseConnection:

    """
    Manages SQLite database connections for the
    N100 Financial Intelligence Platform.
    """

    def __init__(
        self,
        database_path=DATABASE_PATH
    ):

        self.database_path = (
            database_path
        )


    # ------------------------------------------------------
    # Create Database Connection
    # ------------------------------------------------------

    def connect(self):

        try:

            connection = sqlite3.connect(
                self.database_path
            )

            # Enable SQLite foreign-key enforcement
            connection.execute(
                "PRAGMA foreign_keys = ON;"
            )

            logger.success(

                "SQLite database connection "
                "established successfully."

            )

            return connection

        except sqlite3.Error as error:

            logger.error(

                "SQLite database connection "
                f"failed: {error}"

            )

            raise


    # ------------------------------------------------------
    # Transaction-Safe Connection
    # ------------------------------------------------------

    @contextmanager
    def transaction(self):

        connection = None

        try:

            connection = self.connect()

            yield connection

            connection.commit()

            logger.success(

                "Database transaction "
                "committed successfully."

            )

        except Exception as error:

            if connection is not None:

                connection.rollback()

                logger.error(

                    "Database transaction "
                    "rolled back."

                )

            logger.error(

                f"Database operation failed: "
                f"{error}"

            )

            raise

        finally:

            if connection is not None:

                connection.close()

                logger.info(

                    "SQLite database "
                    "connection closed."

                )