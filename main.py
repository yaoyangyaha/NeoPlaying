import os
import sys
import subprocess
import threading
import pystray
import webbrowser
from PIL import Image
import win32api
import win32con

EXE_PATH = r"NowPlayingService.exe"     
ICON_PATH = "nowplaying.ico"               

def create_tray_icon():
    image = Image.open(ICON_PATH) if os.path.exists(ICON_PATH) else Image.new('RGB', (64, 64), 'white')
    menu = pystray.Menu(
        pystray.MenuItem("主页", open_web("http://localhost:9863")),
        pystray.MenuItem("设置", open_web("http://localhost:9863/settings/general")),
        pystray.MenuItem("退出", exit_app)
    )
    icon = pystray.Icon("app_icon", image, "NeoPlaying运行中", menu)
    icon.run()

def open_web(WEB_URL):
    webbrowser.open(WEB_URL)

def exit_app(icon):
    if process and process.poll() is None:
        terminate_process_tree(process.pid)
    icon.stop()
    os._exit(0)

def run_exe():
    global process
    while True:
        try:
            process = subprocess.Popen(EXE_PATH)
            process.wait()
            threading.Event().wait(5)
        except Exception as e:
            print(f"进程启动失败: {e}")
            threading.Event().wait(10) 

def terminate_process_tree(pid):
    try:
        subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, check=True)
    except subprocess.CalledProcessError:
        pass

if __name__ == "__main__":
    if sys.executable.endswith("pythonw.exe"):
        pass 
    else:
        try:
            win32api.ShowWindow(win32api.GetConsoleWindow(), win32con.SW_HIDE)
        except:
            pass
    process = None
    threading.Thread(target=run_exe, daemon=True).start()
    create_tray_icon()