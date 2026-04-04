# 日志工具
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# 日志配置
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = logging.INFO


def setup_logger(name: str = __name__, log_level: str = LOG_LEVEL):
    """配置日志"""
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志文件
    log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    # 配置处理器
    file_handler = logging.FileHandler(
        filename=log_file,
        mode='a',
        encoding='utf-8',
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )
    console_handler = logging.StreamHandler(sys.stdout)
    
    # 设置级别
    file_handler.setLevel(log_level)
    console_handler.setLevel(log_level)
    
    # 配置格式
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # 添加处理器
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # 添加处理器
    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = __name__):
    """获取日志器（单例模式）"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        return setup_logger(name)
    
    return logger


def log_function_call(func):
    """装饰器：记录函数调用"""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__name__)
        
        func_name = func.__name__
        args_str = ", ".join([str(a) for a in args])
        kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        
        logger.debug(f"调用函数: {func_name}({args_str}, {kwargs_str})")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"函数返回: {func_name} -> {result}")
            return result
        except Exception as e:
            logger.error(f"函数异常: {func_name} -> {e}")
            raise
    
    return wrapper


def log_exception(logger: logging.Logger, func_name: str, exception: Exception):
    """记录异常"""
    import traceback
    
    logger.error(f"函数异常: {func_name}")
    logger.error(f"异常信息: {str(exception)}")
    logger.error("异常堆栈:")
    logger.error(traceback.format_exc())


def log_execution_time(logger: logging.Logger, func_name: str, start_time: float):
    """记录执行时间"""
    execution_time = datetime.now().timestamp() - start_time
    logger.info(f"函数执行完成: {func_name}，耗时: {execution_time:.2f}秒")
    return execution_time
