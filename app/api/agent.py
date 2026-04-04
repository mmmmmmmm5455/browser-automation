# 浏览器 Agent
from langchain.agents import Agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

from core.browser_controller import BrowserController
from core.form_filler import FormFiller
from core.data_extractor import DataExtractor
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowserTool:
    """浏览器工具类"""
    
    def __init__(self, controller: BrowserController):
        self.controller = controller
        self.form_filler = FormFiller(controller)
        self.data_extractor = DataExtractor(controller)
    
    def navigate_to_url(self, url: str) -> str:
        """导航到 URL"""
        result_url = self.controller.navigate(url)
        return f"已导航到 {result_url}"
    
    def click_element(self, selector: str) -> str:
        """点击元素"""
        self.controller.click(selector)
        return f"已点击 {selector}"
    
    def fill_input(self, selector: str, text: str) -> str:
        """填充输入框"""
        self.controller.fill(selector, text)
        return f"已填写 {selector}"
    
    def get_page_text(self, selector: str = None) -> str:
        """获取页面文本"""
        if selector:
            return self.controller.get_text(selector)
        else:
            return self.controller.page.content()
    
    def extract_table_data(self, selector: str) -> list:
        """提取表格数据"""
        return self.data_extractor.extract_table(selector)
    
    def extract_all_links(self) -> list:
        """提取所有链接"""
        return self.data_extractor.extract_links()
    
    def screenshot(self, path: str = None) -> str:
        """截图"""
        timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = path or f"screenshot_{timestamp}.png"
        self.controller.screenshot(screenshot_path)
        return f"截图已保存: {screenshot_path}"


def create_browser_agent(controller: BrowserController, llm_model: str = "gpt-4o"):
    """创建浏览器 Agent"""
    # 创建浏览器工具
    browser_tool = BrowserTool(controller)
    
    # 定义工具列表
    tools = [
        Tool(
            name="navigate",
            func=browser_tool.navigate_to_url,
            description="导航到指定的 URL。使用方法：navigate(url='https://example.com')"
        ),
        Tool(
            name="click_element",
            func=browser_tool.click_element,
            description="点击页面上的元素。使用方法：click_element(selector='#submit-button')"
        ),
        Tool(
            name="fill_input",
            func=browser_tool.fill_input,
            description="填充表单输入框。使用方法：fill_input(selector='#name', text='张三')"
        ),
        Tool(
            name="get_page_text",
            func=browser_tool.get_page_text,
            description="获取页面上的文本内容。使用方法：get_page_text(selector='#content')"
        ),
        Tool(
            name="extract_table",
            func=browser_tool.extract_table_data,
            description="提取表格数据。使用方法：extract_table(selector='#data-table')"
        ),
        Tool(
            name="extract_links",
            func=browser_tool.extract_all_links,
            description="提取页面所有链接。使用方法：extract_links()"
        ),
        Tool(
            name="screenshot",
            func=browser_tool.screenshot,
            description="截图保存。使用方法：screenshot(path='screenshot.png')"
        ),
    ]
    
    # 创建 LLM
    llm = ChatOpenAI(model=llm_model, temperature=0)
    
    # 创建 Agent
    agent = Agent(
        llm=llm,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return agent


def execute_agent_task(user_input: str) -> dict:
    """执行 Agent 任务"""
    global browser_controller
    
    try:
        if browser_controller is None:
            raise Exception("浏览器未启动")
        
        logger.info(f"执行 Agent 任务: {user_input}")
        
        # 创建 Agent
        agent = create_browser_agent(browser_controller)
        
        # 执行任务
        result = agent.invoke(user_input)
        
        logger.info(f"Agent 执行结果: {result}")
        
        return {
            "success": True,
            "output": result["output"],
            "agent_type": "browser_agent",
            "input": user_input
        }
        
    except Exception as e:
        logger.error(f"Agent 执行失败: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "input": user_input
        }
