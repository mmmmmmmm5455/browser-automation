# 浏览器控制器（使用 Playwright）
from playwright.sync_api import sync_playwright
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowserController:
    """浏览器控制器 - 封装 Playwright 操作"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.is_running = False
    
    def start(self, headless: bool = False):
        """启动浏览器"""
        if self.is_running:
            logger.warning("浏览器已经在运行")
            return
        
        logger.info(f"启动浏览器 (headless={headless})")
        
        try:
            self.playwright = sync_playwright()
            self.browser = self.playwright.chromium.launch(headless=headless)
            self.page = self.browser.new_page()
            self.is_running = True
            logger.info("✅ 浏览器启动成功")
            
        except Exception as e:
            logger.error(f"启动浏览器失败: {str(e)}")
            raise
    
    def stop(self):
        """停止浏览器"""
        if not self.is_running:
            return
        
        logger.info("停止浏览器")
        
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            self.is_running = False
            logger.info("✅ 浏览器已关闭")
            
        except Exception as e:
            logger.error(f"停止浏览器失败: {str(e)}")
    
    def restart(self):
        """重启浏览器"""
        self.stop()
        self.start()
    
    def navigate(self, url: str, timeout: int = 30000):
        """导航到 URL"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        logger.info(f"导航到: {url}")
        self.page.goto(url, timeout=timeout)
        
        # 等待页面加载完成
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            pass  # 页面可能有 JS 错误，继续
        
        return self.page.url()
    
    def click(self, selector: str, timeout: int = 5000):
        """点击元素"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        logger.info(f"点击元素: {selector}")
        self.page.click(selector, timeout=timeout)
    
    def fill(self, selector: str, text: str, timeout: int = 5000):
        """填充输入框"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        logger.info(f"填充输入框: {selector} = {text}")
        self.page.fill(selector, text, timeout=timeout)
    
    def select(self, selector: str, value: str):
        """选择下拉框"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        logger.info(f"选择下拉框: {selector} = {value}")
        self.page.select_option(selector, value)
    
    def get_text(self, selector: str) -> str:
        """获取元素的文本"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        return self.page.locator(selector).inner_text()
    
    def get_inner_html(self, selector: str) -> str:
        """获取元素的内部 HTML"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        return self.page.locator(selector).inner_html()
    
    def get_page_content(self) -> str:
        """获取页面完整内容"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        return self.page.content()
    
    def screenshot(self, path: str, full_page: bool = False):
        """截图"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        logger.info(f"截图保存到: {path}")
        self.page.screenshot(path=path, full_page=full_page)
    
    def scroll(self, direction: str = "down", pixels: int = 300):
        """滚动页面"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        if direction == "down":
            self.page.evaluate(f"window.scrollBy(0, {pixels})")
        elif direction == "up":
            self.page.evaluate(f"window.scrollBy(0, -{pixels})")
        
        logger.info(f"页面滚动: {direction} {pixels}px")
    
    def wait_for_element(self, selector: str, timeout: int = 5000):
        """等待元素出现"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        logger.info(f"等待元素: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        if not self.is_running:
            return False
        
        return self.page.is_visible(selector)
    
    def get_title(self) -> str:
        """获取页面标题"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        return self.page.title()
    
    def get_url(self) -> str:
        """获取当前 URL"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        return self.page.url
    
    @property
    def page(self):
        """获取 Playwright Page 对象"""
        if not self.is_running:
            raise Exception("浏览器未启动")
        
        return self.page
    
    def __enter__(self):
        """支持 with 上下文管理器"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭"""
        self.stop()
