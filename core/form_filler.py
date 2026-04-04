# 表单填充器 - 智能填充表单
from typing import Dict, Any, List, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class FormFiller:
    """智能表单填充器 - AI 辅助的表单填充工具"""
    
    def __init__(self, controller):
        self.controller = controller
    
    def fill_form(self, form_data: Dict[str, Any], auto_submit: bool = False) -> Dict[str, Any]:
        """
        智能填充表单
        
        Args:
            form_data: 表单数据字典，key 为字段名，value 为值
            auto_submit: 是否自动提交表单
        """
        logger.info(f"开始填充表单，字段数: {len(form_data)}")
        
        results = {
            "total_fields": len(form_data),
            "success_count": 0,
            "failed_count": 0,
            "details": []
        }
        
        # 遍历表单数据
        for field_name, field_value in form_data.items():
            try:
                # 智能查找字段选择器
                selector = self._find_field(field_name)
                
                if selector:
                    # 填充字段
                    self.controller.fill(selector, str(field_value))
                    results["success_count"] += 1
                    results["details"].append({
                        "field": field_name,
                        "selector": selector,
                        "status": "success",
                        "value": field_value
                    })
                    logger.info(f"✓ 填充字段: {field_name}")
                else:
                    # 未找到字段，尝试用 AI 识别
                    results["failed_count"] += 1
                    results["details"].append({
                        "field": field_name,
                        "selector": None,
                        "status": "not_found",
                        "value": field_value
                    })
                    logger.warning(f"✗ 未找到字段: {field_name}")
                    
            except Exception as e:
                results["failed_count"] += 1
                results["details"].append({
                    "field": field_name,
                    "selector": None,
                    "status": "error",
                    "value": field_value,
                    "error": str(e)
                })
                logger.error(f"✗ 填充字段失败: {field_name}, 错误: {e}")
        
        # 自动提交表单
        if auto_submit:
            try:
                self._submit_form()
                results["details"].append({
                    "field": "submit",
                    "selector": "button[type='submit'], input[type='submit']",
                    "status": "success",
                    "value": "自动提交"
                })
                logger.info("✓ 表单已自动提交")
            except Exception as e:
                results["failed_count"] += 1
                results["details"].append({
                    "field": "submit",
                    "selector": None,
                    "status": "error",
                    "value": "提交",
                    "error": str(e)
                })
                logger.error(f"✗ 自动提交失败: {e}")
        
        logger.info(f"表单填充完成: 成功 {results['success_count']}, 失败 {results['failed_count']}")
        return results
    
    def _find_field(self, field_name: str) -> Optional[str]:
        """
        智能查找表单字段选择器
        
        Args:
            field_name: 字段名（如"姓名"、"email"）
        
        Returns:
            选择器字符串，如果未找到则返回 None
        """
        # 构建可能的选择器列表
        selectors = [
            # 按精确匹配优先
            f"input[name='{field_name}']",
            f"input[placeholder*='{field_name}']",
            f"input[id*='{field_name}']",
            f"#{field_name}",
            f".{field_name}",
            # 模糊匹配
            f"input[contains(@placeholder, '{field_name}')]",
            f"input[contains(@id, '{field_name}')]",
            f"input[contains(@name, '{field_name}')]",
            # label 关联
            f"//label[contains(text(), '{field_name}')]/..//input",
            f"//span[contains(text(), '{field_name}')]/..//input",
        ]
        
        # 尝试每个选择器
        for selector in selectors:
            try:
                if self.controller.is_visible(selector):
                    # 验证这是一个输入框
                    element_type = self.controller.page.locator(selector).get_attribute("type")
                    if element_type and "input" in element_type.lower():
                        logger.info(f"找到字段: {field_name} -> {selector}")
                        return selector
            except Exception:
                continue
        
        # 如果没找到，尝试用 AI 分析页面 HTML
        logger.warning(f"未通过常规选择器找到字段: {field_name}")
        return self._ai_find_field(field_name)
    
    def _ai_find_field(self, field_name: str) -> Optional[str]:
        """
        使用 AI 分析页面 HTML，智能匹配字段
        
        Args:
            field_name: 字段名
        Returns:
            选择器字符串，如果未找到则返回 None
        """
        try:
            # 获取页面 HTML
            page_html = self.controller.get_inner_html("body")
            
            # 这里简化处理，实际应该调用 LLM 分析
            # 先返回 None，可以后续集成 LLM
            logger.warning(f"AI 字段识别未实现，字段: {field_name}")
            return None
            
        except Exception as e:
            logger.error(f"AI 字段识别失败: {e}")
            return None
    
    def fill_by_dict(self, selector_value_map: Dict[str, str]) -> Dict[str, str]:
        """
        使用精确的 selector -> value 映射表单
        
        Args:
            selector_value_map: 选择器到值的映射
        """
        results = {}
        
        for selector, value in selector_value_map.items():
            try:
                self.controller.fill(selector, value)
                results[selector] = "success"
                logger.info(f"✓ 填充: {selector}")
            except Exception as e:
                results[selector] = f"error: {e}"
                logger.error(f"✗ 填充失败: {selector}")
        
        return results
    
    def _submit_form(self):
        """提交表单"""
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button[type='submit']"
        ]
        
        for selector in submit_selectors:
            try:
                if self.controller.is_visible(selector):
                    self.controller.click(selector)
                    logger.info(f"点击提交按钮: {selector}")
                    return True
            except Exception:
                continue
        
        logger.warning("未找到提交按钮")
        return False
    
    def extract_form_fields(self) -> List[Dict[str, str]]:
        """
        提取页面上的所有表单字段
        
        Returns:
            字段信息列表
        """
        try:
            # 查找所有 input 元素
            inputs = self.controller.page.query_selector("input")
            
            fields = []
            for i, input_el in enumerate(inputs):
                input_type = input_el.get_attribute("type", "")
                input_name = input_el.get_attribute("name", "")
                input_id = input_el.get_attribute("id", "")
                input_placeholder = input_el.get_attribute("placeholder", "")
                
                # 计算唯一标识符
                identifier = input_name or input_id or f"input_{i}"
                
                fields.append({
                    "index": i,
                    "type": input_type,
                    "name": input_name,
                    "id": input_id,
                    "placeholder": input_placeholder,
                    "selector": f"input[name='{input_name}']" if input_name else f"#{input_id}" if input_id else None,
                    "visible": self.controller.is_visible(f"input[name='{input_name}']" if input_name else f"#{input_id}"),
                    "value": ""  # 当前值
                })
            
            logger.info(f"提取到 {len(fields)} 个表单字段")
            return fields
            
        except Exception as e:
            logger.error(f"提取表单字段失败: {e}")
            return []
    
    def validate_form(self, validation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证表单数据
        
        Args:
            validation_rules: 验证规则
                {
                    "field_name": {
                        "required": bool,
                        "type": "email"/"phone"/"number"/"regex",
                        "pattern": "正则表达式"
                    }
                }
        
        Returns:
            验证结果
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        for field_name, field_config in validation_rules.items():
            field_value = validation_rules.get("form_data", {}).get(field_name)
            
            # 检查必填字段
            if field_config.get("required", False) and not field_value:
                results["valid"] = False
                results["errors"].append(f"{field_name}: 必填项")
            
            # 类型检查
            field_type = field_config.get("type")
            if field_type == "email" and field_value:
                # 邮箱格式验证
                if "@" not in field_value or "." not in field_value.split("@")[0]:
                    results["valid"] = False
                    results["errors"].append(f"{field_name}: 邮箱格式错误")
            
            elif field_type == "phone" and field_value:
                # 手机号格式验证
                digits = "".join(filter(str.isdigit, field_value))
                if len(digits) != 11 or not digits.startswith(("1", "3", "5", "7", "8", "9")):
                    results["      " = False
                    results["errors"].append(f"{field_name}: 手机号格式错误")
            
            elif field_type == "regex" and field_value:
                # 正则表达式验证
                import re
                pattern = field_config.get("pattern", "")
                if pattern and not re.match(pattern, field_value):
                    results["valid"] = False
                    results["errors"].append(f"{field_name}: 格式不匹配")
            
            # 检查正则匹配
            pattern = field_config.get("pattern")
            if pattern:
                import re
                if not re.match(pattern, field_value):
                    results["warnings"].append(f"{field_name}: 不匹配模式: {pattern}")
        
        return results
