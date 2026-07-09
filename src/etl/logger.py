from loguru import logger as loguru_logger
from src.etl.config import LOG_DIR

# Remove default logger
loguru_logger.remove()

# File logger
loguru_logger.add(
    LOG_DIR / "etl.log",
    rotation="5 MB",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Console logger
loguru_logger.add(
    lambda msg: print(msg, end=""),
    level="INFO"
)

# Export logger
logger = loguru_logger