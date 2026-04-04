# FastAPI 主应用
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from datetime import datetime
import json
import logging

from .api.agent import create_browser_agent, execute_agent_task
from .models.task import Task, TaskStatus, TaskCreate
from .models.execution import Execution, ExecutionStatus
from core.browser_controller import BrowserController
from core.form_filler import FormFiller
from core.data_extractor import DataExtractor
from utils.logger import setup_logger

# 设置日志
setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="智能浏览器自动化 API",
    description="基于 AI 的智能浏览器自动化工具",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
browser_controller = None


@asynccontextmanager
async def get_browser():
    """获取浏览器实例（单例模式）"""
    global browser_controller
    
    if browser_controller is None:
        browser_controller = BrowserController()
        browser_controller.start(headless=True)
    
    try:
        yield browser_controller
    finally:
        pass  # 不关闭浏览器，保持运行


@app.on_event("startup")
async def startup_event():
    """启动事件"""
    logger.info("🚀 浏览器自动化服务启动")
    global browser_controller
    browser_controller = BrowserController()
    browser_controller.start(headless=True)
    logger.info("✅ 浏览器已启动")


@app.on_event("shutdown")
async def shutdown_event():
    """关闭事件"""
    logger.info("🛑 浏览器自动化服务关闭")
    global browser_controller
    if browser_controller:
        browser_controller.close()
        logger.info("✅ 浏览器已关闭")


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "智能浏览器自动化 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.post("/api/tasks", response_model=Task)
async def create_task(task_data: TaskCreate):
    """创建新任务"""
    try:
        # 创建任务
        task = Task(
            id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=task_data.title,
            description=task_data.description,
            user_input=task_data.user_input,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        logger.info(f"创建任务: {task.id} - {task.title}")
        
        # 异步执行任务
        import asyncio
        asyncio.create_task(execute_background_task(task))
        
        return task
        
    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks")
async def list_tasks(status: TaskStatus = None):
    """获取任务列表"""
    # TODO: 从数据库获取任务列表
    return []


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """获取任务详情"""
    # TODO: 从数据库获取任务详情
    return {"task_id": task_id}


@app.get("/api/tasks/{task_id}/execution", response_model=list)
async def get_task_executions(task_id: str):
    """获取任务执行记录"""
    # TODO: 从数据库获取执行记录
    return []


@app.post("/api/browser/navigate")
async def navigate_to_url(url: str):
    """导航到指定 URL"""
    try:
        async with get_browser() as browser:
            result_url = browser.navigate(url)
            logger.info(f"导航到: {result_url}")
            return {
                "success": True,
                "current_url": result_url
            }
    except Exception as e:
        logger.error(f"导航失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/browser/screenshot")
async def take_screenshot(path: str = None):
    """截取屏幕"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = path or f"screenshot_{timestamp}.png"
        
        async with get_browser() as browser:
            browser.screenshot(screenshot_path)
            logger.info(f"截图已保存: {screenshot_path}")
            return {
                "success": True,
                "screenshot_path": screenshot_path
            }
    except Exception as e:
        logger.error(f"截图失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/execute")
async def execute_agent_direct(user_input: str):
    """直接执行 Agent 任务"""
    try:
        result = execute_agent_task(user_input)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        logger.error(f"Agent 执行失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def execute_background_task(task: Task):
    """后台执行任务（不阻塞响应）"""
    try:
        # 更新任务状态为进行中
        task.status = TaskStatus.RUNNING
        
        # 执行 Agent
        result = execute_agent_task(task.user_input)
        
        # 更新任务状态
        if "error" in result:
            task.status = TaskStatus.FAILED
        else:
            task.status = TaskStatus.COMPLETED
        
        # 保存执行记录
        execution = Execution(
            task_id=task.id,
            step="agent_execution",
            input=task.user_input,
            output=result,
            status=ExecutionStatus.SUCCESS if "error" not in result else ExecutionStatus.FAILED,
            timestamp=datetime.now()
        )
        
        logger.info(f"任务 {task.id} 执行完成")
        
    except Exception as e:
        logger.error(f"后台任务执行失败: {str(e)}")
        # 更新任务状态为失败
        task.status = TaskStatus.FAILED
        task.error = str(e)


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "browser-automation",
        "browser": "running" if browser_controller else "stopped"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
