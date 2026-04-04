import streamlit as st
from datetime import datetime

def show():
    st.set_page_config(
        page_title="创建任务 - 浏览器自动化",
        page_icon="➕",
        layout="centered"
    )
    
    st.title("➕️ 创建新任务")
    
    st.markdown("""
    ### 📝 用自然语言描述你的任务，我会用 AI 理解并自动执行
    
    **示例：**
    - "帮我打开 Google 并搜索 'Python 教程'"
    - "帮我打开 example.com 并填写表单：姓名=张三，邮箱=zhangsan@example.com，电话=13800000000"
    - "访问 Hacker News，提取前 10 条新闻的标题和链接"
    """)
    
    # 任务输入
    title = st.text_input("任务标题*", placeholder="例如：搜索 Python 教程", key="title")
    description = st.text_area("任务描述（可选）", placeholder="描述任务的详细信息...", height=100, key="description")
    
    user_input = st.text_area("自然语言指令*", placeholder="例如：帮我打开 Google 并搜索 Python 教程，提交表单", height=200, key="input")
    
    # 自动执行开关
    auto_submit = st.checkbox("立即执行", value=False, key="auto_submit", help="创建后立即开始执行")
    
    if st.button("🚀 创建任务", type="primary", use_container_width=True):
        # 将按钮放到按钮区域
        st.markdown("\n\n---")
        
        if title.strip() and user_input.strip():
            # 创建任务
            task_data = {
                "title": title,
                "description": description,
                "user_input": user_input
            }
            
            # 按钮样式
            col1, col2 = st.columns(2)
            
            with col1:
                if auto_submit:
                    create_btn = st.form_submit_button("🚀 创建并执行", type="primary")
                else:
                    create_btn = st.form_submit_button("🚀 创建任务", type="primary")
            with col2:
                cancel_btn = st.form_submit_button("取消", type="secondary")
            
            create_btn.type = "primary"
            create_btn.use_container_width = True
            create_btn.disabled = False
            
            if create_btn.form_submit_button.form_completed:
                if cancel_btn.form_submit_button.form_completed:
                    pass  # 用户点击了取消
                else:
                    pass  # 用户点击了创建
                    pass
        else:
            # 标题或输入为空
            st.warning("⚠️ 请输入标题和自然语言指令")
        else:
            # 标题为空或输入为空
            st.warning("⚠️ 请输入任务标题和自然语言指令")
    
    st.markdown("\n\n---")
    
    # 快速填充按钮
    st.subheader("🚀 快速填充示例")
    
    col1, col2 = st.columns(2)
    
    with col1:
        quick_tasks_1 = [
            "打开 Google 并搜索 Python 教程",
            "访问 Hacker News 提取新闻",
            "打开 example.com 填写表单",
        ]
        
        selected_task = st.selectbox("选择快速任务：", quick_tasks_1)
        
        if st.button("🚀 使用此模板", key="quick_task_1"):
            pass
    with col2:
        quick_tasks_2 = [
            "测试登录功能",
            "批量提取数据",
            "截取页面截图",
        ]
        
        selected_task = st.selectbox("选择快速任务：", quick_tasks_2)
        
        if st.button("🚀 使用此模板", key="quick_task_2"):
            pass
