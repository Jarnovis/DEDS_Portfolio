from pathlib import Path
from loguru import logger

class Settings():
    basedir = Path.cwd()
    rawdir = Path("../data/raw")
    processedir = Path("../data/processed")
    logdir = basedir / "log"
    
    sales_activity_columns = [
        
    ]

settings = Settings()
logger.add("logfile.log")