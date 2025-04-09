from pathlib import Path
from loguru import logger

class Settings():
    basedir = Path.cwd() / r"../../../data"
    rawdir = Path("raw")
    proccesddir = Path("processed")
    logdir = basedir / "log"

settings = Settings()
logger.add("logfile_week_log")