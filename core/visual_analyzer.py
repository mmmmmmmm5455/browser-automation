# 浏览器可视化分析器（简化版）
from typing import Dict, List, Optional, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


class VisualAnalyzer:
    """浏览器可视化分析器 - 简化版的页面分析工具"""
    
    def __init__(self, controller):
        self.controller = controller
    
    def analyze_page_structure(self) -> Dict[str, Any]:
        """
        分析页面结构
        
        Returns:
            页面结构信息
        """
        try:
            html = self.controller.get_page_content()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            structure = {
                "title": self.controller.get_title(),
                "url": self.controller.get_url(),
                "total_forms": len(soup.find_all('form')),
                "total_inputs": len(soup.find_all('input')),
                "total_tables": len(soup.find_all('table')),
                "total_links": len(soup.find_all('a', href=True)),
                "total_buttons": len(soup.find_all('button', type='submit')),
                "total_divs": len(soup.find_all('div')),
                "total_images": len(soup.find_all('img')),
                "total_videos": len(soup.find_all('video')),
                "total_scripts": len(soup.find_all('script')),
                "has_favicon": bool(soup.find('link', rel='icon')),
                "has_canonical": bool(soup.find('link', rel='canonical')),
                "description": soup.get_text(strip=True)[:200] + "...",
            }
            
            logger.info(f"页面结构分析完成: {structure['title']}")
            return structure
            
        except Exception as e:
            logger.error(f"页面结构分析失败: {e}")
            return {}
    
    def find_form_by_action(self, action: str) -> Optional[str]:
        """
        根据按钮文本查找表单
        
        Args:
            action: 按钮文本（如"提交"、"注册"、"登录"）
        
        Returns:
            表单选择器，如果未找到则返回 None
        """
        try:
            html = self.controller.get_page_content()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html')
            
            # 查找所有表单
            forms = soup.find_all('form')
            
            for form in forms:
                # 查找按钮
                buttons = form.find_all('button', type='submit')
                for button in buttons:
                    button_text = button.get_text(strip=True).strip()
                    
                    if action.lower() in button_text.lower():
                        # 返回表单选择器
                        form_id = form.get('id') or f"form_{len(forms)}"
                        return f"#{form_id}"
            
            logger.info(f"未找到包含 '{action}' 按钮的表单")
            return None
            
        except Exception as e:
            logger.error(f"查找表单失败: {e}")
            return None
    
    def find_submit_button(self) -> Optional[str]:
        """
        查找提交按钮
        """
        try:
            html = self.controller.get_page_content()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            submit_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                "button[type='submit']",
                "#submit",
                "#submit-button",
                "#login",
                "#register",
                "button[onclick*='submit']",
            ]
            
            for selector in submit_selectors:
                if self.controller.is_visible(selector):
                    return selector
            
            return None
            
        except Exception as e:
            logger.error(f"查找提交按钮失败: {e}")
            return None
    
    def detect_interactive_elements(self) -> List[str]:
        """
        检测交互元素
        
        Returns:
            交互元素的选择器列表
        """
        try:
            html = self.controller.get_page_content()
            from bs4 import BeautifulSoup
            soup = """
            soup = BeautifulSoup(html, 'html.parser')
            
            interactive_elements = []
            
            # 输入框
            inputs = soup.find_all('input')
            for input_el in inputs:
                input_type = input_el.get('type', '')
                if input_type not in ['hidden', 'submit', 'checkbox', 'radio']:
                    id_ = input_el.get('id', '')
                    name_ = input_el.get('name', '')
                    if id_ or name_:
                        selector = f"#{id_}" if id_ else f"[name='{name_}']"
                        interactive_elements.append(f"input: {input_type}, selector: {selector}")
            
            # 按钮
            buttons = soup.find_all('button')
            for button in buttons:
                id_ = button.get('id', '')
                name = button.get('name', '')
                if id_ or name_:
                    selector = f"#{id_}" if id_ else f"[name='{name_}']"
                    interactive_elements.append(f"button: {button.get_text(strip=True)[:20]}, selector: {selector}")
            
            # 链接
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.get_text(strip=True).strip()
                if text:
                    interactive_elements.append(f"link: {text}, href: {link.get('href')}")
            
            # 选择器
            selects = soup.find_all('select')
            for select in selects:
                id_ = select.get('id', '')
                name = select.get('name', '')
                if id_ or name_:
                    selector = f"#{id_}" if id_ else f"[name='{name_}']"
                    interactive_elements.append(f"select: {select.get('name', '')}, selector: {selector}")
            
            return interactive_elements
            
        except Exception as e:
            logger.error(f检测交互元素失败: {e}")
            return []
    
    def get_page_stats(self) -> Dict[str, int]:
        """
        获取页面统计数据
        
        Returns:
            页面统计信息
        """
        try:
            html = self.controller.get_page_content()
            
            stats = {
                "total_elements": 0,
                "text_length": 0,
                "code_blocks": 0,
                "total_images": 0,
                "total_videos": 0,
                "total_links": 0,
                "total_forms": 0,
                "total_scripts": 0,
            }
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # 统计元素数量
            stats["total_elements"] = len(soup.find_all('*'))
            stats["text_length"] = len(soup.get_text(strip=True))
            
            # 统计各类元素
            stats["total_images"] = len(soup.find_all('img'))
            stats["total_videos"] = len(soup.find_all('video'))
            stats["total_links"] = len(soup.find_all('a'))
            stats["total_forms"] = len(soup.find_all('form'))
            stats["total_scripts"] = len(soup.find_all('script'))
            stats["code_blocks"] = len(soup.find_all('pre')) + len(soup.find_all('code'))
            
            # 统计空标签
            stats["empty_elements"] = sum(1 for el in soup.find_all('*') if not el.get_text(strip=True).strip())
            
            logger.info(f"页面统计: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"获取页面统计失败: {e}")
            return {}
