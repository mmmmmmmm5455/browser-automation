# 任务模型
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"       # 失败
    CANCELLED = "cancelled"  # 已取消


class TaskBase(BaseModel):
    """任务基础模型"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        arbitrary_types_allowed = True


class Task(TaskBase):
    """任务模型"""
    id: str
    title: str
    description: str
    user_input: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None
    
    class Config:
        use_enum_values = True


class TaskCreate(TaskBase):
    """创建任务请求"""
    title: str
    description: str = ""
    user_input: str


class TaskUpdate(TaskBase):
    """更新任务请求"""
    status: Optional[TaskStatus] = None
    result: Optional[str] = None
    error: Optional[str] = None


class Task(Task):
    """完整任务模型"""
    id: str
    title: str
    description: str
    user_input: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None
    steps: List[str] = []
    execution_log: List[str] = []
    
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
