# 配置管理
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger(__name__)

# 加载环境变量
load_dotenv()


class Config:
    """配置管理器"""
    
    # API 配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # LLM 配置
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))
    
    # 浏览器配置
    BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))  # 30秒
    BROWSER_SLOW_MO = int(os.getenv("BROWSER_SLOW_MO", "0"))  # 慢速模式
    BROWSER_USER_AGENT = os.getenv("BROWSER_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    BROWSER_VIEWPORT_WIDTH = int(os.getenv("BROWSER_VIEWPORT_WIDTH", "1280"))
    BROWSER_VIEWPORT_HEIGHT = int(os.getenv("BROWSER_VIEWPORT_HEIGHT", "720"))
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/browsers.db")
    
    # 存储配置
    SCREENSHOT_DIR = "screenshots"
    DATA_DIR = "data"
    LOG_DIR = "logs"
    
    # LangChain 配置
    LANGCHAIN_VERBOSE = os.getenv("LANGCHAIN_VERBOSE", "false").lower() == "true"
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """获取配置项"""
        value = os.getenv(key, default)
        return value if value else default
    
    @classmethod
    def get_int(cls, key: str, default: int = 0) -> int:
        """获取整数配置项"""
        value = os.getenv(key, "")
        return int(value) if value else default
    
    @classmethod
    def get_bool(cls, key: str, default: bool = False) -> bool:
        """获取布尔配置项"""
        value = os.getenv(key, "")
        return value.lower() == "true" if value else default
    
    @classmethod
    def get_list(cls, key: str, default: list = None) -> list:
        """获取列表配置项（逗号分隔）"""
        value = os.getenv(key, "")
        return [item.strip() for item in value.split(",")] if value else default
    
    @classmethod
 def get_dict(cls, key: str, default: dict = None) -> dict:
        """获取字典配置项（JSON 字符串）"""
        value = os.getenv(key, "")
        return json.loads(value) if value else default
    
    def validate(self) -> bool:
        """验证配置"""
        errors = []
        
        # 验证必填配置
        if not self.OPENAI_API_KEY and not self.ANTHROPIC_API_KEY:
            errors.append("至少配置一个 LLM API Key（OPENAI_API_KEY 或 ANTHROPIC_API_KEY）")
        
        if errors:
            logger.error(f"配置验证失败: {', '.join(errors)}")
            return False
        
        logger.info("✅ 配置验证通过")
        return True
    
    def get_env_dict(self) -> Dict[str, str]:
        """获取所有环境变量"""
        return {
            "OPENAI_API_KEY": "***HIDDEN***",
            "ANTHROPIC_API_KEY": "***HIDDEN***",
            "LLM_MODEL": self.LLM_MODEL,
            "LLM_TEMPERATURE": str(self.LLM_TEMPERATURE),
            "LLM_MAX_TOKENS": str(self.LLM_MAX_TOKENS),
            "BROWSER_HEADLESS": str(self.BROWSER_HEADLESS),
            "BROWSER_TIMEOUT": str(self.BROWSER_TIMEOUT),
            "BROWSER_SLOW_MO": str(self.BROWSER_SLOW_MO),
            "BROWSER_USER_AGENT": self.BROWSER_USER_AGENT[:50] + "...",
            "HOST": self.HOST,
            "PORT": str(self.PORT),
            "DEBUG": str(self.DEBUG),
        }
