import sys
import logging

log_format = '[%(asctime)s] %(levelname)s %(message)s'
datetime_format = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(filename="cdncert.log",
                    filemode="w",
                    format=log_format,
                    datefmt=datetime_format,
                    level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(fmt=log_format, datefmt=datetime_format))

logging.getLogger().addHandler(console)

log = logging.getLogger(__name__)
