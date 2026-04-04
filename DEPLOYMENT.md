# 部署指南

## 🚀 快速部署

### 方式 1：本地开发

```bash
# 克隆项目
git clone https://github.com/your-username/browser-automation.git
cd browser-automation

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
playwright install

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 运行后端
python -m app.main

# 运行前端（新终端）
streamlit run frontend/app.py
```

### 方式 2：Docker �署

```bash
# 构建 Docker 镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f app
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| OPENAI_API_KEY | OpenAI API 密钥 | - |
| ANTHROPIC_API_KEY | Anthropic API 密钥 | - |
| LLM_MODEL | LLM 模型 | gpt-4o |
| BROWSER_HEADLESS | 无头模式 | true |
| BROWSER_TIMEOUT | 页面超时（秒） | 30 |
| HOST | 服务地址 | 0.0.0.0 |
| PORT | 服务端口 | 8000 |

### 数据存储

- **截图目录：** `./screenshots/`
- **数据目录：** `./data/`
- **日志目录：** `./logs/`
- **数据库：** `./data/browsers.db` (SQLite)

## 📝 API 文档

### 基础 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/tasks` | POST | 创建任务 |
| `/api/tasks` | GET | 获取任务列表 |
| `/api/tasks/{task_id}` | GET | 获取任务详情 |
| `/api/tasks/{task_id}/execution` | GET | 获取执行日志 |
| `/api/browser/navigate` | POST | 导航到 URL |
| `/api/browser/screenshot` | POST | 截图 |
| `/api/agent/execute` | POST | 直接执行 Agent 任务 |

### 数据模型

#### Task（任务）
```json
{
  "id": "task_20260405_000000",
  "title": "搜索 Python 教程",
  "description": "在 Google 上搜索教程",
  "user_input": "打开 Google 并搜索 Python 教程",
  "status": "completed",
  "result": "任务执行成功...",
  "created_at": "2026-04-05T00:00:00Z",
  "updated_at": "2026-04-05T00:01:00Z"
}
```

#### Execution（执行记录）
```json
{
  "id": "exec_20260405_000001",
  "task_id": "task_20260405_000000",
  "step": "navigate",
  "input": "导航到 https://www.google.com",
  "output": "已导航到 https://www.google.com",
  "status": "success",
  "timestamp": "2026-04-05T00:00:00Z"
}
```

## 📚 使用教程

### 教程 1：创建第一个任务

1. 打开 Streamlit UI（`http://localhost:8501`）
2. 输入任务标题："搜索教程"
3. 输入任务描述："在 Google 上搜索 Python 教程"
4. 输入自然语言指令："帮我打开 Google 并搜索 'Python 教程'"
5. 点击「创建任务」

### 教程 2：直接使用 Agent

```python
import requests

response = requests.post(
    "http://localhost:8000/api/agent/execute",
    json={"user_input": "打开 Google 并搜索 Python 教程"}
)

result = response.json()
print(result["output"])
```

### 教程 3：批量操作

```python
# 批量填写表单
form_data = {
    "姓名": "张三",
    "邮箱": "zhangsan@example.com",
    "电话": "13800000000",
    "地址": "北京市朝阳区"
}

response = requests.post(
    "http://localhost:8000/api/agent/execute",
    json={"user_input": f"帮我打开 {url} 并填写表单：{json.dumps(form_data, ensure_ascii=False)}"}
)

print(response.json())
```

## 🐛 常见问题

### 1. 浏览器启动失败

**原因：** Playwright 浏览器未安装

**解决：**
```bash
playwright install
```

### 2. LLM API 调用失败

**原因：** API Key 未配置或错误

**解决：**
1. 检查 `.env` 文件中的 API Key
2. 确保网络连接正常
3. 检查 API Key 是否有效

### 3. 任务执行失败

**原因：** LLM 无法理解指令或页面加载超时

**解决：**
1. 检查网络连接
2. 检查页面是否可访问
3. 尝试使用更明确的指令
4. 调整 `BROWSER_TIMEOUT` 参数

### 4. 数据提取失败

**原因：** 选择器错误或页面结构变化

**解决：**
1. 检查页面是否已加载完成
2. 尝试使用更通用的选择器
3. 使用 AI 辅助识别页面结构

## 📊 性能优化

### 1. 减少页面加载时间
- 启用无头模式（`headless=true`）
- 启用缓存（`use_cache=True`）
- 限制资源加载（可配置）

### 2. 加快 LLM 响应
- 使用更快的 LLM（如 gpt-4o-mini）
- 降低 max_tokens
- 减少 conversation history

### 3. 优化数据库查询
- 添加索引
- 限制返回数量
- 使用连接池

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 贡献类型
- 🐛 Bug 修复
- ✨ 新功能开发
- 📚 文档改进
- 🧪 代码优化
- 🎨 UI 改进

### 贡献流程
1. Fork 项目
2. 创建新分支
3. 提交更改
4. 推送 Pull Request
5. 等待审查

### 开发规范
- 遵循 PEP 8 代码规范
- 添加单元测试
- 更新文档
- 添加 JSDoc 注释

---

**有问题吗？[查看文档](https://github.com/your-username/browser-automation/issues) 或 [联系我](mailto:your-email)！** 🐉
