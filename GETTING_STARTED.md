# 开始使用指南

## 🎯 第一次使用？

### 第 1 步：安装依赖

```bash
# 进入项目目录
cd browser-automation

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# Windows: venv\Scripts\activate

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 第 2 步：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，填入你的 API Key
nano .env
# 或
vi .env
```

**必须配置项：**
- `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`（至少一个）

### 第 3 步：启动服务

**方式 A：分开启动（开发模式）**

```bash
# 终端 1：启动后端 API
python -m app.main

# 终端 2：启动前端 UI
streamlit run frontend/app.py
```

**方式 B：使用 Docker（生产模式）**

```bash
docker-compose up -d
```

### 第 4 步：开始使用

1. 打开浏览器访问：`http://localhost:8501`
2. 输入你的任务描述
3. 点击「创建任务」
4. 查看 AI 自动执行！

---

## 🎮 快速体验示例

### 示例 1：自动搜索

```
任务标题：搜索 Python 教程
任务描述：在 Google 上查找 Python 教程
自然语言指令：帮我打开 Google 并搜索 'Python 机器学习教程'
```

**执行步骤：**
1. ✓ 导航到 Google
2. ✓ 搜索 Python 机器学习教程
3. ✓ 提取搜索结果
4. ✓ 返回结果摘要

### 示例 2：自动填写表单

```
任务标题：填写注册表单
任务描述：在示例网站上注册账号
自然语言指令：帮我打开 https://example.com/user/register 并填写表单：姓名=测试用户，邮箱=test@example.com，密码=123456
```

**执行步骤：**
1. ✓ 导航到注册页面
2. ✓ 智能识别表单字段
3. ✓ 自动填充所有字段
4. ✓ 验证填充结果
5. ✓ 提交表单

### 示例 3：提取数据

```
任务标题：提取 Hacker News 新闻
任务描述：提取 Hacker News 前的新闻标题和链接
自然语言指令：访问 https://news.ycombinator.com，提取前 10 条新闻的标题和链接
```

**执行步骤：**
1. ✓ 导航到 Hacker News
2. ✓ 识别新闻列表
3. ✓ 提取标题和链接
4. ✓ 导出为 JSON
5. ✓ 返回结构化数据

---

## 🔧 高级功能

### 1. 自定义提示词

你可以修改 AI 的系统提示词，让它更符合你的需求：

```python
# 编辑 agents/browser_agent.py 中的提示词
# 找到 SYSTEM_PROMPT 变量
# 修改其内容即可
```

### 2. 添加新工具

添加新的浏览器操作工具：

```python
# 在 app/api/agent.py 的 tools 列表中添加新工具
tools = [
    Tool(
        name="scroll_down",
        func=browser_tool.scroll_down,
        description="向下滚动页面。使用方法：scroll_down(像素=300)"
    ),
    Tool(
        name="wait_for_element",
        func=browser_tool.wait_for_element,
        description="等待元素出现。使用方法：wait_for_element(selector='#submit-button', timeout=5000)"
    ),
    # 添加更多工具...
]
```

### 3. 自定义数据格式

修改数据提取器的输出格式：

```python
# 修改 core/data_extractor.py 中的提取方法
# 可以添加自定义格式，如 CSV、JSON、XML 等
```

---

## 💡 提高效率的技巧

### 1. 保存常用任务

你可以将常用任务保存为模板，快速重复执行：

```
1. 创建任务
2. 查看任务详情
3. 点击「保存为模板」
4. 下次选择模板快速创建
```

### 2. 批量操作

使用脚本批量执行多个任务：

```python
# examples/batch_tasks.py

tasks = [
    "任务 1",
    "任务 2",
    "任务 3",
]

for task in tasks:
    # 创建并执行任务
    pass
```

### 3. 自动化任务

设置定时任务，定期自动执行：

```python
# 可以结合 crontab 或其他定时工具
```

---

## 📚 更多教程

- [API 文档](DEPLOYMENT.md#api-文档)
- [数据提取指南](DEPLOYMENT.md#数据提取)
- [自定义工具开发](DEPLOYMENT.md#自定义工具)
- [部署到云服务器](DEPLOYMENT.md#docker-部署)

---

**准备好开始了吗？** 🚀

**遇到问题？** 查看 [FAQ](DEPLOYMENT.md#常见问题) 或 [提交 Issue](https://github.com/your-username/browser-automation/issues) 或 [联系我](mailto:your-email)！** 🐉
