# 数据提取器 - 从网页提取数据
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


class DataExtractor:
    """数据提取器 - 从网页提取各种数据"""
    
    def __init__(self, controller):
        self.controller = controller
    
    def extract_table(self, selector: str) -> List[List[str]]:
        """
        提取表格数据
        
        Args:
            selector: 表格的选择器
        
        Returns:
            表格数据的列表（每行是一个列表）
        """
        try:
            table_html = self.controller.get_inner_html(selector)
            soup = BeautifulSoup(table_html, 'html.parser')
            
            # 查找表格
            table = soup.find('table')
            if not table:
                logger.warning(f"未找到表格: {selector}")
                return []
            
            # 提取行数据
            rows = table.find_all('tr')
            table_data = []
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                if any(row_data):  # 跳过空行
                    table_data.append(row_data)
            
            logger.info(f"提取表格成功: {len(table_data)} 行")
            return table_data
            
        except Exception as e:
            logger.error(f"提取表格失败: {e}")
            return []
    
    def extract_table_as_dataframe(self, selector: str, headers: List[str] = None) -> pd.DataFrame:
        """
        提取表格数据并转换为 DataFrame
        
        Args:
            selector: 表格的选择器
            headers: 列名（可选）
        
        Returns:
            DataFrame
        """
        try:
            table_data = self.extract_table(selector)
            
            # 添加列名
            if headers and len(table_data) > 0:
                if len(table_data[0]) != len(headers):
                    logger.warning(f"表头数量 ({len(headers)}) 与表格列数 ({len(table_data[0])}) 不匹配")
                    headers = headers[:len(table_data[0])]
            
                df = pd.DataFrame(table_data, columns=headers)
            else:
                df = pd.DataFrame(table_data)
            
            logger.info(f"提取表格为 DataFrame: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"提取 DataFrame 失败: {e}")
            return pd.DataFrame()
    
    def extract_links(self, selector: str = None, **filters: Dict = None) -> List[Dict[str, str]]:
        """
        提取所有链接
        
        Args:
            selector: 可选，限定查找范围
            filters: 过滤条件
                {
                    "domain": "域名过滤",
                    "text": "文本过滤"
                }
        
        Returns:
            链接列表
        """
        try:
            # 获取 HTML
            if selector:
                html = self.controller.get_inner_html(selector)
            else:
                html = self.controller.get_page_content()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找所有链接
            all_links = soup.find_all('a', href=True)
            
            links = []
            seen_urls = set()
            
            for a in all_links:
                url = a.get('href', '')
                text = a.get_text(strip=True).strip()
                
                # 过滤空链接
                if not url:
                    continue
                
                # URL 验证
                if url.startswith('#'):  # 锚点链接
                    continue
                
                # 过滤域名
                if filters and "domain" in filters:
                    if filters["domain"]:
                        domain = filters["domain"]
                        if not (domain.replace("https://", "").startswith(url.replace("https://", "").split('/')[2])):
                            continue
                
                # 过滤文本
                if filters and "text" in filters:
                    if filters["text"]:
                        text_filter = filters["text"].lower()
                        if text_filter not in text.lower():
                            continue
                
                # 去重
                if url in seen_urls:
                    continue
                
                seen_urls.add(url)
                links.append({
                    "text": text,
                    "url": url,
                    "target": "_blank" if a.get('target') == "_blank" else "_self"
                })
            
            logger.info(f"提取到 {len(links)} 个链接")
            return links
            
        except Exception as e:
            logger.error(f"提取链接失败: {e}")
            return []
    
    def extract_images(self, selector: str = None) -> List[Dict[str, str]]:
        """
        提取图片信息
        
        Args:
            selector: 可选，限定查找范围
        
        Returns:
            图片信息列表
        """
        try:
            if selector:
                html = self.controller.get_inner_html(selector)
            else:
                html = logger.get_page_content()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            images = []
            img_elements = soup.find_all('img')
            
            for img in img_elements:
                src = img.get('src', '')
                alt = img.get('alt', '')
                title = img.get('title', '')
                
                if src:
                    # 跳过空 src 或 base64 图片
                    if not src or src.startswith('data:image'):
                        continue
                    
                    images.append({
                        "url": src,
                        "alt": alt,
                        "title": title
                    })
            
            logger.info(f"提取到 {len(images)} 张图片")
            return images
            
        except Exception as e:
            logger.error(f"提取图片失败: {e}")
            return []
    
    def extract_text(self, selector: str = None) -> str:
        """
        提取纯文本
        
        Args:
            selector: 可选，限定查找范围
        
        Returns:
            纯文本内容
        """
        try:
            if selector:
                text = self.controller.get_text(selector)
            else:
                text = self.controller.get_page_content()
            
            # 清理空白行
            lines = [line.strip() for line in text.split('\n')]
            non_empty_lines = [line for line in lines if line]
            
            clean_text = '\n'.join(non_empty_lines)
            
            logger.info(f"提取文本: {len(clean_text)} 字符")
            return clean_text
            
        except Exception as e:
            logger.error(f"提取文本失败: {e}")
            return ""
    
    def extract_headers(self, selector: str) -> List[str]:
        """
        提取所有标题（h1-h6）
        
        Args:
            selector: 可选，限定查找范围
        
        Returns:
            标题列表
        """
        try:
            if selector:
                html = self.controller.get_inner_html(selector)
            else:
                html = self.controller.get_page_content()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找所有标题
            headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            titles = [h.get_text(strip=True).strip() for h in headers if h.get_text(strip=True).strip()]
            
            logger.info(f"提取到 {len(titles)} 个标题")
            return titles
            
        except Exception as e:
            logger.error(f"提取标题失败: {e}")
            return []
    
    def extract_metadata(self) -> Dict[str, Any]:
        """
        提取页面元数据
        
        Returns:
            元数据字典
        """
        try:
            title = self.controller.get_title()
            url = self.controller.get_url()
            
            # 获取页面语言
            html = self.controller.get_page_content()
            lang = "unknown"
            
            if '<html' in html.lower():
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                html_tag = soup.find('html')
                if html_tag:
                    lang = html_tag.get('lang', '')
            
            # 获取元信息
            meta = {
                "title": title,
                "url": url,
                "language": lang,
                "total_links": len(self.extract_links()),
                "total_images": len(self.extract_images()),
                "has_table": bool(self.extract_table()),
                "word_count": len(self.extract_text().split())
            }
            
            logger.info(f"页面元数据: {meta}")
            return meta
            
        except Exception as e:
            logger.error(f"提取元数据失败: {e}")
            return {}
    
    def extract_structured_data(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据结构化数据 schema 提取数据
        
        Args:
            schema: 数据模式
                {
                    "field_name": {
                        "type": "text"|"number"|"email"|"link"|"image",
                        "selector": "css selector",
                        "required": bool
                    }
                }
        
        Returns:
            提取的数据
        """
        data = {}
        
        for field_name, field_config in schema.items():
            field_type = field_config.get("type")
            selector = field_config.get("selector")
            required = field_config.get("required", False)
            
            try:
                if field_type == "text":
                    value = self.extract_text(selector)
                elif field_type == "number":
                    value = self._extract_number(selector)
                elif field_type == "email":
                    value = self._extract_email(selector)
                elif field_type == "link":
                    links = self.extract_links(selector)
                    value = links[0]["url"] if links else ""
                elif field_type == "image":
                    images = self.extract_images(selector)
                    value = images[0]["url"] if images else ""
                else:
                    value = ""
                
                if required and not value:
                    data[field_name] = None
                    logger.warning(f"必填字段 {field_name} 未提取到值")
                else:
                    data[field_name] = value
                    
            except Exception as e:
                logger.error(f"提取字段 {field_name} 失败: {e}")
                data[field_name] = None
        
        return data
    
    def _extract_number(self, selector: str) -> Optional[float]:
        """
        提取数字
        """
        try:
            text = self.extract_text(selector)
            import re
            
            # 查找数字（包括小数点）
            matches = re.findall(r'[-+]?\d+\.?\d*', text)
            if matches:
                return float(matches[0])
            return None
            
        except:
            return None
    
    def _extract_email(self, selector: str) -> Optional[str]:
        """
        提取邮箱
        """
        try:
            text = self.extract_text(selector)
            import re
            
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
            if emails:
                return emails[0]
            return None
            
        except:
            return None
    
    def export_to_csv(self, data: List[List[str]], filename: str) -> str:
        """
        导出数据到 CSV
        
        Args:
            data: 二维数据
            filename: 文件名
        
        Returns:
            保存的文件路径
        """
        try:
            df = pd.DataFrame(data)
            filepath = f"data/{filename}"
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info(f"数据已导出到: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"导出 CSV 失败: {e}")
            return ""
    
    def export_to_json(self, data: Any, filename: str) -> str:
        """
        导出数据到 JSON
        
        Args:
            data: 数据对象
            filename: 文件名
        
        Returns:
            保存的文件路径
        """
        try:
            filepath = f"data/{filename}"
            
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"数据已导出到: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"导出 JSON 失败: {e}")
            return ""
    
    def export_to_excel(self, data: List[List[str]], filename: str) -> str:
        """
        导出数据到 Excel
        
        Args:
            data: 二维数据
            filename: 文件名
        
        Returns:
            保存的文件路径
        """
        try:
            df = pd.DataFrame(data)
            filepath = f"data/{filename}"
            df.to_excel(filepath, index=False, engine='openpyxl')
            
            logger.info(f"数据已导出到: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"导出 Excel 失败: {e}")
            return ""
