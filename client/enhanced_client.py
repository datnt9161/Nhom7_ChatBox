#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatBox Client - Enhanced Version
Beautiful and modern chat client with advanced features
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import socket
import threading
import json
import hashlib
import os
from datetime import datetime
from styles import ModernStyles, IconHelper, AnimationHelper
from components import NotificationToast, LoadingSpinner, StatusBar

class EnhancedChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Network variables
        self.socket = None
        self.connected = False
        self.username = ""
        self.server_ip = "127.0.0.1"
        self.server_port = 5000
        
        # GUI variables
        self.current_frame = None
        self.online_users = []
        self.selected_user = None
        self.unread_messages = {}
        
        # Create main components
        self.create_status_bar()
        self.create_login_frame()
        self.create_chat_frame()
        
        # Show login frame first
        self.show_login_frame()
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_window(self):
        """Setup main window with modern design"""
        self.root.title("💬 ChatBox - Modern Chat Client")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.configure(bg=ModernStyles.COLORS['secondary'])
        
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
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side='bottom', fill='x')
    
    def create_login_frame(self):
        """Create enhanced login interface"""
        self.login_frame = tk.Frame(self.root, bg=ModernStyles.COLORS['secondary'])
        
        # Background gradient effect (simulated with frames)
        bg_frame = tk.Frame(self.login_frame, bg=ModernStyles.COLORS['secondary'])
        bg_frame.pack(fill='both', expand=True)
        
        # Main login container
        login_container = tk.Frame(bg_frame, bg=ModernStyles.COLORS['dark'], 
                                  relief='raised', bd=0)
        login_container.place(relx=0.5, rely=0.5, anchor='center', 
                             width=450, height=600)
        
        # Add subtle shadow effect
        shadow = tk.Frame(bg_frame, bg='#1a252f', relief='raised', bd=0)
        shadow.place(relx=0.5, rely=0.5, anchor='center', 
                    width=455, height=605)
        login_container.lift()
        
        # Header section
        header_frame = tk.Frame(login_container, bg=ModernStyles.COLORS['primary'], height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # App title with icon
        title_frame = tk.Frame(header_frame, bg=ModernStyles.COLORS['primary'])
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, text="💬", 
                font=('Segoe UI', 36),
                fg=ModernStyles.COLORS['white'], 
                bg=ModernStyles.COLORS['primary']).pack(pady=(20, 5))
        
        tk.Label(title_frame, text="ChatBox", 
                font=('Segoe UI', 24, 'bold'),
                fg=ModernStyles.COLORS['white'], 
                bg=ModernStyles.COLORS['primary']).pack()
        
        tk.Label(title_frame, text="Kết nối và trò chuyện", 
                font=('Segoe UI', 12),
                fg=ModernStyles.COLORS['light'], 
                bg=ModernStyles.COLORS['primary']).pack(pady=(0, 10))
        
        # Form section
        form_frame = tk.Frame(login_container, bg=ModernStyles.COLORS['dark'])
        form_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Username field
        self.create_input_field(form_frame, "👤 Tên đăng nhập", "username_entry")
        
        # Password field
        self.create_input_field(form_frame, "🔒 Mật khẩu", "password_entry", show="*")
        
        # Server settings (collapsible)
        self.create_server_settings(form_frame)
        
        # Action buttons
        self.create_login_buttons(form_frame)
        
        # Status message
        self.login_status_label = tk.Label(form_frame, text="",
                                          font=ModernStyles.FONTS['small'],
                                          bg=ModernStyles.COLORS['dark'])
        self.login_status_label.pack(pady=(15, 0))
        
        # Loading spinner (hidden initially)
        self.login_spinner = LoadingSpinner(form_frame, "Đang kết nối...",
                                           bg=ModernStyles.COLORS['dark'])
        
    def create_input_field(self, parent, label_text, attr_name, show=None):
        """Create a modern input field"""
        # Label
        tk.Label(parent, text=label_text,
                font=ModernStyles.FONTS['body'],
                fg=ModernStyles.COLORS['light'],
                bg=ModernStyles.COLORS['dark']).pack(anchor='w', pady=(15, 5))
        
        # Entry with modern styling
        entry = tk.Entry(parent,
                        font=ModernStyles.FONTS['input'],
                        bg=ModernStyles.COLORS['light'],
                        fg=ModernStyles.COLORS['black'],
                        relief='flat', bd=0,
                        highlightthickness=2,
                        highlightcolor=ModernStyles.COLORS['primary'],
                        show=show)
        entry.pack(fill='x', ipady=12)
        
        # Store reference
        setattr(self, attr_name, entry)
        
        # Add focus effects
        def on_focus_in(e):
            entry.config(highlightbackground=ModernStyles.COLORS['primary'])
        
        def on_focus_out(e):
            entry.config(highlightbackground=ModernStyles.COLORS['muted'])
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
    
    def create_server_settings(self, parent):
        """Create collapsible server settings"""
        # Server settings header
        server_header = tk.Frame(parent, bg=ModernStyles.COLORS['dark'])
        server_header.pack(fill='x', pady=(20, 10))
        
        self.server_expanded = tk.BooleanVar(value=False)
        
        server_toggle = tk.Checkbutton(server_header, 
                                      text="⚙️ Cài đặt server",
                                      variable=self.server_expanded,
                                      command=self.toggle_server_settings,
                                      font=ModernStyles.FONTS['body'],
                                      fg=ModernStyles.COLORS['muted'],
                                      bg=ModernStyles.COLORS['dark'],
                                      selectcolor=ModernStyles.COLORS['dark'],
                                      activebackground=ModernStyles.COLORS['dark'],
                                      activeforeground=ModernStyles.COLORS['light'])
        server_toggle.pack(anchor='w')
        
        # Server settings panel (hidden initially)
        self.server_panel = tk.Frame(parent, bg=ModernStyles.COLORS['dark'])
        
        # Server IP
        tk.Label(self.server_panel, text="🌐 Server IP:",
                font=ModernStyles.FONTS['small'],
                fg=ModernStyles.COLORS['muted'],
                bg=ModernStyles.COLORS['dark']).pack(anchor='w', pady=(5, 2))
        
        self.server_ip_entry = tk.Entry(self.server_panel,
                                       font=ModernStyles.FONTS['body'],
                                       bg=ModernStyles.COLORS['light'],
                                       fg=ModernStyles.COLORS['black'],
                                       relief='flat', bd=0)
        self.server_ip_entry.pack(fill='x', ipady=8, pady=(0, 10))
        self.server_ip_entry.insert(0, "127.0.0.1")
        
        # Server Port
        tk.Label(self.server_panel, text="🔌 Port:",
                font=ModernStyles.FONTS['small'],
                fg=ModernStyles.COLORS['muted'],
                bg=ModernStyles.COLORS['dark']).pack(anchor='w', pady=(0, 2))
        
        self.server_port_entry = tk.Entry(self.server_panel,
                                         font=ModernStyles.FONTS['body'],
                                         bg=ModernStyles.COLORS['light'],
                                         fg=ModernStyles.COLORS['black'],
                                         relief='flat', bd=0)
        self.server_port_entry.pack(fill='x', ipady=8)
        self.server_port_entry.insert(0, "5000")
    
    def toggle_server_settings(self):
        """Toggle server settings visibility"""
        if self.server_expanded.get():
            self.server_panel.pack(fill='x', pady=(0, 10))
        else:
            self.server_panel.pack_forget()
    
    def create_login_buttons(self, parent):
        """Create login action buttons"""
        button_frame = tk.Frame(parent, bg=ModernStyles.COLORS['dark'])
        button_frame.pack(fill='x', pady=(25, 0))
        
        # Login button
        self.login_btn = ModernStyles.create_modern_button(
            button_frame, "🔐 Đăng nhập", self.login, 'primary')
        self.login_btn.pack(fill='x', pady=(0, 12), ipady=12)
        
        # Register button
        self.register_btn = ModernStyles.create_modern_button(
            button_frame, "📝 Tạo tài khoản", self.register, 'success')
        self.register_btn.pack(fill='x', ipady=12)
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())    def crea
te_chat_frame(self):
        """Create enhanced chat interface"""
        self.chat_frame = tk.Frame(self.root, bg=ModernStyles.COLORS['secondary'])
        
        # Top header bar
        self.create_chat_header()
        
        # Main chat area
        main_container = tk.Frame(self.chat_frame, bg=ModernStyles.COLORS['secondary'])
        main_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Left sidebar - Users and controls
        self.create_sidebar(main_container)
        
        # Right area - Chat messages and input
        self.create_chat_area(main_container)
    
    def create_chat_header(self):
        """Create chat header with user info and controls"""
        header = tk.Frame(self.chat_frame, bg=ModernStyles.COLORS['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Left side - App info
        left_header = tk.Frame(header, bg=ModernStyles.COLORS['primary'])
        left_header.pack(side='left', fill='y', padx=20)
        
        tk.Label(left_header, text="💬 ChatBox",
                font=('Segoe UI', 20, 'bold'),
                fg=ModernStyles.COLORS['white'],
                bg=ModernStyles.COLORS['primary']).pack(anchor='w', pady=(15, 0))
        
        self.welcome_label = tk.Label(left_header, text="",
                                     font=ModernStyles.FONTS['body'],
                                     fg=ModernStyles.COLORS['light'],
                                     bg=ModernStyles.COLORS['primary'])
        self.welcome_label.pack(anchor='w', pady=(0, 15))
        
        # Right side - Controls
        right_header = tk.Frame(header, bg=ModernStyles.COLORS['primary'])
        right_header.pack(side='right', fill='y', padx=20)
        
        # Control buttons
        controls_frame = tk.Frame(right_header, bg=ModernStyles.COLORS['primary'])
        controls_frame.pack(pady=20)
        
        # Settings button
        settings_btn = tk.Button(controls_frame, text="⚙️",
                               font=ModernStyles.FONTS['heading'],
                               bg=ModernStyles.COLORS['primary'],
                               fg=ModernStyles.COLORS['white'],
                               relief='flat', bd=0, cursor='hand2',
                               command=self.show_settings)
        settings_btn.pack(side='left', padx=(0, 10))
        
        # Disconnect button
        disconnect_btn = tk.Button(controls_frame, text="🚪 Thoát",
                                  font=ModernStyles.FONTS['button'],
                                  bg=ModernStyles.COLORS['danger'],
                                  fg=ModernStyles.COLORS['white'],
                                  relief='flat', bd=0, cursor='hand2',
                                  command=self.disconnect)
        disconnect_btn.pack(side='left')
    
    def create_sidebar(self, parent):
        """Create left sidebar with users list"""
        sidebar = tk.Frame(parent, bg=ModernStyles.COLORS['dark'], width=280)
        sidebar.pack(side='left', fill='y', padx=(0, 15))
        sidebar.pack_propagate(False)
        
        # Users section header
        users_header = tk.Frame(sidebar, bg=ModernStyles.COLORS['secondary'], height=50)
        users_header.pack(fill='x', padx=10, pady=10)
        users_header.pack_propagate(False)
        
        tk.Label(users_header, text="👥 Người dùng online",
                font=ModernStyles.FONTS['heading'],
                fg=ModernStyles.COLORS['white'],
                bg=ModernStyles.COLORS['secondary']).pack(pady=12)
        
        # Users list with search
        search_frame = tk.Frame(sidebar, bg=ModernStyles.COLORS['dark'])
        search_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.user_search = tk.Entry(search_frame,
                                   font=ModernStyles.FONTS['body'],
                                   bg=ModernStyles.COLORS['light'],
                                   fg=ModernStyles.COLORS['black'],
                                   relief='flat', bd=0)
        self.user_search.pack(fill='x', ipady=8)
        self.user_search.insert(0, "🔍 Tìm kiếm người dùng...")
        self.user_search.bind('<FocusIn>', self.clear_search_placeholder)
        self.user_search.bind('<FocusOut>', self.restore_search_placeholder)
        self.user_search.bind('<KeyRelease>', self.filter_users)
        
        # Users list
        users_frame = tk.Frame(sidebar, bg=ModernStyles.COLORS['dark'])
        users_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollable users list
        self.users_canvas = tk.Canvas(users_frame, bg=ModernStyles.COLORS['light'],
                                     highlightthickness=0)
        self.users_scrollbar = ttk.Scrollbar(users_frame, orient="vertical",
                                           command=self.users_canvas.yview)
        self.users_scrollable_frame = tk.Frame(self.users_canvas, bg=ModernStyles.COLORS['light'])
        
        self.users_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.users_canvas.configure(scrollregion=self.users_canvas.bbox("all"))
        )
        
        self.users_canvas.create_window((0, 0), window=self.users_scrollable_frame, anchor="nw")
        self.users_canvas.configure(yscrollcommand=self.users_scrollbar.set)
        
        self.users_canvas.pack(side="left", fill="both", expand=True)
        self.users_scrollbar.pack(side="right", fill="y")
        
        # Chat type selector
        chat_type_frame = tk.Frame(sidebar, bg=ModernStyles.COLORS['secondary'], height=60)
        chat_type_frame.pack(fill='x', padx=10, pady=(0, 10))
        chat_type_frame.pack_propagate(False)
        
        tk.Label(chat_type_frame, text="💬 Loại tin nhắn",
                font=ModernStyles.FONTS['body'],
                fg=ModernStyles.COLORS['white'],
                bg=ModernStyles.COLORS['secondary']).pack(pady=(8, 2))
        
        type_buttons_frame = tk.Frame(chat_type_frame, bg=ModernStyles.COLORS['secondary'])
        type_buttons_frame.pack()
        
        self.msg_type_var = tk.StringVar(value="public")
        
        public_btn = tk.Radiobutton(type_buttons_frame, text="🌐 Công khai",
                                   variable=self.msg_type_var, value="public",
                                   font=ModernStyles.FONTS['small'],
                                   fg=ModernStyles.COLORS['white'],
                                   bg=ModernStyles.COLORS['secondary'],
                                   selectcolor=ModernStyles.COLORS['primary'],
                                   activebackground=ModernStyles.COLORS['secondary'])
        public_btn.pack(side='left', padx=(0, 15))
        
        private_btn = tk.Radiobutton(type_buttons_frame, text="🔒 Riêng tư",
                                    variable=self.msg_type_var, value="private",
                                    font=ModernStyles.FONTS['small'],
                                    fg=ModernStyles.COLORS['white'],
                                    bg=ModernStyles.COLORS['secondary'],
                                    selectcolor=ModernStyles.COLORS['danger'],
                                    activebackground=ModernStyles.COLORS['secondary'])
        private_btn.pack(side='left')
    
    def create_chat_area(self, parent):
        """Create main chat area"""
        chat_container = tk.Frame(parent, bg=ModernStyles.COLORS['dark'])
        chat_container.pack(side='right', fill='both', expand=True)
        
        # Chat header
        chat_header = tk.Frame(chat_container, bg=ModernStyles.COLORS['secondary'], height=50)
        chat_header.pack(fill='x', padx=10, pady=10)
        chat_header.pack_propagate(False)
        
        self.chat_title_label = tk.Label(chat_header, text="💬 Chat công khai",
                                        font=ModernStyles.FONTS['heading'],
                                        fg=ModernStyles.COLORS['white'],
                                        bg=ModernStyles.COLORS['secondary'])
        self.chat_title_label.pack(pady=12)
        
        # Messages area
        messages_frame = tk.Frame(chat_container, bg=ModernStyles.COLORS['dark'])
        messages_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Chat display with custom styling
        self.chat_display = scrolledtext.ScrolledText(
            messages_frame,
            font=ModernStyles.FONTS['body'],
            bg=ModernStyles.COLORS['light'],
            fg=ModernStyles.COLORS['black'],
            relief='flat', bd=0,
            state='disabled',
            wrap='word',
            padx=15, pady=15
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Apply text tags for different message types
        ModernStyles.apply_chat_text_tags(self.chat_display)
        
        # Message input area
        self.create_message_input(chat_container)
    
    def create_message_input(self, parent):
        """Create message input area with modern design"""
        input_container = tk.Frame(parent, bg=ModernStyles.COLORS['dark'])
        input_container.pack(fill='x', padx=10, pady=(0, 10))
        
        # Input frame with rounded appearance
        input_frame = tk.Frame(input_container, bg=ModernStyles.COLORS['light'],
                              relief='raised', bd=1)
        input_frame.pack(fill='x', pady=5)
        
        # Message entry
        self.message_entry = tk.Entry(input_frame,
                                     font=ModernStyles.FONTS['input'],
                                     bg=ModernStyles.COLORS['light'],
                                     fg=ModernStyles.COLORS['black'],
                                     relief='flat', bd=0,
                                     highlightthickness=0)
        self.message_entry.pack(side='left', fill='x', expand=True, 
                               padx=15, pady=12)
        
        # Action buttons
        buttons_frame = tk.Frame(input_frame, bg=ModernStyles.COLORS['light'])
        buttons_frame.pack(side='right', padx=10, pady=8)
        
        # File attachment button
        file_btn = tk.Button(buttons_frame, text="📎",
                           font=ModernStyles.FONTS['heading'],
                           bg=ModernStyles.COLORS['light'],
                           fg=ModernStyles.COLORS['muted'],
                           relief='flat', bd=0, cursor='hand2',
                           command=self.attach_file)
        file_btn.pack(side='left', padx=(0, 8))
        
        # Emoji button
        emoji_btn = tk.Button(buttons_frame, text="😊",
                            font=ModernStyles.FONTS['heading'],
                            bg=ModernStyles.COLORS['light'],
                            fg=ModernStyles.COLORS['muted'],
                            relief='flat', bd=0, cursor='hand2',
                            command=self.show_emoji_picker)
        emoji_btn.pack(side='left', padx=(0, 8))
        
        # Send button
        self.send_btn = tk.Button(buttons_frame, text="📤",
                                 font=ModernStyles.FONTS['heading'],
                                 bg=ModernStyles.COLORS['primary'],
                                 fg=ModernStyles.COLORS['white'],
                                 relief='flat', bd=0, cursor='hand2',
                                 command=self.send_message)
        self.send_btn.pack(side='left')
        
        # Bind Enter key
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        self.message_entry.bind('<KeyRelease>', self.on_typing)    # UI H
elper Methods
    def show_login_frame(self):
        """Show login frame"""
        if self.current_frame:
            self.current_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)
        self.current_frame = self.login_frame
        self.username_entry.focus()
        self.status_bar.set_connection_status(False)
    
    def show_chat_frame(self):
        """Show chat frame"""
        if self.current_frame:
            self.current_frame.pack_forget()
        self.chat_frame.pack(fill='both', expand=True)
        self.current_frame = self.chat_frame
        self.message_entry.focus()
        self.status_bar.set_connection_status(True)
    
    def clear_search_placeholder(self, event):
        """Clear search placeholder text"""
        if self.user_search.get() == "🔍 Tìm kiếm người dùng...":
            self.user_search.delete(0, tk.END)
            self.user_search.config(fg=ModernStyles.COLORS['black'])
    
    def restore_search_placeholder(self, event):
        """Restore search placeholder text"""
        if not self.user_search.get():
            self.user_search.insert(0, "🔍 Tìm kiếm người dùng...")
            self.user_search.config(fg=ModernStyles.COLORS['muted'])
    
    def filter_users(self, event):
        """Filter users based on search"""
        search_term = self.user_search.get().lower()
        if search_term == "🔍 tìm kiếm người dùng...":
            return
        
        # Clear current user list
        for widget in self.users_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Show filtered users
        filtered_users = [user for user in self.online_users 
                         if search_term in user.lower()]
        self.display_users(filtered_users)
    
    def display_users(self, users):
        """Display users in the list"""
        for i, user in enumerate(users):
            user_frame = tk.Frame(self.users_scrollable_frame, 
                                 bg=ModernStyles.COLORS['light'],
                                 cursor='hand2')
            user_frame.pack(fill='x', padx=5, pady=2)
            
            # User info
            info_frame = tk.Frame(user_frame, bg=ModernStyles.COLORS['light'])
            info_frame.pack(fill='x', padx=10, pady=8)
            
            # Status indicator
            status_label = tk.Label(info_frame, text="🟢",
                                   font=ModernStyles.FONTS['body'],
                                   bg=ModernStyles.COLORS['light'])
            status_label.pack(side='left', padx=(0, 8))
            
            # Username
            username_label = tk.Label(info_frame, text=user,
                                     font=ModernStyles.FONTS['body'],
                                     fg=ModernStyles.COLORS['black'],
                                     bg=ModernStyles.COLORS['light'])
            username_label.pack(side='left', fill='x', expand=True)
            
            # Unread indicator
            if user in self.unread_messages and self.unread_messages[user] > 0:
                unread_label = tk.Label(info_frame, 
                                       text=str(self.unread_messages[user]),
                                       font=('Segoe UI', 9, 'bold'),
                                       fg=ModernStyles.COLORS['white'],
                                       bg=ModernStyles.COLORS['danger'],
                                       width=3, height=1)
                unread_label.pack(side='right')
            
            # Click handler
            def on_user_click(username=user):
                self.select_user(username)
            
            # Hover effects
            def on_enter(e, frame=user_frame):
                frame.config(bg=ModernStyles.COLORS['primary'])
                for child in frame.winfo_children():
                    self.update_widget_bg(child, ModernStyles.COLORS['primary'])
            
            def on_leave(e, frame=user_frame):
                frame.config(bg=ModernStyles.COLORS['light'])
                for child in frame.winfo_children():
                    self.update_widget_bg(child, ModernStyles.COLORS['light'])
            
            user_frame.bind("<Button-1>", lambda e, u=user: on_user_click(u))
            user_frame.bind("<Enter>", on_enter)
            user_frame.bind("<Leave>", on_leave)
            
            # Bind events to child widgets too
            for child in user_frame.winfo_children():
                self.bind_user_events(child, on_user_click, on_enter, on_leave, user)
    
    def bind_user_events(self, widget, click_handler, enter_handler, leave_handler, user):
        """Bind events to user widget and its children"""
        widget.bind("<Button-1>", lambda e: click_handler(user))
        widget.bind("<Enter>", enter_handler)
        widget.bind("<Leave>", leave_handler)
        
        for child in widget.winfo_children():
            self.bind_user_events(child, click_handler, enter_handler, leave_handler, user)
    
    def update_widget_bg(self, widget, color):
        """Recursively update widget background"""
        try:
            widget.config(bg=color)
            if color == ModernStyles.COLORS['primary']:
                widget.config(fg=ModernStyles.COLORS['white'])
            else:
                widget.config(fg=ModernStyles.COLORS['black'])
        except:
            pass
        
        for child in widget.winfo_children():
            self.update_widget_bg(child, color)
    
    def select_user(self, username):
        """Select a user for private chat"""
        self.selected_user = username
        self.msg_type_var.set("private")
        self.chat_title_label.config(text=f"🔒 Chat riêng với {username}")
        
        # Mark messages as read
        if username in self.unread_messages:
            self.unread_messages[username] = 0
            self.display_users(self.online_users)
        
        # Show notification
        NotificationToast(self.root, f"Đã chọn chat riêng với {username}", "info", 2000)
    
    # Network Methods
    def login(self):
        """Handle login with enhanced UI feedback"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_login_status("Vui lòng nhập đầy đủ thông tin!", "error")
            return
        
        # Get server settings if expanded
        if self.server_expanded.get():
            try:
                self.server_ip = self.server_ip_entry.get().strip()
                self.server_port = int(self.server_port_entry.get().strip())
            except ValueError:
                self.show_login_status("Port không hợp lệ!", "error")
                return
        
        # Show loading
        self.show_login_loading(True)
        self.show_login_status("Đang kết nối đến server...", "info")
        
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
                self.root.after(0, lambda: self.show_login_status("Đăng nhập thất bại! Kiểm tra lại thông tin.", "error"))
                self.root.after(0, lambda: self.show_login_loading(False))
                
        except Exception as e:
            error_msg = f"Lỗi kết nối: {str(e)}"
            self.root.after(0, lambda: self.show_login_status(error_msg, "error"))
            self.root.after(0, lambda: self.show_login_loading(False))
    
    def _login_success(self):
        """Handle successful login"""
        self.show_login_loading(False)
        self.welcome_label.config(text=f"Chào mừng, {self.username}! 👋")
        self.show_chat_frame()
        self.add_system_message("🎉 Đã kết nối thành công với server!")
        self.status_bar.set_status("Đã kết nối", "success")
        
        # Show success notification
        NotificationToast(self.root, f"Chào mừng {self.username}!", "success")
    
    def register(self):
        """Handle registration with validation"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_login_status("Vui lòng nhập đầy đủ thông tin!", "error")
            return
        
        if len(username) < 3:
            self.show_login_status("Tên đăng nhập phải có ít nhất 3 ký tự!", "error")
            return
        
        if len(password) < 6:
            self.show_login_status("Mật khẩu phải có ít nhất 6 ký tự!", "error")
            return
        
        # Get server settings if expanded
        if self.server_expanded.get():
            try:
                self.server_ip = self.server_ip_entry.get().strip()
                self.server_port = int(self.server_port_entry.get().strip())
            except ValueError:
                self.show_login_status("Port không hợp lệ!", "error")
                return
        
        # Show loading
        self.show_login_loading(True)
        self.show_login_status("Đang tạo tài khoản...", "info")
        
        # Register in separate thread
        threading.Thread(target=self._register_user, 
                        args=(username, password), daemon=True).start()
    
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
                self.root.after(0, lambda: self.show_login_status("✅ Đăng ký thành công! Hãy đăng nhập.", "success"))
                self.root.after(0, lambda: NotificationToast(self.root, "Tài khoản đã được tạo thành công!", "success"))
            else:
                self.root.after(0, lambda: self.show_login_status("❌ Đăng ký thất bại! Tên đã tồn tại.", "error"))
                
            self.root.after(0, lambda: self.show_login_loading(False))
            
        except Exception as e:
            error_msg = f"Lỗi kết nối: {str(e)}"
            self.root.after(0, lambda: self.show_login_status(error_msg, "error"))
            self.root.after(0, lambda: self.show_login_loading(False))
    
    def show_login_status(self, message, status_type):
        """Show login status message"""
        colors = {
            'info': ModernStyles.COLORS['info'],
            'success': ModernStyles.COLORS['success'],
            'error': ModernStyles.COLORS['danger'],
            'warning': ModernStyles.COLORS['warning']
        }
        
        color = colors.get(status_type, colors['info'])
        self.login_status_label.config(text=message, fg=color)
    
    def show_login_loading(self, show):
        """Show/hide login loading spinner"""
        if show:
            self.login_btn.config(state='disabled')
            self.register_btn.config(state='disabled')
            self.login_spinner.pack(pady=10)
            self.login_spinner.start()
        else:
            self.login_btn.config(state='normal')
            self.register_btn.config(state='normal')
            self.login_spinner.pack_forget()
            self.login_spinner.stop()   
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
                    self.root.after(0, lambda: self.add_system_message(f"❌ Lỗi nhận tin: {str(e)}"))
                break
        
        self.connected = False
    
    def _handle_received_message(self, msg_type, sender, receiver, content):
        """Handle received message with enhanced features"""
        if msg_type == "PUBLIC":
            self.add_chat_message(sender, content, "public")
        elif msg_type == "PRIVATE":
            self.add_chat_message(sender, content, "private")
            # Update unread count if not current chat
            if sender != self.selected_user:
                self.unread_messages[sender] = self.unread_messages.get(sender, 0) + 1
                self.display_users(self.online_users)
        elif msg_type == "USERLIST":
            users = content.split(',') if content else []
            self.update_user_list(users)
        elif msg_type == "JOIN":
            self.add_system_message(f"👋 {sender} đã tham gia phòng chat")
            NotificationToast(self.root, f"{sender} đã tham gia", "info", 2000)
        elif msg_type == "LEAVE":
            self.add_system_message(f"👋 {sender} đã rời khỏi phòng chat")
        elif msg_type == "ERROR":
            self.add_system_message(f"❌ Lỗi: {content}")
            NotificationToast(self.root, f"Lỗi: {content}", "error")
    
    def send_message(self):
        """Send message with enhanced validation"""
        if not self.connected:
            NotificationToast(self.root, "Chưa kết nối đến server!", "error")
            return
        
        message = self.message_entry.get().strip()
        if not message:
            return
        
        msg_type = self.msg_type_var.get()
        
        if msg_type == "private":
            if not self.selected_user:
                NotificationToast(self.root, "Vui lòng chọn người nhận tin nhắn riêng tư!", "warning")
                return
            receiver = self.selected_user
        else:
            receiver = "ALL"
            self.chat_title_label.config(text="💬 Chat công khai")
        
        try:
            # Send message to server
            msg = f"{msg_type.upper()}|{self.username}|{receiver}|{message}|{datetime.now()}"
            self.socket.send(msg.encode('utf-8'))
            
            # Clear input
            self.message_entry.delete(0, tk.END)
            
            # Add bounce effect to send button
            AnimationHelper.bounce_button(self.send_btn)
            
        except Exception as e:
            self.add_system_message(f"❌ Lỗi gửi tin: {str(e)}")
            NotificationToast(self.root, f"Lỗi gửi tin: {str(e)}", "error")
    
    def add_chat_message(self, sender, content, msg_type):
        """Add message to chat display with enhanced formatting"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Message prefix with emoji
        if msg_type == "public":
            if sender == self.username:
                prefix = f"[{timestamp}] 🗣️ Bạn: "
                tag = "own_message"
            else:
                prefix = f"[{timestamp}] 👤 {sender}: "
                tag = "other_message"
        else:  # private
            if sender == self.username:
                prefix = f"[{timestamp}] 🔒 Bạn (riêng tư): "
                tag = "private_own"
            else:
                prefix = f"[{timestamp}] 🔒 {sender} (riêng tư): "
                tag = "private_other"
        
        # Insert message
        self.chat_display.insert(tk.END, prefix, tag)
        self.chat_display.insert(tk.END, f"{content}\n", tag)
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        # Play notification sound (if available)
        if sender != self.username:
            self.play_notification_sound()
    
    def add_system_message(self, message):
        """Add system message with timestamp"""
        self.chat_display.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {message}\n", "system")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def update_user_list(self, users):
        """Update online users list"""
        self.online_users = [user for user in users if user and user != self.username]
        self.display_users(self.online_users)
        
        # Update status
        user_count = len(self.online_users)
        self.status_bar.set_status(f"Online: {user_count} người dùng", "info")
    
    def play_notification_sound(self):
        """Play notification sound (placeholder)"""
        # Could implement actual sound playing here
        pass
    
    def on_typing(self, event):
        """Handle typing indicator"""
        # Could implement typing indicator here
        pass
    
    def attach_file(self):
        """Handle file attachment"""
        file_path = filedialog.askopenfilename(
            title="Chọn file để gửi",
            filetypes=[
                ("Tất cả files", "*.*"),
                ("Hình ảnh", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Tài liệu", "*.pdf *.doc *.docx *.txt"),
                ("Video", "*.mp4 *.avi *.mov *.wmv")
            ]
        )
        
        if file_path:
            # For now, just show the filename in chat
            filename = os.path.basename(file_path)
            self.message_entry.insert(tk.END, f"📎 {filename}")
            NotificationToast(self.root, f"Đã chọn file: {filename}", "info", 2000)
    
    def show_emoji_picker(self):
        """Show emoji picker (simplified)"""
        emojis = ["😊", "😂", "❤️", "👍", "👎", "😢", "😮", "😡", "🎉", "🔥"]
        
        # Create popup window
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("Chọn emoji")
        emoji_window.geometry("300x100")
        emoji_window.resizable(False, False)
        emoji_window.configure(bg=ModernStyles.COLORS['dark'])
        
        # Center the window
        emoji_window.transient(self.root)
        emoji_window.grab_set()
        
        # Emoji buttons
        emoji_frame = tk.Frame(emoji_window, bg=ModernStyles.COLORS['dark'])
        emoji_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        for i, emoji in enumerate(emojis):
            btn = tk.Button(emoji_frame, text=emoji,
                           font=('Segoe UI', 16),
                           bg=ModernStyles.COLORS['light'],
                           relief='flat', bd=0, cursor='hand2',
                           command=lambda e=emoji: self.insert_emoji(e, emoji_window))
            btn.grid(row=i//5, column=i%5, padx=2, pady=2, sticky='nsew')
        
        # Configure grid weights
        for i in range(5):
            emoji_frame.columnconfigure(i, weight=1)
        for i in range(2):
            emoji_frame.rowconfigure(i, weight=1)
    
    def insert_emoji(self, emoji, window):
        """Insert emoji into message entry"""
        self.message_entry.insert(tk.END, emoji)
        window.destroy()
        self.message_entry.focus()
    
    def show_settings(self):
        """Show settings dialog"""
        NotificationToast(self.root, "Cài đặt sẽ được thêm trong phiên bản sau!", "info")
    
    def disconnect(self):
        """Disconnect from server with confirmation"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát khỏi chat?"):
            self._perform_disconnect()
    
    def _perform_disconnect(self):
        """Perform actual disconnection"""
        if self.connected:
            try:
                # Send leave message
                leave_msg = f"LEAVE|{self.username}|ALL|has left|{datetime.now()}"
                self.socket.send(leave_msg.encode('utf-8'))
                self.socket.close()
            except:
                pass
        
        # Reset state
        self.connected = False
        self.socket = None
        self.username = ""
        self.selected_user = None
        self.unread_messages.clear()
        
        # Clear forms
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.login_status_label.config(text="")
        self.show_login_loading(False)
        
        # Clear chat
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        
        # Show login frame
        self.show_login_frame()
        self.status_bar.set_status("Đã ngắt kết nối", "warning")
        
        NotificationToast(self.root, "Đã ngắt kết nối khỏi server", "info")
    
    def on_closing(self):
        """Handle window closing"""
        if self.connected:
            if messagebox.askyesno("Xác nhận thoát", "Bạn đang trong phiên chat. Có chắc muốn thoát?"):
                self._perform_disconnect()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Main function to run the application"""
    app = EnhancedChatClient()
    app.root.mainloop()

if __name__ == "__main__":
    main()