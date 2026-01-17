#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatBox Client Launcher
Khởi chạy ứng dụng chat client với giao diện đẹp
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_requirements():
    """Kiểm tra yêu cầu hệ thống"""
    # Kiểm tra Python version
    if sys.version_info < (3, 8):
        messagebox.showerror("Lỗi", "Cần Python 3.8 trở lên để chạy ứng dụng!")
        return False
    
    # Kiểm tra Tkinter
    try:
        import tkinter as tk
        # Test tạo window
        test_root = tk.Tk()
        test_root.withdraw()
        test_root.destroy()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Tkinter không khả dụng: {str(e)}")
        return False
    
    return True

def show_launcher():
    """Hiển thị launcher để chọn phiên bản client"""
    root = tk.Tk()
    root.title("ChatBox Launcher")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg='#2c3e50')
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Title
    title_label = tk.Label(root, text="💬 ChatBox Launcher",
                          font=('Segoe UI', 20, 'bold'),
                          fg='#3498db', bg='#2c3e50')
    title_label.pack(pady=(30, 20))
    
    # Description
    desc_label = tk.Label(root, text="Chọn phiên bản client để khởi chạy:",
                         font=('Segoe UI', 12),
                         fg='#ecf0f1', bg='#2c3e50')
    desc_label.pack(pady=(0, 30))
    
    # Buttons frame
    buttons_frame = tk.Frame(root, bg='#2c3e50')
    buttons_frame.pack(pady=20)
    
    # Enhanced client button (recommended)
    enhanced_btn = tk.Button(buttons_frame, 
                           text="🚀 Client Nâng Cao\n(Khuyên dùng)",
                           font=('Segoe UI', 12, 'bold'),
                           bg='#27ae60', fg='white',
                           relief='flat', bd=0, cursor='hand2',
                           width=20, height=3,
                           command=lambda: launch_client('enhanced'))
    enhanced_btn.pack(pady=(0, 15))
    
    # Basic client button
    basic_btn = tk.Button(buttons_frame,
                         text="📱 Client Cơ Bản",
                         font=('Segoe UI', 12, 'bold'),
                         bg='#3498db', fg='white',
                         relief='flat', bd=0, cursor='hand2',
                         width=20, height=2,
                         command=lambda: launch_client('basic'))
    basic_btn.pack(pady=(0, 15))
    
    # Info label
    info_label = tk.Label(root, 
                         text="Client Nâng Cao có giao diện đẹp hơn và nhiều tính năng hơn",
                         font=('Segoe UI', 9),
                         fg='#bdc3c7', bg='#2c3e50')
    info_label.pack(pady=(20, 0))
    
    def launch_client(client_type):
        """Launch selected client"""
        root.destroy()
        
        try:
            if client_type == 'enhanced':
                # Import and run enhanced client
                from enhanced_client import EnhancedChatClient
                app = EnhancedChatClient()
                app.root.mainloop()
            else:
                # Import and run basic client
                from main import ChatClient
                app = ChatClient()
                app.root.mainloop()
                
        except ImportError as e:
            messagebox.showerror("Lỗi", f"Không thể import client: {str(e)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khởi chạy: {str(e)}")
    
    root.mainloop()

def main():
    """Main function"""
    print("🚀 ChatBox Client Launcher")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Show launcher
    try:
        show_launcher()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    main()