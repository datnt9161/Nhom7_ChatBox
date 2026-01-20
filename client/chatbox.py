#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatBox - Modern Application
Ứng dụng chat hiện đại với giao diện Material Design
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.modern_login_page import ModernLoginPage
from ui.modern_register_page import ModernRegisterPage
from ui.modern_chat_page import ModernChatPage
from modern_styles import ModernColors, ModernFonts

class ModernChatBox:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Application state
        self.current_page = None
        self.username = None
        self.socket = None
        
        # Create pages
        self.login_page = ModernLoginPage(
            self.root, 
            self.on_login_success, 
            self.show_register_page
        )
        
        self.register_page = ModernRegisterPage(
            self.root,
            self.on_register_success,
            self.show_login_page
        )
        
        self.chat_page = None
        
        # Show login page initially
        self.show_login_page()
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_window(self):
        """Setup main window"""
        self.root.title("💬 ChatBox - Modern Chat Application")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)  # Giảm kích thước tối thiểu
        self.root.configure(bg=ModernColors.GRAY_50)
        
        # Improve font rendering on Windows
        try:
            self.root.tk.call('tk', 'scaling', 1.0)
        except:
            pass
        
        # Center window
        self.center_window()
        
        # Try to set icon
        try:
            if os.path.exists('assets/icon.ico'):
                self.root.iconbitmap('assets/icon.ico')
        except:
            pass
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_login_page(self):
        """Show login page"""
        if self.current_page:
            self.current_page.hide()
        
        self.login_page.show()
        self.current_page = self.login_page
        self.root.title("💬 ChatBox - Sign In")
    
    def show_register_page(self):
        """Show register page"""
        if self.current_page:
            self.current_page.hide()
        
        self.register_page.show()
        self.current_page = self.register_page
        self.root.title("💬 ChatBox - Create Account")
    
    def show_chat_page(self, username, socket_conn):
        """Show chat page"""
        if self.current_page:
            self.current_page.hide()
        
        # Create chat page if not exists
        if not self.chat_page:
            self.chat_page = ModernChatPage(
                self.root,
                username,
                socket_conn,
                self.on_disconnect
            )
        
        self.chat_page.show()
        self.current_page = self.chat_page
        self.username = username
        self.socket = socket_conn
        self.root.title(f"💬 ChatBox - {username}")
    
    def on_login_success(self, username, socket_conn):
        """Handle successful login"""
        self.show_chat_page(username, socket_conn)
    
    def on_register_success(self):
        """Handle successful registration"""
        self.show_login_page()
        # Clear login form and show success message
        self.login_page.clear_form()
        self.login_page.show_status("Registration successful! Please sign in.", "success")
    
    def on_disconnect(self):
        """Handle disconnect"""
        self.username = None
        self.socket = None
        self.chat_page = None
        
        # Clear login form and show login page
        self.login_page.clear_form()
        self.show_login_page()
    
    def on_closing(self):
        """Handle window closing"""
        if self.chat_page and self.socket:
            if messagebox.askyesno("Confirm Exit", 
                                  "You are currently in a chat session. Are you sure you want to exit?"):
                self.chat_page.disconnect()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = ModernChatBox()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()