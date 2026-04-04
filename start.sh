#!/usr/bin/env python3
"""
快速启动脚本 - 一键启动浏览器自动化服务
包含后端 API 和前端 UI
"""
import subprocess
import os
import sys
import time
import webbrowser
from pathlib import Path


def main():
    """主函数"""
    print("\n🚀 启动智能浏览器自动化工具...")
    print("=" * 50)
    
    # 检查环境
    print("\n1️⃣ 检查环境...")
    python_version = sys.version_info
    print(f"✓ Python 版本: {python_version}")
    
    # 检查依赖
    try:
        import streamlit
        import fastapi
        import playwright
        print(f"✓ Streamlit: {streamlit.__version__}")
        print(f"✓ FastAPI: {fastapi.__version__}")
        print(f"✓ Playwright: {playwright.__version__}")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return
    
    # 检查配置文件
    if not Path(".env").exists():
        print("\n⚠️  未找到 .env 文件，正在创建...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✓ 已从 .env.example 创建 .env")
            print("⚠️️  请编辑 .env 文件，填入你的 API Key")
            return
        else:
            print("❌ 未找到 .env.example 文件")
            return
    
    # 检查 API Key
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    
    if not openai_key and not anthropic_key:
        print("\n❌  请在 .env 中配置至少一个 LLM API Key：")
        print("   OPENAI_API_KEY 或 ANTHROPIC_API_KEY")
        return
    
    print("✅ API Key 已配置")
    
    # 创建必要的目录
    print("\n📁 创建目录...")
    for dir_name in ["screenshots", "data", "logs"]:
        Path(dir_name).mkdir(exist_ok=True)
    print("✓ 目录创建完成")
    
    # 启动后端
    print("\n2️⃣ 启动后端 API...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "app.main"],
        env=os.environ,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("✓ 后端 API 正在启动...")
    time.sleep(3)  # 等待服务启动
    
    # 启动前端
    print("3️⃣ 启动前端 UI...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        env=os.environ,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("✓ 前端 UI 正在启动...")
    time.sleep(3)  # 等待 UI 启动
    
    # 打开浏览器
    print("\n🌐 打开浏览器...")
    print("   后端 API: http://localhost:8000")
    print("   前端 UI: http://localhost:8501")
    
    webbrowser.open("http://localhost:8501")
    
    print("\n🎉 启动完成！")
    print("=" * 50)
    print("\n💡 提示：")
    print("   - 按 Ctrl+C 停止服务")
    print("   - 关闭终端窗口可停止服务")
    print("   - 如果端口被占用，请检查端口占用情况")
    print("\n")
    
    # 保持运行
    try:
        while True:
            # 检查进程是否还在运行
            backend_alive = backend_process.poll() is None
            frontend_alive = frontend_process.poll() is None
            
            if not backend_alive and not frontend_alive:
                print("\n\n🛑 服务已停止")
                break
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")


if __name__ == "__main__":
    main()
