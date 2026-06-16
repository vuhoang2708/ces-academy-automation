import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
from pathlib import Path

from config import BASE_DIR, PYTHON_EXE, FB_CDP_PORT, find_chrome

def run_script(script_path, name):
    executable = PYTHON_EXE
    base_dir = BASE_DIR
    full_path = base_dir / script_path

    if not full_path.exists():
        messagebox.showerror("Error", f"Không tìm thấy file:\n{full_path}")
        return
    if not Path(executable).exists():
        messagebox.showerror("Error", f"Không tìm thấy Python executable:\n{executable}")
        return

    try:
        # Chạy trong cửa sổ console mới để user dễ theo dõi log
        subprocess.Popen([executable, str(full_path)], cwd=str(base_dir), creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        messagebox.showerror("Error", f"Lỗi khi khởi chạy {name}:\n{e}")

def run_v11():
    run_script(r"Project_V11_SharePoint_Capture\capture_v11_sharepoint.py", "V11 SharePoint Capture")

def run_v12():
    run_script(r"Project_V12_Zalo_Screenshot\capture_v12_zalo_pro.py", "V12 Zalo Screenshot Pro")

def run_v13_fb():
    run_script(r"Project_V13_Media_Downloader\v13_fb_media_downloader.py", "V13 Facebook Media")

def run_v13_zalo():
    run_script(r"Project_V13_Media_Downloader\v13_zalo_media_downloader.py", "V13 Zalo Media")

def run_v14_zalo_diag():
    run_script(r"Project_V14_Zalo_Media_Downloader\zalo_media_v14.py", "V14 Zalo Diagnostic")

def open_chrome_debug():
    try:
        # Mở Chrome ở chế độ remote debugging tĩnh
        chrome = find_chrome()
        if not chrome:
            messagebox.showwarning("Warning", "Không tìm thấy Chrome. Hãy đặt CES_CHROME_EXE hoặc thêm Chrome vào PATH.")
            return
        subprocess.Popen([chrome, f"--remote-debugging-port={FB_CDP_PORT}"])
    except Exception as e:
        messagebox.showwarning("Warning", "Không thể tự động mở Chrome. Vui lòng thêm Chrome vào System PATH hoặc chạy lệnh thủ công.\nChi tiết lỗi: " + str(e))

# Khởi tạo giao diện chính
root = tk.Tk()
root.title("CES Academy Automation Hub")
root.geometry("450x420")
root.configure(bg="#1E1E1E")
root.resizable(False, False)

# Styling
style = ttk.Style(root)
style.theme_use("default")
style.configure("TButton",
                padding=10,
                font=("Arial", 10, "bold"),
                background="#333333",
                foreground="white",
                borderwidth=0)
style.map("TButton",
          background=[('active', '#555555')])

style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Arial", 11))

# Tiêu đề
title_label = ttk.Label(root, text="🚀 AUTOHUB - CES ACADEMY", font=("Arial", 14, "bold"), foreground="#4A90E2")
title_label.pack(pady=20)

subtitle_label = ttk.Label(root, text="Bảng điều khiển trung tâm (Corporate Edition)", font=("Arial", 10), foreground="#AAAAAA")
subtitle_label.pack(pady=0)

# Spacer
tk.Frame(root, height=20, bg="#1E1E1E").pack()

# Nút chức năng
btn_chrome = ttk.Button(root, text="🌐 BƯỚC 1: Mở Chrome Debug Mode", command=open_chrome_debug)
btn_chrome.pack(fill="x", padx=40, pady=6)

btn_v11 = ttk.Button(root, text="📄 V11 - Cào PDF SharePoint", command=run_v11)
btn_v11.pack(fill="x", padx=40, pady=6)

btn_v12 = ttk.Button(root, text="📸 V12 - Chụp ảnh khung chat Zalo", command=run_v12)
btn_v12.pack(fill="x", padx=40, pady=6)

btn_v13_fb = ttk.Button(root, text="⬇️ V13 - Tải Media Facebook Group", command=run_v13_fb)
btn_v13_fb.pack(fill="x", padx=40, pady=6)

btn_v14 = ttk.Button(root, text="🧪 V14 - Zalo Diagnostic Capture", command=run_v14_zalo_diag)
btn_v14.pack(fill="x", padx=40, pady=6)

# Footer
footer = ttk.Label(root, text="Powered by Antigravity Agent © 2026", font=("Arial", 9, "italic"), foreground="#666666")
footer.pack(side="bottom", pady=15)

# Bắt đầu vòng lặp ứng dụng
root.mainloop()
