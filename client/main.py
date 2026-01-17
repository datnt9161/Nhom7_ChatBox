#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatBox Client - Main Application
Modern GUI Chat Client with beautiful interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading
import json
from datetime import datetime
import hashlib
import os

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        
        # Network variables
        self.socket = None
        self.connected = False
        self.username = ""
        self.server_ip = "127.0.0.1"
        self.server_port = 5000
        
        # GUI variables
        self.current_frame = None
        self.online_users = []
        
        # Create frames
        self.create_login_frame()
        self.create_chat_frame()
        
        # Show login frame first
        self.show_login_frame()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("ChatBox - Modern Chat Client")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg='#2c3e50')
        
        # Center window
        self.center_window()
        
        # Set icon (if exists)
        try:
            self.root.iconbitmap('assets/chat_icon.ico')
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
        
    def setup_styles(self):
        """Setup modern styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 24, 'bold'),
                           foreground='#ecf0f1',
                           background='#2c3e50')
        
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 12),
                           foreground='#bdc3c7',
                           background='#2c3e50')
        
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           padding=(20, 10))
        
        self.style.configure('Login.TEntry',
                           font=('Segoe UI', 12),
                           padding=(10, 8))

    def create_login_frame(self):
        """Create beautiful login interface"""
        self.login_frame = tk.Frame(self.root, bg='#2c3e50')
        
        # Main container
        container = tk.Frame(self.login_frame, bg='#34495e', relief='raised', bd=2)
        container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)
        
        # Title
        title_label = tk.Label(container, text="💬 ChatBox", 
                              font=('Segoe UI', 28, 'bold'),
                              fg='#3498db', bg='#34495e')
        title_label.pack(pady=(30, 10))
        
        subtitle_label = tk.Label(container, text="Kết nối và trò chuyện cùng bạn bè",
                                 font=('Segoe UI', 12),
                                 fg='#bdc3c7', bg='#34495e')
        subtitle_label.pack(pady=(0, 30))
        
        # Login form
        form_frame = tk.Frame(container, bg='#34495e')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Username
        tk.Label(form_frame, text="Tên đăng nhập:", 
                font=('Segoe UI', 11, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(form_frame, font=('Segoe UI', 12),
                                      bg='#ecf0f1', fg='#2c3e50',
                                      relief='flat', bd=0, highlightthickness=2,
                                      highlightcolor='#3498db')
        self.username_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(form_frame, text="Mật khẩu:", 
                font=('Segoe UI', 11, 'bold'),
                fg='#ecf0f1', bg='#34495e').pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(form_frame, font=('Segoe UI', 12),
                                      bg='#ecf0f1', fg='#2c3e50',
                                      relief='flat', bd=0, show='*',
                                      highlightthickness=2, highlightcolor='#3498db')
        self.password_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Server settings
        server_frame = tk.Frame(form_frame, bg='#34495e')
        server_frame.pack(fill='x', pady=(10, 20))
        
        tk.Label(server_frame, text="Server IP:", 
                font=('Segoe UI', 10),
                fg='#bdc3c7', bg='#34495e').pack(anchor='w')
        
        self.server_ip_entry = tk.Entry(server_frame, font=('Segoe UI', 10),
                                       bg='#ecf0f1', fg='#2c3e50',
                                       relief='flat', bd=0)
        self.server_ip_entry.pack(fill='x', pady=(2, 5), ipady=4)
        self.server_ip_entry.insert(0, "127.0.0.1")
        
        tk.Label(server_frame, text="Port:", 
                font=('Segoe UI', 10),
                fg='#bdc3c7', bg='#34495e').pack(anchor='w')
        
        self.server_port_entry = tk.Entry(server_frame, font=('Segoe UI', 10),
                                         bg='#ecf0f1', fg='#2c3e50',
                                         relief='flat', bd=0)
        self.server_port_entry.pack(fill='x', pady=(2, 0), ipady=4)
        self.server_port_entry.insert(0, "5000")
        
        # Buttons
        button_frame = tk.Frame(container, bg='#34495e')
        button_frame.pack(pady=20, padx=40, fill='x')
        
        # Main login button
        self.login_btn = tk.Button(button_frame, text="🔐 Đăng nhập",
                                  font=('Segoe UI', 12, 'bold'),
                                  bg='#3498db', fg='white',
                                  relief='flat', bd=0, cursor='hand2',
                                  command=self.login)
        self.login_btn.pack(fill='x', pady=(0, 10), ipady=10)
        
        # Register button
        self.register_btn = tk.Button(button_frame, text="📝 Đăng ký tài khoản mới",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#27ae60', fg='white',
                                     relief='flat', bd=0, cursor='hand2',
                                     command=self.register)
        self.register_btn.pack(fill='x', pady=(0, 10), ipady=10)
        
        # Divider
        divider_frame = tk.Frame(button_frame, bg='#34495e', height=20)
        divider_frame.pack(fill='x', pady=(5, 5))
        
        tk.Label(divider_frame, text="hoặc",
                font=('Segoe UI', 9),
                fg='#95a5a6', bg='#34495e').pack()
        
        # Guest login button
        self.guest_btn = tk.Button(button_frame, text="👤 Đăng nhập khách",
                                   font=('Segoe UI', 11),
                                   bg='#95a5a6', fg='white',
                                   relief='flat', bd=0, cursor='hand2',
                                   command=self.guest_login)
        self.guest_btn.pack(fill='x', ipady=8)
        
        # Status label
        self.status_label = tk.Label(container, text="",
                                    font=('Segoe UI', 10),
                                    fg='#e74c3c', bg='#34495e')
        self.status_label.pack(pady=(10, 0))
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())

    def create_chat_frame(self):
        """Create beautiful chat interface"""
        self.chat_frame = tk.Frame(self.root, bg='#2c3e50')
        
        # Header
        header = tk.Frame(self.chat_frame, bg='#34495e', height=60)
        header.pack(fill='x', padx=10, pady=(10, 0))
        header.pack_propagate(False)
        
        # Header content
        header_left = tk.Frame(header, bg='#34495e')
        header_left.pack(side='left', fill='y', padx=20)
        
        tk.Label(header_left, text="💬 ChatBox", 
                font=('Segoe UI', 18, 'bold'),
                fg='#3498db', bg='#34495e').pack(anchor='w')
        
        self.welcome_label = tk.Label(header_left, text="",
                                     font=('Segoe UI', 11),
                                     fg='#bdc3c7', bg='#34495e')
        self.welcome_label.pack(anchor='w')
        
        # Header right
        header_right = tk.Frame(header, bg='#34495e')
        header_right.pack(side='right', fill='y', padx=20)
        
        self.disconnect_btn = tk.Button(header_right, text="🚪 Thoát",
                                       font=('Segoe UI', 10, 'bold'),
                                       bg='#e74c3c', fg='white',
                                       relief='flat', bd=0, cursor='hand2',
                                       command=self.disconnect)
        self.disconnect_btn.pack(side='right', pady=15)
        
        # Main content
        main_content = tk.Frame(self.chat_frame, bg='#2c3e50')
        main_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Users list
        left_panel = tk.Frame(main_content, bg='#34495e', width=250)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Users header
        users_header = tk.Frame(left_panel, bg='#2c3e50', height=40)
        users_header.pack(fill='x', padx=5, pady=5)
        users_header.pack_propagate(False)
        
        tk.Label(users_header, text="👥 Người dùng online",
                font=('Segoe UI', 12, 'bold'),
                fg='#ecf0f1', bg='#2c3e50').pack(pady=8)
        
        # Users list
        users_frame = tk.Frame(left_panel, bg='#34495e')
        users_frame.pack(fill='both', expand=True, padx=5, pady=(0, 5))
        
        self.users_listbox = tk.Listbox(users_frame,
                                       font=('Segoe UI', 11),
                                       bg='#ecf0f1', fg='#2c3e50',
                                       relief='flat', bd=0,
                                       selectbackground='#3498db',
                                       selectforeground='white',
                                       activestyle='none')
        self.users_listbox.pack(fill='both', expand=True)
        
        # Right panel - Chat area
        right_panel = tk.Frame(main_content, bg='#34495e')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Chat header
        chat_header = tk.Frame(right_panel, bg='#2c3e50', height=40)
        chat_header.pack(fill='x', padx=5, pady=5)
        chat_header.pack_propagate(False)
        
        tk.Label(chat_header, text="💬 Chat công khai",
                font=('Segoe UI', 12, 'bold'),
                fg='#ecf0f1', bg='#2c3e50').pack(pady=8)
        
        # Chat display area
        chat_display_frame = tk.Frame(right_panel, bg='#34495e')
        chat_display_frame.pack(fill='both', expand=True, padx=5, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(chat_display_frame,
                                                     font=('Segoe UI', 11),
                                                     bg='#ecf0f1', fg='#2c3e50',
                                                     relief='flat', bd=0,
                                                     state='disabled',
                                                     wrap='word')
        self.chat_display.pack(fill='both', expand=True)
        
        # Message input area
        input_frame = tk.Frame(right_panel, bg='#34495e', height=80)
        input_frame.pack(fill='x', padx=5, pady=(0, 5))
        input_frame.pack_propagate(False)
        
        # Message type selector
        type_frame = tk.Frame(input_frame, bg='#34495e')
        type_frame.pack(fill='x', pady=(5, 0))
        
        self.msg_type_var = tk.StringVar(value="public")
        
        public_radio = tk.Radiobutton(type_frame, text="🌐 Công khai",
                                     variable=self.msg_type_var, value="public",
                                     font=('Segoe UI', 10),
                                     fg='#ecf0f1', bg='#34495e',
                                     selectcolor='#3498db',
                                     activebackground='#34495e',
                                     activeforeground='#ecf0f1')
        public_radio.pack(side='left', padx=(0, 20))
        
        private_radio = tk.Radiobutton(type_frame, text="🔒 Riêng tư",
                                      variable=self.msg_type_var, value="private",
                                      font=('Segoe UI', 10),
                                      fg='#ecf0f1', bg='#34495e',
                                      selectcolor='#e74c3c',
                                      activebackground='#34495e',
                                      activeforeground='#ecf0f1')
        private_radio.pack(side='left')
        
        # Message input
        message_frame = tk.Frame(input_frame, bg='#34495e')
        message_frame.pack(fill='x', pady=(10, 5))
        
        self.message_entry = tk.Entry(message_frame,
                                     font=('Segoe UI', 12),
                                     bg='#ecf0f1', fg='#2c3e50',
                                     relief='flat', bd=0,
                                     highlightthickness=2,
                                     highlightcolor='#3498db')
        self.message_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        self.send_btn = tk.Button(message_frame, text="📤 Gửi",
                                 font=('Segoe UI', 11, 'bold'),
                                 bg='#3498db', fg='white',
                                 relief='flat', bd=0, cursor='hand2',
                                 command=self.send_message)
        self.send_btn.pack(side='right', padx=(10, 0), ipady=8, ipadx=15)
        
        # Bind Enter key
        self.message_entry.bind('<Return>', lambda e: self.send_message())

    def show_login_frame(self):
        """Show login frame"""
        if self.current_frame:
            self.current_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)
        self.current_frame = self.login_frame
        self.username_entry.focus()
        
    def show_chat_frame(self):
        """Show chat frame"""
        if self.current_frame:
            self.current_frame.pack_forget()
        self.chat_frame.pack(fill='both', expand=True)
        self.current_frame = self.chat_frame
        self.message_entry.focus()
        
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        server_ip = self.server_ip_entry.get().strip()
        server_port = self.server_port_entry.get().strip()
        
        if not username or not password:
            self.show_status("Vui lòng nhập đầy đủ thông tin!", "#e74c3c")
            return
            
        try:
            self.server_port = int(server_port)
            self.server_ip = server_ip
        except ValueError:
            self.show_status("Port không hợp lệ!", "#e74c3c")
            return
            
        self.show_status("Đang kết nối...", "#f39c12")
        self.login_btn.config(state='disabled')
        
        # Connect in separate thread
        threading.Thread(target=self._connect_and_login, 
                        args=(username, password), daemon=True).start()
        
    def _connect_and_login(self, username, password):
        """Connect to server and login"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            
            # Connect to server
            self.socket.connect((self.server_ip, self.server_port))
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Send login message
            login_msg = f"LOGIN|{username}|SERVER|{hashed_password}|{datetime.now()}"
            self.socket.send(login_msg.encode('utf-8'))
            
            # Wait for response
            response = self.socket.recv(1024).decode('utf-8')
            
            if response.startswith("LOGIN_OK"):
                self.connected = True
                self.username = username
                
                # Update UI in main thread
                self.root.after(0, self._login_success)
                
                # Start message listener
                threading.Thread(target=self._message_listener, daemon=True).start()
                
            else:
                self.root.after(0, lambda: self.show_status("Đăng nhập thất bại!", "#e74c3c"))
                self.root.after(0, lambda: self.login_btn.config(state='normal'))
                
        except Exception as e:
            self.root.after(0, lambda: self.show_status(f"Lỗi kết nối: {str(e)}", "#e74c3c"))
            self.root.after(0, lambda: self.login_btn.config(state='normal'))
            
    def _login_success(self):
        """Handle successful login"""
        self.welcome_label.config(text=f"Chào mừng, {self.username}!")
        self.show_chat_frame()
        self.add_system_message(f"Đã kết nối thành công với server!")
        
    def register(self):
        """Handle registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        server_ip = self.server_ip_entry.get().strip()
        server_port = self.server_port_entry.get().strip()
        
        if not username or not password:
            self.show_status("Vui lòng nhập đầy đủ thông tin!", "#e74c3c")
            return
            
        if len(password) < 6:
            self.show_status("Mật khẩu phải có ít nhất 6 ký tự!", "#e74c3c")
            return
            
        try:
            self.server_port = int(server_port)
            self.server_ip = server_ip
        except ValueError:
            self.show_status("Port không hợp lệ!", "#e74c3c")
            return
            
        self.show_status("Đang đăng ký...", "#f39c12")
        self.register_btn.config(state='disabled')
        
        # Register in separate thread
        threading.Thread(target=self._register_user, 
                        args=(username, password), daemon=True).start()
    
    def guest_login(self):
        """Handle guest login"""
        import random
        guest_name = f"Guest{random.randint(1000, 9999)}"
        guest_password = "guest123"
        
        # Auto fill and login
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, guest_name)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, guest_password)
        
        self.show_status(f"Đăng nhập với tên: {guest_name}", "#3498db")
        
        # Auto register and login
        threading.Thread(target=self._guest_register_and_login, 
                        args=(guest_name, guest_password), daemon=True).start()
    
    def _guest_register_and_login(self, username, password):
        """Register guest and auto login"""
        try:
            # First register
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.settimeout(10)
            temp_socket.connect((self.server_ip, self.server_port))
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            register_msg = f"REGISTER|{username}|SERVER|{hashed_password}|{datetime.now()}"
            temp_socket.send(register_msg.encode('utf-8'))
            
            response = temp_socket.recv(1024).decode('utf-8')
            temp_socket.close()
            
            # Then login
            if response.startswith("REGISTER_OK") or "already exists" in response.lower():
                self.root.after(100, lambda: self._connect_and_login(username, password))
            else:
                self.root.after(0, lambda: self.show_status("Lỗi đăng nhập khách!", "#e74c3c"))
                
        except Exception as e:
            self.root.after(0, lambda: self.show_status(f"Lỗi: {str(e)}", "#e74c3c"))
        
    def _register_user(self, username, password):
        """Register new user"""
        try:
            # Create socket
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.settimeout(10)
            
            # Connect to server
            temp_socket.connect((self.server_ip, self.server_port))
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Send register message
            register_msg = f"REGISTER|{username}|SERVER|{hashed_password}|{datetime.now()}"
            temp_socket.send(register_msg.encode('utf-8'))
            
            # Wait for response
            response = temp_socket.recv(1024).decode('utf-8')
            temp_socket.close()
            
            if response.startswith("REGISTER_OK"):
                self.root.after(0, lambda: self.show_status("Đăng ký thành công! Hãy đăng nhập.", "#27ae60"))
            else:
                self.root.after(0, lambda: self.show_status("Đăng ký thất bại! Tên đã tồn tại.", "#e74c3c"))
                
            self.root.after(0, lambda: self.register_btn.config(state='normal'))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_status(f"Lỗi kết nối: {str(e)}", "#e74c3c"))
            self.root.after(0, lambda: self.register_btn.config(state='normal'))

    def _message_listener(self):
        """Listen for messages from server"""
        while self.connected:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                # Parse message
                parts = message.split('|')
                if len(parts) >= 4:
                    msg_type = parts[0]
                    sender = parts[1]
                    receiver = parts[2]
                    content = parts[3]
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self._handle_received_message(
                        msg_type, sender, receiver, content))
                        
            except Exception as e:
                if self.connected:
                    self.root.after(0, lambda: self.add_system_message(f"Lỗi nhận tin: {str(e)}"))
                break
                
        self.connected = False
        
    def _handle_received_message(self, msg_type, sender, receiver, content):
        """Handle received message"""
        if msg_type == "PUBLIC":
            self.add_chat_message(sender, content, "public")
        elif msg_type == "PRIVATE":
            self.add_chat_message(sender, content, "private")
        elif msg_type == "USERLIST":
            self.update_user_list(content.split(',') if content else [])
        elif msg_type == "JOIN":
            self.add_system_message(f"{sender} đã tham gia phòng chat")
        elif msg_type == "LEAVE":
            self.add_system_message(f"{sender} đã rời khỏi phòng chat")
        elif msg_type == "ERROR":
            self.add_system_message(f"Lỗi: {content}")
            
    def send_message(self):
        """Send message"""
        if not self.connected:
            return
            
        message = self.message_entry.get().strip()
        if not message:
            return
            
        msg_type = self.msg_type_var.get()
        
        if msg_type == "private":
            # Get selected user
            selection = self.users_listbox.curselection()
            if not selection:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn người nhận tin nhắn riêng tư!")
                return
            receiver = self.users_listbox.get(selection[0])
        else:
            receiver = "ALL"
            
        try:
            # Send message to server
            msg = f"{msg_type.upper()}|{self.username}|{receiver}|{message}|{datetime.now()}"
            self.socket.send(msg.encode('utf-8'))
            
            # Clear input
            self.message_entry.delete(0, tk.END)
            
        except Exception as e:
            self.add_system_message(f"Lỗi gửi tin: {str(e)}")
            
    def add_chat_message(self, sender, content, msg_type):
        """Add message to chat display"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if msg_type == "public":
            if sender == self.username:
                self.chat_display.insert(tk.END, f"[{timestamp}] Bạn: {content}\n")
            else:
                self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {content}\n")
        else:  # private
            if sender == self.username:
                self.chat_display.insert(tk.END, f"[{timestamp}] Bạn (riêng tư): {content}\n")
            else:
                self.chat_display.insert(tk.END, f"[{timestamp}] {sender} (riêng tư): {content}\n")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
    def add_system_message(self, message):
        """Add system message"""
        self.chat_display.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] 🔔 {message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
    def update_user_list(self, users):
        """Update online users list"""
        self.users_listbox.delete(0, tk.END)
        self.online_users = [user for user in users if user and user != self.username]
        
        for user in self.online_users:
            self.users_listbox.insert(tk.END, f"🟢 {user}")
            
    def show_status(self, message, color):
        """Show status message"""
        self.status_label.config(text=message, fg=color)
        
    def disconnect(self):
        """Disconnect from server"""
        if self.connected:
            try:
                # Send leave message
                leave_msg = f"LEAVE|{self.username}|ALL|has left|{datetime.now()}"
                self.socket.send(leave_msg.encode('utf-8'))
                self.socket.close()
            except:
                pass
                
        self.connected = False
        self.socket = None
        self.username = ""
        
        # Clear forms
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="")
        self.login_btn.config(state='normal')
        self.register_btn.config(state='normal')
        
        # Show login frame
        self.show_login_frame()
        
    def on_closing(self):
        """Handle window closing"""
        if self.connected:
            self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    app = ChatClient()
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.root.mainloop()