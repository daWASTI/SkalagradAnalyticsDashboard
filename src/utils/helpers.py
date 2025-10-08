import logging
import colorlog

def setup_logging(level=logging.INFO) -> logging.Logger:
    """Configure and return a colored logger."""
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }
    ))

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)