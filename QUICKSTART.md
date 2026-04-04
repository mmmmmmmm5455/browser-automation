# 🚀 5 分钟快速上手指南

## ⚡️ 前置条件（2 分钟）

### 1. 确保 Python 3.10+ 已安装
```bash
python --version
# 应显示：Python 3.10.x
```

### 2. 克隆项目到本地
```bash
cd /path/to/your/projects
git clone https://github.com/your-username/browser-automation.git
cd browser-automation
```

### 3. 创建虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install
```

### 4. 配置 API Key
```bash
cp .env.example .env
nano .env  # 编辑并填入你的 OPENAI_API_KEY
```

---

## 🎮 开始使用（3 分钟）

### 方式 A：一键启动 ⭐ 推荐

```bash
# 一键启动所有服务（后端 + 前端）
./start.sh
```

浏览器会自动打开：http://localhost:8501

---

### 方式 B：手动启动

**终端 1（后端）：**
```bash
python -m app.main
```

**终端 2（前端）：**
```bash
streamlit run frontend/app.py
```

访问：http://localhost:8501

---

## 🎯 快速体验（30 秒）

### 1. 创建简单任务

在 Streamlit UI 上填写：

- **标题：** 测试任务
- **描述：** 测试自动搜索
- **自然语言指令：** 帮我打开百度并搜索"Python 教程"

点击「创建任务」

### 2. 等待执行

AI 会自动：
- ✅ 打开百度
- ✅ 输入搜索词
- ✅ 点击搜索按钮
- ✅ 提取搜索结果

### 3. 查看结果

你会看到：
- 📊 执行步骤
- 📝 最终结果
- 📸 截图（如果配置了）

---

## 📚 更多示例

### 示例 1：搜索教程
```
指令：帮我打开 Google 并搜索 "Python 机器学习教程"
```

### 示例 2：自动填写表单
```
指令：帮我打开 example.com 并填写表单：姓名=张三，邮箱=test@example.com，电话=13800000000
```

### 示例 3：提取数据
```
指令：访问 https://news.ycombinator.com，提取前 10 条新闻的标题和链接
```

### 示例 4：自动化测试
```
指令：测试登录功能：访问 https://example.com/login，输入 test@example.com/password123，点击登录，验证跳转到首页
```

---

## 💡 常用命令

### 启动/停止
```bash
# 启动
./start.sh

# 或手动启动
python -m app.main

# 停止
Ctrl+C
```

### 重新安装依赖
```bash
pip install -r requirements.txt
playwright install --force
```

### 查看日志
```bash
tail -f logs/browsers.log
```

### 运行测试
```bash
pytest tests/test_browser.py
```

---

## 🔧 配置调整

### 更换 LLM 模型

编辑 `.env` 文件：
```bash
# 使用 Claude（推荐）
LLM_MODEL=claude-3.5-sonnet

# 或使用 GPT-4o-mini（更快更便宜）
LLM_MODEL=gpt-4o-mini
```

### 切换到有头模式

编辑 `.env` 文件：
```bash
# 改为有头模式（可以看到浏览器窗口）
BROWSER_HEADLESS=false
```

### 调整超时时间

编辑 `.env` 文件：
```bash
# 增加页面加载超时
BROWSER_TIMEOUT=60  # 60 秒
```

---

## 🎨 自定义

### 添加自定义工具

编辑 `app/api/agent.py`，在 `tools` 列表中添加：

```python
Tool(
    name="scroll_down",
    func=browser_tool.scroll_down,
    description="向下滚动页面，使用方法：scroll_down(像素=300)"
),
Tool(
    name="wait_for_element",
    func=browser_tool.wait_for_element,
    description="等待元素出现，使用方法：wait_for_element(selector='#submit-button', timeout=5000)",
),
```

### 添加自定义页面

在 `frontend/pages/` 目录下创建新的 `.py` 文件：

```python
def show():
    st.set_page_config(...)
    st.title("我的自定义页面")
    # 你的代码
```

在 `frontend/app.py` 的导航列表中添加：
```python
page = st.radio(
    "导航",
    ["🏠️ 首页", "🎯 创建任务", "📋 任务列表", "📊 执行详情", "我的页面"]
)
```

---

## 🤝 需要帮助？

### 常见问题

**Q: 浏览器启动失败**
```bash
playwright install --force
```

**Q: 连接不上后端**
```bash
# 检查端口占用
lsof -i:8000
# 检查服务状态
curl http://localhost:8000/api/health
```

**Q: API 调用失败**
```
# 检查 API Key
grep OPENAI_API_KEY .env
# 测试网络
curl https://api.openai.com/v1/models
```

### 获取支持

- 📖 [README](README.md)
- 📚 [文档中心](DEPLOYMENT.md)
- 📝 [快速上手](GETTING_STARTED.md)
- 🐛 [提交 Issue](https://github.com/your-username/browser-automation/issues)

---

**准备好开始了！** 🚀

**试试看：输入一个任务，AI 帮你自动完成！** 🐉
