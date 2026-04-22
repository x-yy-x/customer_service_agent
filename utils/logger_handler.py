import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime

LOG_ROOT = get_abs_path("logs")

os.makedirs(LOG_ROOT, exist_ok=True)

DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )  

def get_logger(name:str = "agent", 
               console_level: int=logging.INFO,
               file_level: int=logging.DEBUG,
               log_file = None
               ) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to the lowest level to capture all logs
    
    # 防止重复添加处理器
    if logger.handlers:
        return logger  # Logger already has handlers, return it directly
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)
    
    # File handler
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
        
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)
    
    return logger


logger = get_logger()

if __name__ == "__main__":
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.warning("This is a critical message.")