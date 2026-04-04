# 执行记录模型
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any, JSON
from enum import Enum


class ExecutionStatus(str, Enum):
    """执行状态"""
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    SUCCESS = "success"      # 成功
    FAILED = "failed"       # 失败
    ERROR = "error"         # 错误


class ExecutionBase(BaseModel):
    """执行记录基础模型"""
    id: str
    task_id: str
    step: str
    input: str
    output: str
    status: ExecutionStatus
    timestamp: datetime
    
    class Config:
        arbitrary_types_allowed = True


class Execution(ExecutionBase):
    """执行记录"""
    id: str
    task_id: str
    step: str
    input: str
    output: str
    status: ExecutionStatus
    timestamp: datetime
    duration_ms: Optional[float] = None
    screenshot_path: Optional[str] = None
    
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class ExecutionCreate(BaseModel):
    """创建执行记录请求"""
    task_id: str
    step: str
    input: str
    output: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    screenshot_path: Optional[str] = None
    duration_ms: Optional[float] = None


class ExecutionUpdate(ExecutionBase):
    """更新执行记录请求"""
    status: Optional[ExecutionStatus] = None
    output: Optional[str] = None
    screenshot_path: Optional[str] = None
    duration_ms: Optional[float] = None
    error: Optional[str] = None
