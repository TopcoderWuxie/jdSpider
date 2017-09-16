#coding: utf-8

"""
DEBUG	获得诊断问题是具体的信息
INFO	确认程序是否按正常工作
WARNING	在程序还正常运行时获取发生的意外的信息，这可能会在之后引发异常（例如磁盘空间不足）
ERROR	获取程序某些功能无法正常调用这类严重异常的信息
CRITICAL	获取程序无法继续运行的这类最严重异常信息
"""

import logging
import logging.handlers

def Init():
    global logger
    LOG_FILE = 'Logging.log'  
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
    fmt = '%(asctime)s - %(levelname)s - %(message)s'  

    formatter = logging.Formatter(fmt)   # 实例化formatter  
    handler.setFormatter(formatter)      # 为handler添加formatter  
      
    logger = logging.getLogger('Logging')    # 获取名为Logging的logger  
    logger.addHandler(handler)           # 为logger添加handler  
    logger.setLevel(logging.DEBUG)

def logging_save(*args):
    if args[1] == "DEBUG":
        logger.debug(args[0])
    elif args[1] == "INFO":
        logger.info(args[0])
    elif args[1] == "WARNING":
        logger.warn(args[0])
    elif args[1] == "ERROR":
        logger.error(args[0])
    elif args[1] == "CRITICAL":
        logger.critical(args[0])