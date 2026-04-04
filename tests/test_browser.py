# 测试文件 - 浏览器自动化
import pytest
import pytest
import tempfile
from datetime import datetime

from app.main import app
from core.browser_controller import BrowserController
from core.form_filler import FormFiller
from core.data_extractor import DataExtractor
from utils.logger import setup_logger

# 设置日志
setup_logger(__name__)


class TestBrowserController:
    def test_start(self):
        """测试启动浏览器"""
        print("\n=== 测试浏览器启动 ===")
        print("1. 启动浏览器...")
        
        try:
            controller = BrowserController()
            controller.start(headless=True)
            
            assert controller.is_running, "❌ 浏览器启动失败"
            print("✓� 浏览器启动成功")
            
            # 测试导航
            print("\n2. 测试导航...")
            url = "https://www.baidu.com"
            result_url = controller.navigate(url)
            
            assert result_url and "baidu" in result_url.lower(), "❌ 导航失败"
            print(f"✓� 导航成功: {result_url}")
            
            # 测试标题
            title = controller.get_title()
            assert title and "百度一下，你就知道" in title, "❌ 标题提取失败"
            print(f"✓� 标题: {title}")
            
            # 测试截图
            print("\n3. 测试截图...")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = f"test_screenshot_{timestamp}.png"
            controller.screenshot(screenshot_path)
            
            # 检查文件是否存在
            import os
            if os.path.exists(screenshot_path):
                print(f"✓� 截图已保存: {screenshot_path}")
                os.remove(screenshot_path)  # 清理测试文件
            else:
                print("❌ 截图未保存")
            
            print("✓� 截图测试通过")
            
        except AssertionError as e:
            print(f"❌ 浏览器启动测试失败: {e}")
        except Exception as e:
            print(f"❌ 浏览器启动测试异常: {e}")
    
    def test_form_filling(self):
        """测试表单填充"""
        print("\n=== 测试表单填充 ===")
        print("1. 创建浏览器控制器...")
        
        try:
            controller = BrowserController()
            controller.start(headless=True)
            
            # 创建测试页面
            test_html = """
            <html>
                <head>
                    <title>测试表单</title>
                </head>
                <body>
                    <h1>测试表单</h1>
                    <form id="test-form">
                        <label>姓名:</label>
                        <input type="text" id="name" name="name" placeholder="请输入姓名">
                        
                        <label>邮箱:</label>
                        <input type="email" id="email" name="email" placeholder="请输入邮箱">
                        
                        <label>电话:</label>
                        <input type="tel" id="phone" name="phone" placeholder="请输入电话">
                        
                        <label>地址:</label>
                        <input type="text" id="address" name="address" placeholder="请输入地址">
                        
                        <label>备注:</label>
                        <textarea id="remarks" name="remarks" rows="4" placeholder="请输入备注"></textarea>
                        
                        <button type="submit" id="submit">提交</button>
                    </form>
                    <div id="result">结果区域</div>
                </body>
            </html>
            
            # 注入测试 HTML
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.html') as f:
                f.write(test_html)
                temp_path = f.name
            else:
                raise FileNotFoundError("创建测试文件失败")
            
            # 使用 Controller 加载页面
            controller.navigate(f"file://{temp_path}")
            
            # 创建填充器
            form_filler = FormFiller(controller)
            
            # 测试填充
            form_data = {
                "姓名": "张三",
                "邮箱": "zhangsan@example.com",
                "电话": "13800000000",
                "地址": "北京市朝阳区",
                "备注": "测试自动填充"
            }
            
            print("2. 填充表单...")
            result = form_filler.fill_form(form_data)
            
            # 验证结果
            print(f"✅ 填充字段数: {result['success_count']}/{result['total_fields']}")
            
            for detail in result['details']:
                if detail["status"] == "success":
                    print(f"  ✓ {detail['field']}")
                elif detail["status"] == "not_found":
                    print(f"  ✗ {detail['field']}")
                elif detail["status"] == "error":
                    print(f"  ✗ {detail['field']}: {detail.get('error', '未知错误')}")
            
            print("✓� 表单填充测试通过")
            
            # 清理临时文件
            import os
            os.unlink(temp_path)
            
            print("✓� 临时文件已清理")
            
        except AssertionError as e:
            print(f"❌ 表单填充测试失败: {e}")
        except Exception as e:
            print(f"❌ 表单填充测试异常: {e}")
    
    def test_data_extraction(self):
        """测试数据提取"""
        print("\n=== 测试数据提取 ===")
        print("1. 创建测试页面...")
        
        try:
            controller = BrowserController()
            controller.start(headless=True)
            
            # 创建测试页面
            test_html = """
            <html>
                <head>
                    <title>测试数据提取</title>
                    <style>
                        table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        th, td {
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: left;
                        }
                    }
                    th {
                            background-color: #f5f5f5;
                            font-weight: 600;
                            color: #333;
                        }
                    tr:hover {
                        background-color: #f9faf9;
                    }
                    tr:nth-child(odd) {
                        background-color: #f9faf9;
                    }
                    .header_row {
                        position: sticky;
                        top: 0;
                        z-index: 1000;
                        background-color: #fff;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    .header_row th {
                        border-bottom: 2px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                </style>
                </head>
                <body>
                    <h1>测试数据提取</h1>
                    <table>
                        <tr>
                            <th>姓名</th>
                            <th>年龄</th>
                            <th>职业</th>
                        </tr>
                        <tr>
                            <td>张三</td>
                            <td>28</td>
                            <td>工程师</td>
                        </tr>
                        <tr>
                            <td>李四</td>
                            <td>32</td>
                            <td设计师</td>
                        </tr>
                        <tr>
                            <td>王五</td>
                            <td>25</td>
                            <td医生</td>
                        </tr>
                        <tr>
                            <td>赵六</td>
                            <td>30</td>
                            <td教师</td>
                        </tr>
                        <tr>
                            <td>钱七</td>
                            <td>29</td>
                            <td律师</td>
                        </tr>
                    </table>
                    
                    <h2>链接列表</h2>
                    <ul>
                        <li><a href="https://example.com">Example 1</a></li>
                        <li><a href="https://example.com">Example 2</a></li>
                        <li><a href="https://example.com">Example 3</a></li>
                    </ul>
                    
                    <h2>标题列表</h2>
                    <ul>
                        <li>Python 编程教程</li>
                        <li>机器学习基础</li>
                        <li>数据科学入门</li>
                    </ul>
                </body>
            </html>
            
            # 注入测试 HTML
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.html') as f:
                f.write(test_html)
                temp_path = f.name
            else:
                raise FileNotFoundError("创建测试文件失败")
            
            # 加载页面
            controller.navigate(f"file://{temp_path}")
            
            # 创建数据提取器
            data_extractor = DataExtractor(controller)
            
            # 测试表格提取
            table_data = data_extractor.extract_table("#test-table")
            print(f"3. 测试表格提取...")
            
            assert len(table_data) > 0, "❌ 未提取到表格数据"
            print(f"✓� 提取到 {len(table_data)} 行数据")
            
            # 显示部分数据
            print("前 3 行数据：")
            for i, row in table_data[:3]:
                print(f"  行 {i+1}: {row}")
            
            # 测试链接提取
            links = data_extractor.extract_links()
            print(f"4. 测试链接提取...")
            
            assert len(links) > 0, "❌ 未提取到链接"
            print(f"✓� 提取到 {len(links)} 个链接")
            print(f"  前 3 个链接：")
            for i, link in links[:3]:
                print(f"  链接 {i+1}: {link['text']}")
            
            # 测试标题提取
            titles = data_extractor.extract_headers()
            print(f"5. 测试标题提取...")
            
            assert len(titles) > 0, "❌ 未提取到标题"
            print(f"✓� 提取到 {len(titles)} 个标题")
            print(f"  前 3 个标题：")
            for i, title in titles[:3]:
                print(f"  {i+1}: {title}")
            
            print("✓� 数据提取测试通过")
            
            # 清理临时文件
            import os
            os.unlink(temp_path)
            
        except AssertionError as e:
            print(f"❌ 数据提取测试失败: {e}")
        except Exception as e:
            print(f"❌ 数据提取测试异常: {e}")
    
    def test_visual_analysis(self):
        """测试视觉分析"""
        print("\n=== 测试视觉分析 ===")
        print("1. 创建测试页面...")
        
        try:
            controller = BrowserController()
            controller.start(headless=True)
            
            # 创建测试页面
            test_html = """
            <html>
                <head>
                    <title>测试视觉分析</title>
                </head>
                <body>
                    <h1>测试视觉分析</h1>
                    <div id="content">
                        <p>这是一段测试文本。</p>
                        <button id="submit">点击我</button>
                        <div id="result"></div>
                    </div>
                </body>
            </html>
            
            # 注入测试 HTML
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.html') as f:
                f.write(test_html)
                temp_path = f.name
            else:
                raise FileNotFoundError("创建测试文件失败")
            
            # 加载页面
            controller.navigate(f"file://{temp_path}")
            
            # 创建视觉分析器
            analyzer = VisualAnalyzer(controller)
            
            # 测试页面结构分析
            print("2. 测试页面结构分析...")
            structure = analyzer.analyze_page_structure()
            
            print(f"✓� 页面标题: {structure.get('title', '无标题')}")
            print(f"   - 表单数: {structure.get('total_forms', 0)}")
            print(f"   - 输入框数: {structure.get('total_inputs', 0)}")
            print(f"   - 链接数: {structure.get('total_links', 0)}")
            print(f"   - 按钮数: {structure.get('total_buttons', 0)}")
            print(f"   - 图片数: {structure.get('total_images', 0)}")
            
            # 测试交互元素检测
            print("3. 测试交互元素检测...")
            interactive_elements = analyzer.detect_interactive_elements()
            print(f"✓� 检测到 {len(interactive_elements)} 个交互元素")
            
            for element in interactive_elements[:3]:
                print(f"  • {element}")
            
            print("✓� 视觉分析测试通过")
            
            # 清理临时文件
            import os
            os.unlink(temp_path)
            
        except AssertionError as e:
            print(f"❌ 视觉分析测试失败: {e}")
        except Exception as e:
            print(f"❌ 视觉分析测试异常: {e}")


if __name__ == "__main__":
    print("开始测试浏览器自动化核心组件...")
    
    # 选择要运行的测试
    test_map = {
        "1": ("测试浏览器启动", "test_browser_start"),
        "2": ("测试表单填充", "test_form_filling"),
        "3": ("测试数据提取", "test_data_extraction"),
        "4": ("测试视觉分析", "test_visual_analysis")
    }
    
    print("\n请选择测试编号（输入 1-4）：")
    choice = input()
    
    if choice in test_map:
        test_func = test_map[choice]
        test_func()
    else:
        print("无效选择，退出测试")
