import logging

class AppLogger:
    def __init__(self, name, log_dir):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        log_file = log_dir / f"{name}.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
