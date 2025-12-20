"""Logger configuration for the benchmark infrastructure."""
import logging
import os
import sys
from typing import Optional

_LOG_DIR: Optional[str] = None


def setup_logging(log_dir: str = "logs") -> None:
    """
    Initialize the logging infrastructure by creating the log directory.

    Args:
        log_dir: Directory where log files will be stored

    Example:
        setup_logging("logs")
        logger = get_logger("my_module")
    """
    global _LOG_DIR
    _LOG_DIR = log_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def get_logger(
    name: str,
    use_file: bool = True,
    use_stdout: bool = True,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Get or create a logger with the specified configuration.

    Args:
        name: Name of the logger (typically module name or component name)
        use_file: Whether to add a file handler (default: True)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance

    Raises:
        RuntimeError: If setup_logging() has not been called first

    Example:
        logger = get_logger("bootstrap", use_file=True, level=logging.DEBUG)
        logger.info("Starting bootstrap process")
    """
    if _LOG_DIR is None:
        raise RuntimeError("setup_logging() must be called before get_logger()")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    logger.propagate = False
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    file_fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_fmt = logging.Formatter("%(levelname)s: %(message)s")

    # Console Handler (always added)
    if use_stdout:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(console_fmt)
        ch.setLevel(level)
        logger.addHandler(ch)

    # File Handler (optional)
    if use_file:
        log_file = os.path.join(_LOG_DIR, f"{name}.log")
        fh = logging.FileHandler(log_file)
        fh.setFormatter(file_fmt)
        fh.setLevel(level)
        logger.addHandler(fh)

    return logger
