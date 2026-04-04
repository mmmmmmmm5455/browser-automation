# 辅助函数
from typing import List, Dict, Any, Optional
import time
import json
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger(__name__)


def format_duration(seconds: float) -> str:
    """格式化时长"""
    if seconds < 60:
        return f"{seconds:.2f} 秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} 分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} 小时"


def parse_json_safely(json_str: str) -> Optional[Dict]:
    """安全解析 JSON"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}")
        return None
    except Exception as e:
        logger.error(f"解析 JSON 时出错: {e}")
        return None


def sanitize_filename(filename: str) -> str:
    """清理文件名"""
    # 移除非法字符
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    
    # 限制文件名长度
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename


def create_directories(*dirs: str) -> None:
    """创建目录"""
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.debug(f"创建目录: {dir_path}")


def is_url(text: str) -> bool:
    """检查是否为 URL"""
    import re
    url_pattern = r'^https?://(?:[-\w.]?)+\.+[a-z]{2,}(?:[/\?][^\s]*)?$'
    return re.match(url_pattern, text) is not None


def extract_url(text: str) -> Optional[str]:
    """从文本中提取 URL"""
    import re
    urls = re.findall(r'https?://(?:[-\w.]?)+\.+[a-z]{2,}(?:[/\?][^\s]*)?$', text)
    return urls[0] if urls else None


def extract_emails(text: str) -> List[str]:
    """从文本中提取邮箱"""
    import re
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return emails


def extract_phone_numbers(text: str) -> List[str]:
    """从文本中提取手机号"""
    import re
    phones = re.findall(r'1[3-9]\d{9}', text)
    return phones


def format_timestamp(timestamp: int) -> str:
    """格式化时间戳"""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def clean_text(text: str) -> str:
    """清理文本（移除多余空白）"""
    return " ".join(text.split())
