# README.md
(I try to use Openclaw on Coze mainland version to make it LOL, first try on errrr vibe coding without brain)
# 🤖 智能浏览器自动化工具

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
[![License](https://img.shields.io/badge/License-MIT-green.svg)
[![Stars](https://img.shields.io/github/stars/your-username/browser-automation?style=flat-square)
[![Issues](https://img.shields.io/github/issues/your-username/browser-automation/issues)
[ Discussions](https://github.com/your-username/browser-architecture)

一个基于 AI 的智能浏览器自动化工具，能够理解自然语言指令，自动执行网页操作任务。

## ✨ 特性

- 🎯 **自然语言控制** - 用自然语言描述任务，AI 自动拆解并执行
- 🤖 **AI 智能规划** - 自动将复杂任务拆解为可执行的步骤
- 📊 **实时可视化** - 实时查看执行过程和结果
- 💾 **记忆功能** - 记住常用操作，方便快速重复
- 🔧 **可扩展架构** - 易于添加新的工具和功能
- 🌐 **多浏览器支持** - 支持 Playwright（推荐）/ Selenium
- 🎨 **多 LLM 支持** - OpenAI GPT-4o / Claude 3.5 Sonnet
- 🎨 **多操作系统** 支持 Windows、Linux、macOS

## 🚀 快速开始

### 安装依赖

```bash
pip install browser-automation
playwright install
```

### 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

### 运行服务

```bash
python -m app.main.py
```

访问：http://localhost:8000

## 🎮 使用方式

### 1. 通过 Web UI
1. 打开 Streamlit UI
2. 输入任务描述
3. 点击执行

### 2. 通过 API

**创建任务：**
```bash
curl -X POST http://localhost:8000/api/tasks \\
  -H "Content-Type: application/json" \
  -d '{
      "title": "测试任务",
      "user_input": "帮我打开 Google 并搜索 Python 教程"
    }'
```

**查看任务：**
```bash
curl http://localhost:8000/api/tasks
```

**执行任务：**
```bash
curl -X POST http://localhost:8000/api/agent/execute \\
  -H "Content-Type: application/json" \
  -d '{"user_input": "打开 Google 搜索 Python 教程"}'
```

## 📚 主要功能

### 1. 自然语言任务解析
- 理解模糊的指令
- 自动拆解复杂任务为多步骤操作
- 智能判断输入意图（导航、填写、提取、测试）
- 自动检测表单字段并智能匹配
- 自动处理异常和重试

### 2. 智能表单填充
- 智能识别表单字段
- 自动匹配输入框到字段名、ID、Placeholder
- 验证字段类型（邮箱、手机号等）
- 支持自动提交
- 记录填充结果

### 3. 数据提取
- 提取表格数据
- 提取链接列表
- 提取图片和图片
- 提取标题和文本
- 自动导出为 CSV/JSON/Excel
- 智能识别结构化数据

### 4. 自动化测试
- 自动化登录流程
- 页面加载测试
- 表单提交测试
- 功能验证测试
- 生成测试报告

### 5. 视觉分析
- 页面结构分析
- 交互元素检测
- 性能优化建议
- 障点识别和修复

## 🔧 技术架构

```
┌─────────────────────────┐─────────────────┐
│    │    │    │    │              │    │    │
│    ↓    │    │    ↓              │    │    │
│  Browser │ UI    │    API             │    │    │
│  Controller │    │    │              │    │    │
│  ↓    │    │    ↓              │    │    │
│  LangChain │    │    ↓              │    │    │
│  ↓    │    │    ↓              │    │    │
│  FormFiller  │    │    ↓              │    │    │
│  DataExtractor│    │    ↓              │    │    │
│  DataExtractor│    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
│           │    │    ↓              │    │    │
└─────────────────────────┘─────────────────┘
    │    │    │    │              │    │    │
│    │    │    │              │    │    │
│    │    │    │              │    │    │
└─────────────────────────┘─────────────────┘
```

## 📚 使用示例

### 1. 自动搜索
```python
from browser_automation import BrowserAutomation

automation = BrowserAutomation()

task = "帮我打开 Google 并搜索 'Python 机器学习教程'"
automation.run(task)
```

### 2. 自动填写表单
```python
from browser_automation import BrowserAutomation

task = "帮我打开 https://form.example.com/user/register，填写表单：姓名=张三，邮箱=test@example.com，密码=123456"
automation.run(task)
```

### 3. 提取数据
```python
from browser_automation import BrowserAutomation

task = "访问 Hacker News，提取前 10 条新闻的标题和链接"
automation.run(task)
```

## 🔧 开发路线图

### 第 1 周：基础框架 ⭐⭐
- [x] 创建项目结构
- [x] 配置 Playwright
- [x] 创建核心类
- [x] 实现基础浏览器控制
- [x] 实现基础 API 接口
- [x] 添加 Streamlit 基础界面
- [x] 写基础测试

### 第 2 周：AI Agent 集成 ⭐⭐⭐
- [x] 集成 LangChain Agent
- [x] 实现自然语言任务解析
- [x] 实现工具调用逻辑
- [x] 实现任务步骤跟踪
- [x] 实现错误处理和重试
- [x] 写集成测试

### 第 3 周：核心功能 ⭐⭐⭐⭐
- [x] 完善表单填充
- [x] 完善数据提取
- [x] 添加视觉分析
- [x] 添加任务持久化存储
- [x] 添加任务调度
- [x] 添加批量操作

### 第 4 周：优化和部署 ⭐⭐⭐⭐
- [x] 性能优化
- [x] 添加更多工具和集成
- [x] 添加 Docker 支持
- [x] 添加文档
- [x] 添加示例和教程
- [x] 进行安全审查


## 📜 路线信息

- **主页：** https://github.com/your-username/browser-automation
- **文档：** https://your-username.github.io/browser-automation
- **Releases:** https://github.com/your-username/browser-automation/releases
- **License:** MIT License

---

**⭐ 如果这个项目对你有帮助，请给个 ⭐！🐉**
