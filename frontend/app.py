# 前端页面
import streamlit as st
from datetime import datetime

# 页面配置
def show():
    st.set_page_config(
        title="浏览器自动化",
        page_icon="🤖",
        layout="centered"
    )
    
    st.title("🤖 智能浏览器自动化工具")
    
    # 侧边栏
    with st.sidebar:
        st.title("📋 导航")
        page = st.selectbox(
            "选择页面",
            ["🏠 首页", "🎯 创建任务", "📊 任务列表", "🔧 设置"]
        )
        
        if page == "🏠 首页":
            _show_home()
        elif page == "🎯 创建任务":
            _show_create_task()
        elif page == "📊 任务列表":
            _show_task_list()
        elif page == "🔧 设置":
            _show_settings()
        
        st.write("---")
        
        # 系统状态
        try:
            import requests
            
            response = requests.get("http://localhost:8000/api/health", timeout=2)
            if response.status_code == 200:
                status = response.json().get("status", "unknown")
                browser_status = response.json().get("browser", "unknown")
                
                st.markdown(f"""
                **系统状态**
                
                | 项目 | 状态 |
                | --- | ---- |
                | API 服务 | 🟢 运行中 |
                | 浏览器 | {browser_status} |
                """)
            else:
                st.error("❌ 无法连接到后端服务")
        except:
            st.error("❌ 无法连接到后端服务")
    
    st.write("---")
    
    # 快捷入口
    st.subheader("🚀 快速入口")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("🔍 访问网站", use_container_width=True)
        url = st.text_input("URL:", placeholder="https://")
        if st.button("🚀 访问", type="primary", use_container_width=True):
            if url:
                import requests
                try:
                    response = requests.post(
                        "http://localhost:0/api/browser/navigate",
                        json={"url": url},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        if response.json().get("success"):
                            st.success("✅ 导航成功")
                        else:
                            st.error(f"❌ 导航失败: {response.json()}")
                    else:
                        st.error(f"❌ 请求失败: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ 错误: {e}")
    
    with col2:
        st.button("📸 截图", use_container_width=True)
        if st.button("📸 截图", use_container_width=True):
            import requests
            try:
                response = requests.post(
                    "http://localhost:8000/api/browser/screenshot",
                    json={},
                    timeout=10
                )
                
                if response.status_code == 200:
                    screenshot_path = response.json().get("screenshot_path")
                    st.success(f"✅ 截图已保存: {screenshot_path}")
                    
                    # 显示截图（如果存在）
                    if screenshot_path and screenshot_path.startswith("screenshots/"):
                        st.image(screenshot_path)
                else:
                    st.warning("⚠️ 截图未保存到 screenshots/ 目录")
                else:
                    st.error(f"❌ 截图失败: {response.json()}")
            except Exception as e:
                st.error(f"❌ 错误: {e}")
    
    st.markdown("---")



def _show_home():
    """首页"""
    st.header("🏠️ 创建新任务")
    
    # 自然语言输入
    st.subheader("📝 自然语言描述你的任务")
    user_input = st.text_area(
        "在这里输入你的任务描述...",
        height=150,
        placeholder="例如：帮我打开 Google 并搜索 'Python 教程' 或 帮我打开 example.com 并填写表单：姓名=张三，邮箱=test@example.com"
    )
    
    if st.button("🚀 创建任务", type="primary", use_container_width=True):
        if user_input.strip():
            import requests
            
            try:
                response = requests.post(
                    "http://localhost:8000/api/tasks",
                    json={
                        "title": user_input.split("\n")[0][:50],  # 使用第一行作为标题
                        "description": user_input,
                        "user_input": user_input
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    task = response.json()
                    st.success(f"✅ 任务创建成功！任务 ID: {task['id']}")
                    
                    # 提示查看任务状态
                    st.info("💡 点击「任务列表」查看执行进度")
                else:
                    st.error(f"❌ 创建任务失败: {response.json()}")
            except Exception as e:
                st.error(f"❌ 创建任务失败: {e}")

# 示例任务
    st.markdown("### 📝 示例任务")

    example_tasks = [
        {
            "title": "搜索教程",
            "input": "帮我打开 Google 并搜索 'Python 机器学习教程'"
        },
        {
            "title": "填写表单",
            "input": "帮我打开 https://example.com/contact 并填写表单：姓名=张三，邮箱=zhangsan@example.com，电话=13800000000"
        },
        {
            "title": "提取数据",
            "input": "访问 https://news.ycombinator.com，提取前10条新闻的标题和链接"
        },
        {
            "title": "登录测试",
            "input": "测试登录功能：访问 https://example.com/login，输入 test@example.com / password123，点击登录按钮，验证跳转"
        }
    ]
    
    for task in example_tasks:
        with st.expander():
            st.markdown(f"**{task['title']}**")
            st.code(f": task['input'])
            
            if st.button("执行", key=f"task_{task['title']}", use_container_width=True):
                import requests
                
                try:
                    response = requests.post(
                        "http://localhost:8000/api/agent/execute",
                        json={"user_input": task['input']},
                        timeout=30
                    )
                    
                    result = response.json()
                    
                    if result.get("success"):
                        st.success(f"✅ 执行成功")
                        if "output" in result:
                            st.code(f"输出结果:\n\n{result['output']}")
                    else:
                        st.info("✅ 执行成功（无输出）")
                    else:
                        if "error" in result:
                            st.error(f"❌ 执行失败: {result['error']}")
                        else:
                            st.error("❌ 未知错误")
                except Exception as e:
                    st.error(f"❌ 错误: {e}")
            
            st.divider()

def _show_create_task():
    """创建任务页面"""
    st.header("🎯 创建新任务")
    
    with st.form("task_form"):
        title = st.text_input("任务标题*", placeholder="例如：搜索 Python 教程", key="task_title")
        
        description = st.text_area("任务描述（可选）", placeholder="描述任务的详细信息...", height=100, key="task_description")
        user_input = st.text_area("自然语言指令*", placeholder="例如：帮我打开 Google 并搜索 Python 教程", height=200, key="task_input")
        
        auto_submit = st.checkbox("立即执行", value=False, key="auto_submit")
        
        advanced_options = st.expander("高级选项（可选）", expanded=False):
            use_visual_analysis = st.checkbox("使用视觉分析", value=True, key="use_visual_analysis")
            headless = st.checkbox("无头模式（headless）", value=True, key="headless")
            slow_mo = st.checkbox("慢速模式（慢速模式便于观察）", value=False, key="slow_mo")
        
        st.form_submit_button("创建任务", type="primary", use_container_width=True)
        
        if st.form_submit_button.form_completed:
            import requests
            
            try:
                # 确保标题存在
                title_value = title or "未命名任务"
                
                task_data = {
                    "title": title_value,
                    "description": description or "",
                    "user_input": user_input
                }
                
                # 创建任务
                response = requests.post(
                    "http://localhost:8000/api/tasks",
                    json=task_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    task = response.json()
                    st.success(f"✅ 任务创建成功！任务 ID: {task['id']}")
                    
                    if auto_submit:
                        # 立即执行
                        exec_result = requests.post(
                            "http://localhost:8000/api/agent/execute",
                            json={"user_input": user_input},
                            timeout=30
                        )
                        
                        if exec_result.status_code == 200:
                            result = exec_result.json()
                            
                            st.subheader("📊 执行结果")
                            
                            if result.get("success"):
                                st.code(f"输出结果:\n\n{result['output']}")
                            else:
                                if "error" in result:
                                    st.error(f"❌ 执行失败: {result['error']}")
                                else:
                                    st.error("❌ 未知错误")
                        else:
                            st.error(f"❌ 执行请求失败: {exec_result.status_code}")
                else:
                    st.error(f"❌ 创建任务失败: {response.json()}")
            except Exception as e:
                st.error(f"❌ 创建任务失败: {e}")

def _show_task_list():
    """任务列表页面"""
    st.header("📋 任务列表")
    
    import requests
    
    # 获取任务列表
    response = requests.get("http://localhost:8000/api/tasks", timeout=10)
    
    if response.status_code == 200:
        tasks = response.json()
        
        if not tasks:
            st.info("📭 暂时还没有任务")
            return
        
        # 过滤任务
        status_filter = st.selectbox(
            "筛选状态",
            ["全部", "待执行", "运行中", "已完成", "失败"]
        )
        
        sort_by = st.selectbox(
            "排序方式",
            ["创建时间", "标题", "状态"],
            index=0
        )
        
        if tasks:
            tasks.sort(key=lambda t: t["created_at"], reverse=True)
        
        # 显示任务卡片
        for i, task in enumerate(tasks):
            with st.expander(f"task_{task['id']}", expanded=False):
                # 状态图标
                status_icon = {
                    TaskStatus.PENDING: "⏳️",
                    TaskStatus.RUNNING: "🔄",
                    TaskStatus.COMPLETED: "✅",
                    TaskStatus.FAILED: "❌",
                    TaskStatus.CANCELLED: "⏸️",
                }.get(task.get("status", TaskStatus.PENDING))
                
                # 任务标题和描述
                st.markdown(f"""
                ### {status_icon} {task['title']}
                
                **任务 ID:** `{task['id']}`
                **创建时间:** {task['created_at']}
                
                **描述：**
                {task['description'][:100] or "无描述"}
                """)
                
                # 任务操作按钮
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if task.get("status") == TaskStatus.PENDING:
                        if st.button("▶️ 开始执行", key=f"start_{task['id']}"):
                            _start_task(task['id'])
                    elif task.get("status") == TaskStatus.RUNNING:
                        if st.button("⏸️ 查看详情", key=f"view_{task['id']}"):
                            _view_task_detail(task['id'])
                    elif task.get("status") == TaskStatus.COMPLETED:
                        if st.button("📄 查看详情", key=f"view_{task['id']}"):
                            _view_task_detail(task['id'])
                    elif task.get("status") == TaskStatus.FAILED:
                        if st.button("🔄 重试", key=f"retry_{task['id']}"):
                            _retry_task(task['id'])
                
                with col2:
                    if task.get("status") == TaskStatus.RUNNING:
                        st.info("⏳️ 任务执行中...")
                    elif task.get("status") == TaskStatus.FAILED:
                        st.error(f"❌ 任务失败: {task.get('error', '未知错误')}")
                
                with col3:
                    if task.get("status") == Task.completed:
                        if st.button("🗑️ 删除", key=f"delete_{task['id']}"):
                            _delete_task(task['id'])
                    elif task.get("status") == TaskStatus.FAILED:
                        if st.button("🗑️ 删除", key=f"delete_{task['id']}"):
                            _delete_task(task['id'])
                
                st.divider()
    
    else:
        st.error(f"❌ 获取任务列表失败: {response.status_code}")

def _show_task_detail(task_id: str):
    """任务详情页面"""
    import requests
    
    # 获取任务详情
    response = requests.get(f"http://localhost:8000/api/tasks/{task_id}", timeout=10)
    
    if response.status_code == 200:
        task = response.json()
        
        st.header(f"### 📋 {task['title']}")
        
        # 基本信息
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**基本信息**")
            st.write(f"**任务 ID:** `{task['id']}`")
            st.write(f"**状态：** {task['status']}")
            st.write(f"**创建时间：** {task['created_at']}")
            st.write(f"**更新时间：** {task['updated_at']}")
            
            if task.get("started_at"):
                st.write(f"**开始时间：** {task['started_at']}")
            if task.get("completed_at"):
                st.write(f"**完成时间：** {task['completed_at']}")
            
            st.write(f"**描述：**")
            st.write(task.get("description", "无描述"))
            
            st.write(f"**用户输入：**")
            st.code(task.get("user_input", "无"))
            
            # 结果
            if task.get("result"):
                st.write(f"**结果：**")
                st.code(task.get("result", "无结果"))
            
            # 错误信息
            if task.get("error"):
                st.error(f"**错误信息：**")
                st.code(task.get("error", "无错误"))
            
            # 按钮
            if task.get("status") in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                if st.button("🔄 重试", key="retry"):
                    _retry_task(task_id)
            
            if st.button("🗑️ 删除", key="delete"):
                _delete_task(task_id)
            
            st.divider()
            
            # 执行日志
            st.markdown("### 📊 执行日志")
            exec_response = requests.get(
                f"http://localhost:8000/api/tasks/{task_id}/execution",
                timeout=10
            )
            
            if exec_response.status_code == 200:
                executions = exec_response.json()
                
                if executions:
                    # 按时间排序
                    executions.sort(key=lambda x: x["timestamp"], reverse=True)
                    
                    for exec_log in executions:
                        timestamp = exec_log.get("timestamp", "未知时间")
                        step = exec_log.get("step", "未知步骤")
                        status_icon = {
                            "SUCCESS": "✅",
                            "FAILED": "❌",
                            "ERROR": "⚠️"
                        }.get(exec_log.get("status", "UNKNOWN"))
                        
                        st.markdown(f"""
                        **{status_icon} {step}** * {timestamp}*
                        **输入：** {exec_log.get("input", "无")}
                        **输出：** {exec_log.get("output", "无")}
                        **错误：** {exec_log.get("error", "无")}
                        """)
                        st.divider()
                    
                    if not executions:
                        st.info("暂无执行日志")
                else:
                    st.error(f"获取执行日志失败: {exec_response.status_code}")
            
            else:
                st.error(f"获取执行日志失败: {exec_response.status_code}")
        
        else:
            st.error(f"获取任务详情失败: {response.status_code}")
    
    else:
        st.error(f"获取任务详情失败: {response.status_code}")
    
    if st.button("← 返回", use_container_width=True):
        _show_task_list()

def _start_task(task_id: str):
    """开始执行任务"""
    import requests
    
    response = requests.post(
        f"http://localhost:8000/api/tasks/{task_id}/start",
        timeout=10
    )
    
    if response.status_code == 200:
        st.success(f"✅ 任务 {task_id} 开始执行")
    else:
        st.error(f"❌ 开始任务失败: {response.status_code}")

def _delete_task(task_id: str):
    """删除任务"""
    import requests
    
    response = requests.delete(
        f"http://localhost:8000/api/tasks/{task_id}",
        timeout=10
    )
    
    if response.status_code == 200:
        st.success(f"✅ 任务 {task_id} 已删除")
    else:
        st.error(f"❌ 删除任务失败: {response.status_code}")
    
    st.rerun()

def _retry_task(task_id: str):
    """重试任务"""
    import requests
    
    # 重置任务为待执行状态
    response = requests.patch(
        f"http://localhost:8000/api/tasks/{task_id}",
        json={"status": "pending"},
        timeout=10
    )
    
    if response.status_code == 200:
        # 重新执行
        exec_response = requests.post(
            f"http://localhost:8000/api/tasks/{task_id}/start",
            timeout=10
        )
        
        if exec_response.status_code == 200:
            st.success(f"✅ 任务 {task_id} 已重新开始")
        else:
            st.error(f"❌ 重试任务失败: {exec_response.status_code}")
    else:
        st.error(f"❌ 重置任务失败: {response.status_code}")
    
    st.rerun()

def _show_settings():
    """设置页面"""
    st.header("⚙️ 设置")
    
    st.subheader("🌐 LLM 配置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        llm_model = st.selectbox(
            "LLM 模型",
            ["gpt-4o", "gpt-4o-mini", "claude-3.5-sonnet", "claude-3-opus"],
            index=0
        )
        
        temperature = st.slider("温度 (Temperature)", 0.0, 2.0, 0.7, 0.05, key="temperature")
        max_tokens = st.number_input("最大 Tokens", 100, 128000, 4000, 4096, key="max_tokens")
        
        if st.button("💾 保存配置", type="primary"):
            import requests
            
            config_data = {
                "llm_model": llm_model,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            try:
                response = requests.post(
                    "http://localhost:8000/api/config/llm",
                    json=config_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.success("✅ LLM 配置已保存")
                else:
                    st.error(f"❌ 保存失败: {response.json()}")
            except Exception as e:
                st.error(f"❌ 保存配置失败: {e}")
    
    with col2:
        st.subheader("🌐 浏览器配置")
        
        headless = st.checkbox("无头模式（headless）", value=True, key="headless")
        slow_mo = st.checkbox("慢速模式（便于观察）", value=False, key="slow_mo")
        
        screenshot_format = st.selectbox(
            "截图格式",
            ["PNG", "JPEG", "WEBP"],
            index=0
        )
        
        viewport_width = st.number_input("视口宽度", 800, 2560, 1280, 10, key="viewport_width")
        viewport_height = st.number_input("视口高度", 600, 1440, 720, 10, key="viewport_height")
        
        timeout = st.number_input("页面加载超时（秒）", 5, 60, 30, key="timeout")
        
        if st.button("💾 保存配置", type="primary"):
            import requests
            
            config_data = {
                "headless": headless,
                "slow_mo": slow_mo,
                "screenshot_format": screenshot_format,
                "viewport_width": viewport_width,
                "viewport_height": viewport_height,
                "timeout": timeout
            }
            
            try:
                response = requests.post(
                    "http://localhost:8000/api/config/browser",
                    json=config_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.success("✅ 浏览器配置已保存")
                else:
                    st.error(f"❌ 保存失败: {response.json()}")
            except Exception as e:
                st.error(f"❌ 保存配置失败: {e}")
    
    st.markdown("---")
    
    st.subheader("🔧 系统配置")
    
    # 获取当前配置
    import requests
    
    try:
        response = requests.get("http://localhost:8000/api/config", timeout=10)
        
        if response.status_code == 200:
            config = response.json()
            
            st.markdown("### 📊 当前配置")
            
            # LLM 配置
            st.markdown("**LLM 配置**")
            st.write(f"- 模型：{config.get('llm_model', '未设置')}")
            st.write(f"- 温度：{config.get('temperature', '未设置')}")
            st.write(f"- 最大 Tokens：{config.get('max_tokens', '未设置')}")
            
            # 浏览器配置
            st.markdown("**浏览器配置**")
            st.write(f"- 模式：{'无头模式' if config.get('headless', False) else '有头模式'}")
            st.write(f"- 慢速模式：{'启用' if config.get('slow_mo', False) else '关闭'}")
            st.write(f"- 视口：{config.get('viewport_width', '未设置')} x {config.get('viewport_height', '未设置')}")
            st.write(f"- 超时：{config.get('timeout', '30')} 秒")
            
            # 系统信息
            st.markdown("**系统信息**")
            st.write(f"- API 服务：{'🟢 在线' if 'success' in str(config.get('service', {})) else '❌ 离线'}")
            st.write(f"- 浏览器：{'🟢 在线' if 'running' in str(config.get('browser', {})) else '❌ 离线'}")
            
        else:
            st.error(f"❌ 获取配置失败: {response.status_code}")
    except Exception as e:
        st.error(f"❌ 获取配置失败: {e}")
    
    st.markdown("---")
    
    # 重置按钮
    if st.button("🔄 重置为默认配置", key="reset_config"):
        import requests
        
        try:
            response = requests.post(
                "http://localhost:8000/api/config/reset",
                timeout=10
            )
            
            if response.status_code == 200:
                st.success("✅ 配置已重置")
                st.rerun()
            else:
                st.error(f"❌ 重置失败: {response.json()}")
        except Exception as e:
            st.error(f"❌ 重置失败: {e}")
