import logging
from pathlib import Path

class Logger(object):
    def __init__(self, name: str, log_dir: str = "logs", log_level: int = logging.INFO):
        """
        Initializes the Logger instance.

        Args:
            name (str): The name of the logger (usually the module name).
            log_dir (str): Directory to save the log files.
            log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Prevent duplicate log entries if multiple handlers are added
        if not self.logger.handlers:
            self._add_stream_handler()
            self._add_file_handler()

    def _add_stream_handler(self):
        """Adds a stream handler for console output."""
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(stream_handler)

    def _add_file_handler(self):
        """Adds a file handler for saving logs to a file."""
        log_file = self.log_dir / f"{self.name}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

    def _get_formatter(self):
        """Returns a log formatter."""
        return logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def get_logger(self):
        """Returns the logger instance."""
        return self.logger
