#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Chat Page - Material Design 3 + Glassmorphism
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import socket
from datetime import datetime
import math
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from modern_styles import ModernColors, ModernFonts, ModernWidgets, ModernAnimations

class ModernChatPage:
    def __init__(self, root, username, socket_conn, on_disconnect):
        self.root = root
        self.username = username
        self.socket = socket_conn
        self.on_disconnect = on_disconnect
        
        # Chat variables
        self.connected = True
        self.online_users = []
        self.selected_user = None
        self.unread_messages = {}
        self.msg_type_var = tk.StringVar(value="public")
        
        # Animation variables
        self.animation_step = 0
        
        # UI initialization flag
        self._ui_initialized = False
        
        self.create_modern_ui()
        
        # Start message listener
        threading.Thread(target=self._message_listener, daemon=True).start()
    
    def create_modern_ui(self):
        """Create ultra-modern chat interface"""
        self.main_frame = tk.Frame(self.root, bg=ModernColors.GRAY_50)
        
        # Create animated header
        self.create_modern_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create modern status bar
        self.create_modern_status_bar()
        
        # Mark UI as initialized
        self._ui_initialized = True
        
        # Start animations
        self.animate_interface()
    
    def create_modern_header(self):
        """Create modern animated header"""
        # Header with gradient background
        self.header_canvas = tk.Canvas(
            self.main_frame,
            height=100,
            highlightthickness=0,
            bg=ModernColors.PRIMARY
        )
        self.header_canvas.pack(fill='x')
        
        # Header content frame
        header_content = tk.Frame(self.header_canvas, bg=ModernColors.PRIMARY)
        self.header_canvas.create_window(0, 0, window=header_content, anchor='nw')
        
        # Left side - App branding
        left_frame = tk.Frame(header_content, bg=ModernColors.PRIMARY)
        left_frame.pack(side='left', fill='y', padx=30, pady=20)
        
        # Animated logo
        self.logo_label = tk.Label(
            left_frame,
            text="💬",
            font=('Segoe UI', 32),
            fg=ModernColors.WHITE,
            bg=ModernColors.PRIMARY
        )
        self.logo_label.pack(side='left')
        
        # App title and user info
        title_frame = tk.Frame(left_frame, bg=ModernColors.PRIMARY)
        title_frame.pack(side='left', padx=(15, 0))
        
        tk.Label(
            title_frame,
            text="ChatBox",
            font=ModernFonts.HEADLINE_LARGE,
            fg=ModernColors.WHITE,
            bg=ModernColors.PRIMARY
        ).pack(anchor='w')
        
        self.user_label = tk.Label(
            title_frame,
            text=f"Welcome back, {self.username}! ✨",
            font=ModernFonts.BODY_MEDIUM,
            fg=ModernColors.GRAY_100,
            bg=ModernColors.PRIMARY
        )
        self.user_label.pack(anchor='w')
        
        # Right side - Controls
        right_frame = tk.Frame(header_content, bg=ModernColors.PRIMARY)
        right_frame.pack(side='right', fill='y', padx=30, pady=20)
        
        # Control buttons - CHỈ CÒN LOGOUT
        controls_frame = tk.Frame(right_frame, bg=ModernColors.PRIMARY)
        controls_frame.pack(side='right')
        
        # Logout button
        logout_btn = tk.Button(
            controls_frame,
            text="Logout",
            font=ModernFonts.BODY_MEDIUM,
            bg=ModernColors.ERROR,
            fg=ModernColors.WHITE,
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.handle_logout
        )
        logout_btn.pack(side='left')
        
        # Add hover effect
        ModernAnimations.button_hover_effect(
            logout_btn, ModernColors.ERROR, '#dc2626'
        )
        
        # Update header canvas size
        def update_header_size(event=None):
            self.header_canvas.configure(scrollregion=self.header_canvas.bbox("all"))
            canvas_width = self.header_canvas.winfo_width()
            if self.header_canvas.find_all():
                self.header_canvas.itemconfig(
                    self.header_canvas.find_all()[0],
                    width=canvas_width
                )
        
        self.header_canvas.bind('<Configure>', update_header_size)
        self.root.after(100, update_header_size)
    
    def create_header_button(self, parent, icon, tooltip, command):
        """Create modern header button"""
        btn = tk.Button(
            parent,
            text=icon,
            font=('Segoe UI', 18),
            bg=ModernColors.PRIMARY_LIGHT,
            fg=ModernColors.WHITE,
            relief='flat',
            bd=0,
            cursor='hand2',
            width=3,
            height=1,
            command=command
        )
        
        # Add hover effect
        ModernAnimations.button_hover_effect(
            btn, ModernColors.PRIMARY_LIGHT, ModernColors.PRIMARY_DARK
        )
        
        return btn
    
    def create_main_content(self):
        """Create main content area with sidebar and chat"""
        content_frame = tk.Frame(self.main_frame, bg=ModernColors.GRAY_50)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left sidebar - Users and controls
        self.create_modern_sidebar(content_frame)
        
        # Right area - Chat interface
        self.create_modern_chat_area(content_frame)
    
    def create_modern_sidebar(self, parent):
        """Create modern sidebar with glassmorphism effect"""
        # Sidebar container
        sidebar_container = tk.Frame(parent, bg=ModernColors.GRAY_50)
        sidebar_container.pack(side='left', fill='y', padx=(0, 20))
        
        # Glassmorphism sidebar
        self.sidebar = tk.Frame(
            sidebar_container,
            bg=ModernColors.WHITE,
            relief='flat',
            bd=0,
            width=350
        )
        self.sidebar.pack(fill='y', expand=True)
        self.sidebar.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Frame(self.sidebar, bg=ModernColors.GRAY_50, height=70)
        sidebar_header.pack(fill='x')
        sidebar_header.pack_propagate(False)
        
        tk.Label(
            sidebar_header,
            text="👥 Online Users",
            font=('Segoe UI', 18, 'bold'),
            fg=ModernColors.GRAY_900,
            bg=ModernColors.GRAY_50
        ).pack(pady=20)
        
        # Search box - TẠO RIÊNG ĐỂ KIỂM SOÁT TỐT HƠN
        search_frame = tk.Frame(self.sidebar, bg=ModernColors.WHITE)
        search_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Search label
        search_label = tk.Label(
            search_frame,
            text="🔍 Search Users",
            font=('Segoe UI', 12, 'bold'),
            fg=ModernColors.GRAY_700,
            bg=ModernColors.WHITE
        )
        search_label.pack(anchor='w', pady=(0, 5))
        
        # Search entry container
        search_container = tk.Frame(search_frame, bg=ModernColors.GRAY_50, relief='flat', bd=1)
        search_container.pack(fill='x')
        
        # Search entry
        self.search_entry = tk.Entry(
            search_container,
            font=('Segoe UI', 12, 'normal'),
            bg=ModernColors.GRAY_50,
            fg=ModernColors.GRAY_900,
            relief='flat',
            bd=0,
            insertbackground=ModernColors.PRIMARY
        )
        self.search_entry.pack(fill='x', padx=10, pady=8)  # Padding để text không sát lề
        
        # Placeholder effect
        placeholder_text = "Type username to search..."
        self.search_entry.insert(0, placeholder_text)
        self.search_entry.config(fg=ModernColors.GRAY_500)
        
        def on_search_focus_in(e):
            if self.search_entry.get() == placeholder_text:
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg=ModernColors.GRAY_900)
        
        def on_search_focus_out(e):
            if not self.search_entry.get():
                self.search_entry.insert(0, placeholder_text)
                self.search_entry.config(fg=ModernColors.GRAY_500)
        
        def on_search_key_press(e):
            if self.search_entry.get() == placeholder_text:
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg=ModernColors.GRAY_900)
            # Ngăn focus nhảy sang message entry
            return "break"
        
        def on_search_key_release(e):
            # Xử lý search và giữ focus trong search box
            self.on_search_users(e)
            # Đảm bảo focus vẫn ở search box
            if e.widget == self.search_entry:
                self.search_entry.focus_set()
            return "break"
        
        self.search_entry.bind('<FocusIn>', on_search_focus_in)
        self.search_entry.bind('<FocusOut>', on_search_focus_out)
        self.search_entry.bind('<KeyPress>', on_search_key_press)
        
        # Bind search event với improved handling
        self.search_entry.bind('<KeyRelease>', on_search_key_release)
        
        # Users list
        users_frame = tk.Frame(self.sidebar, bg=ModernColors.WHITE)
        users_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Scrollable users list
        self.users_canvas = tk.Canvas(
            users_frame,
            bg=ModernColors.WHITE,
            highlightthickness=0
        )
        self.users_scrollbar = ttk.Scrollbar(
            users_frame,
            orient="vertical",
            command=self.users_canvas.yview
        )
        self.users_scrollable_frame = tk.Frame(self.users_canvas, bg=ModernColors.WHITE)
        
        self.users_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.users_canvas.configure(
                scrollregion=self.users_canvas.bbox("all")
            )
        )
        
        self.users_canvas.create_window(
            (0, 0), window=self.users_scrollable_frame, anchor="nw"
        )
        self.users_canvas.configure(yscrollcommand=self.users_scrollbar.set)
        
        self.users_canvas.pack(side="left", fill="both", expand=True)
        self.users_scrollbar.pack(side="right", fill="y")
        
        # Chat type selector với custom design
        self.create_chat_type_selector()
    
    def create_chat_type_selector(self):
        """Create custom radio button selector for chat type"""
        type_frame = tk.Frame(self.sidebar, bg=ModernColors.WHITE, height=100)
        type_frame.pack(fill='x')
        type_frame.pack_propagate(False)
        
        tk.Label(
            type_frame,
            text="Message Type",
            font=('Segoe UI', 16, 'bold'),
            fg=ModernColors.GRAY_900,
            bg=ModernColors.WHITE
        ).pack(pady=(20, 15))
        
        # Container cho custom radio buttons
        radio_container = tk.Frame(type_frame, bg=ModernColors.WHITE)
        radio_container.pack()
        
        # Public option
        public_frame = tk.Frame(radio_container, bg=ModernColors.WHITE)
        public_frame.pack(side='left', padx=(0, 40))
        
        # Custom radio button cho Public
        self.public_dot = tk.Label(
            public_frame,
            text="●",
            font=('Segoe UI', 20),
            fg=ModernColors.PRIMARY,  # Màu xanh khi được chọn
            bg=ModernColors.WHITE,
            cursor='hand2'
        )
        self.public_dot.pack(side='left', padx=(0, 8))
        
        public_label = tk.Label(
            public_frame,
            text="Public",
            font=('Segoe UI', 14, 'bold'),
            fg=ModernColors.GRAY_900,
            bg=ModernColors.WHITE,
            cursor='hand2'
        )
        public_label.pack(side='left')
        
        # Private option
        private_frame = tk.Frame(radio_container, bg=ModernColors.WHITE)
        private_frame.pack(side='left')
        
        # Custom radio button cho Private
        self.private_dot = tk.Label(
            private_frame,
            text="●",
            font=('Segoe UI', 20),
            fg=ModernColors.GRAY_300,  # Màu xám khi không được chọn
            bg=ModernColors.WHITE,
            cursor='hand2'
        )
        self.private_dot.pack(side='left', padx=(0, 8))
        
        private_label = tk.Label(
            private_frame,
            text="Private",
            font=('Segoe UI', 14, 'bold'),
            fg=ModernColors.GRAY_900,
            bg=ModernColors.WHITE,
            cursor='hand2'
        )
        private_label.pack(side='left')
        
        # Store references for event binding
        self.public_frame = public_frame
        self.private_frame = private_frame
        self.public_label = public_label
        self.private_label = private_label
        
        # Bind events
        self.public_dot.bind('<Button-1>', lambda e: self.select_public())
        public_label.bind('<Button-1>', lambda e: self.select_public())
        public_frame.bind('<Button-1>', lambda e: self.select_public())
        
        self.private_dot.bind('<Button-1>', lambda e: self.select_private())
        private_label.bind('<Button-1>', lambda e: self.select_private())
        private_frame.bind('<Button-1>', lambda e: self.select_private())
        
        # Set default selection
        self.msg_type_var.set("public")
        self.public_dot.config(fg=ModernColors.PRIMARY)
        self.private_dot.config(fg=ModernColors.GRAY_300)
    
    def create_modern_chat_area(self, parent):
        """Create modern chat area with message bubbles"""
        # Chat container
        chat_container = tk.Frame(parent, bg=ModernColors.WHITE)
        chat_container.pack(side='right', fill='both', expand=True)
        
        # Chat header
        chat_header = tk.Frame(chat_container, bg=ModernColors.GRAY_50, height=70)
        chat_header.pack(fill='x')
        chat_header.pack_propagate(False)
        
        self.chat_title_label = tk.Label(
            chat_header,
            text="💬 Public Chat",
            font=('Segoe UI', 18, 'bold'),
            fg=ModernColors.GRAY_900,
            bg=ModernColors.GRAY_50
        )
        self.chat_title_label.pack(pady=20)
        
        # Messages area - SỬ DỤNG SCROLLEDTEXT VỚI AUTO-RESIZE
        messages_container = tk.Frame(chat_container, bg=ModernColors.WHITE)
        messages_container.pack(fill='both', expand=True)
        
        # Sử dụng ScrolledText
        from tkinter import scrolledtext
        self.chat_display = scrolledtext.ScrolledText(
            messages_container,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_900,
            font=('Segoe UI', 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
            relief='flat',
            bd=0,
            padx=5,
            pady=5
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Lưu trữ tin nhắn để có thể re-render khi resize
        self.messages = []
        
        # Bind resize event để tự động cập nhật vị trí tin nhắn
        self.chat_display.bind('<Configure>', self.on_chat_resize)
        
        # Message input area
        self.create_modern_input_area(chat_container)
        
        # Welcome message
        self.add_system_message("🎉 Welcome to ChatBox! Start chatting now!")
    
    def create_modern_input_area(self, parent):
        """Create modern message input area"""
        input_container = tk.Frame(parent, bg=ModernColors.WHITE)
        input_container.pack(fill='x', padx=0, pady=(0, 20))  # Loại bỏ padx=20
        
        # Input frame with glassmorphism
        input_frame = tk.Frame(
            input_container,
            bg=ModernColors.GRAY_50,
            relief='flat',
            bd=0
        )
        input_frame.pack(fill='x', pady=10, padx=20)  # Thêm padx=20 cho input frame
        
        # Message entry container
        entry_container = tk.Frame(input_frame, bg=ModernColors.GRAY_50)
        entry_container.pack(fill='x', padx=20, pady=15)
        
        # Message entry
        self.message_entry = tk.Entry(
            entry_container,
            font=('Segoe UI', 14, 'normal'),
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_900,
            relief='flat',
            bd=0,
            insertbackground=ModernColors.PRIMARY
        )
        self.message_entry.pack(side='left', fill='x', expand=True, padx=(0, 15), ipady=12)
        
        # Send button
        self.send_btn = tk.Button(
            entry_container,
            text="Send",
            font=('Segoe UI', 12, 'bold'),
            bg=ModernColors.PRIMARY,
            fg=ModernColors.WHITE,
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=25,
            pady=12,
            command=self.send_message
        )
        self.send_btn.pack(side='right')
        
        # Add hover effect to send button
        ModernAnimations.button_hover_effect(
            self.send_btn, ModernColors.PRIMARY, ModernColors.PRIMARY_DARK
        )
        
        # Bind events
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        # Add focus effects to entry
        def on_entry_focus_in(e):
            input_frame.config(
                highlightbackground=ModernColors.PRIMARY,
                highlightcolor=ModernColors.PRIMARY,
                highlightthickness=2
            )
        
        def on_entry_focus_out(e):
            input_frame.config(highlightthickness=0)
        
        self.message_entry.bind('<FocusIn>', on_entry_focus_in)
        self.message_entry.bind('<FocusOut>', on_entry_focus_out)
    
    def create_modern_status_bar(self):
        """Create modern status bar"""
        status_frame = tk.Frame(self.main_frame, bg=ModernColors.GRAY_800, height=35)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        # Status content
        status_content = tk.Frame(status_frame, bg=ModernColors.GRAY_800)
        status_content.pack(fill='both', expand=True, padx=20)
        
        # Connection status
        self.status_label = tk.Label(
            status_content,
            text="🟢 Connected",
            font=('Segoe UI', 11, 'bold'),
            fg=ModernColors.SUCCESS,
            bg=ModernColors.GRAY_800
        )
        self.status_label.pack(side='left', pady=8)
        
        # Online users count
        self.users_count_label = tk.Label(
            status_content,
            text="👥 0 users online",
            font=('Segoe UI', 11, 'normal'),
            fg=ModernColors.GRAY_100,
            bg=ModernColors.GRAY_800
        )
        self.users_count_label.pack(side='right', pady=8)
    
    def select_public(self):
        """Select public chat mode"""
        self.msg_type_var.set("public")
        self.public_dot.config(fg=ModernColors.PRIMARY)
        self.private_dot.config(fg=ModernColors.GRAY_300)
        if self._ui_initialized:
            self.on_chat_type_change()
    
    def select_private(self):
        """Select private chat mode"""
        self.msg_type_var.set("private")
        self.public_dot.config(fg=ModernColors.GRAY_300)
        self.private_dot.config(fg=ModernColors.SECONDARY)
        if self._ui_initialized:
            self.on_chat_type_change()
    
    def on_chat_type_change(self):
        """Handle chat type change"""
        try:
            if self.msg_type_var.get() == "public":
                self.chat_title_label.config(text="💬 Public Chat")
                self.selected_user = None
            elif self.selected_user:
                self.chat_title_label.config(text=f"🔒 Private Chat with {self.selected_user}")
        except (AttributeError, tk.TclError):
            # Widget doesn't exist yet or has been destroyed
            pass
    
    def animate_interface(self):
        """Animate interface elements"""
        self.animation_step += 1
        
        # Animate logo
        if hasattr(self, 'logo_label'):
            # Subtle color animation
            colors = [ModernColors.WHITE, ModernColors.GRAY_100, ModernColors.WHITE]
            color_index = (self.animation_step // 30) % len(colors)
            try:
                self.logo_label.config(fg=colors[color_index])
            except tk.TclError:
                pass
        
        # Continue animation
        if self._ui_initialized:
            self.root.after(100, self.animate_interface)
    
    def on_chat_resize(self, event=None):
        """Handle chat area resize - re-render messages to maintain right alignment"""
        if hasattr(self, 'messages') and self.messages:
            # Lưu vị trí scroll hiện tại
            scroll_pos = self.chat_display.yview()[1]
            
            # Xóa tất cả nội dung
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
            # Re-render tất cả tin nhắn với vị trí mới
            for msg in self.messages:
                self._render_message(msg['sender'], msg['content'], msg['msg_type'], msg['is_own'], msg['timestamp'])
            
            # Khôi phục vị trí scroll
            self.chat_display.after(10, lambda: self.chat_display.yview_moveto(scroll_pos))
    
    def _render_message(self, sender, content, msg_type, is_own, timestamp):
        """Render a single message - tất cả căn trái với tên người gửi"""
        self.chat_display.config(state=tk.NORMAL)
        
        if is_own:
            # Own message - căn trái với tên và màu xanh
            # Hiển thị tên người gửi
            self.chat_display.insert(tk.END, f"You:\n")
            
            start_index = self.chat_display.index(tk.END)
            self.chat_display.insert(tk.END, f"{content}\n")
            end_index = self.chat_display.index(tk.END + "-1c")
            
            # Tag với màu xanh cho tin nhắn của mình
            tag_name = f"own_{start_index.replace('.', '_')}"
            self.chat_display.tag_add(tag_name, start_index, end_index)
            self.chat_display.tag_config(tag_name,
                                       background=ModernColors.PRIMARY,  # Màu xanh
                                       foreground=ModernColors.WHITE,
                                       relief="raised",
                                       borderwidth=1,
                                       justify="left")
            
            # Timestamp
            self.chat_display.insert(tk.END, f"{timestamp}\n\n")
                
        else:
            # Other's message - căn trái với màu xám
            if sender != 'SYSTEM':
                self.chat_display.insert(tk.END, f"{sender}:\n")
            
            start_index = self.chat_display.index(tk.END)
            self.chat_display.insert(tk.END, f"{content}\n")
            end_index = self.chat_display.index(tk.END + "-1c")
            
            # Tag cho tin nhắn người khác hoặc system
            tag_name = f"other_{start_index.replace('.', '_')}"
            self.chat_display.tag_add(tag_name, start_index, end_index)
            
            if sender == 'SYSTEM':
                # System message - màu xanh info
                self.chat_display.tag_config(tag_name,
                                           background=ModernColors.INFO,
                                           foreground=ModernColors.WHITE,
                                           relief="raised",
                                           borderwidth=1,
                                           justify="left")
            else:
                # Other user message - màu xám
                self.chat_display.tag_config(tag_name,
                                           background=ModernColors.GRAY_100,
                                           foreground=ModernColors.GRAY_800,
                                           relief="raised",
                                           borderwidth=1,
                                           justify="left")
            
            if sender != 'SYSTEM':
                self.chat_display.insert(tk.END, f"{timestamp}\n\n")
            else:
                self.chat_display.insert(tk.END, f"\n")
        
        self.chat_display.config(state=tk.DISABLED)
    def add_message_bubble(self, sender, content, msg_type, is_own=False):
        """Add modern message bubble and store for re-rendering"""
        timestamp = datetime.now().strftime('%H:%M')
        
        # Lưu tin nhắn để có thể re-render khi resize
        if not hasattr(self, 'messages'):
            self.messages = []
        
        self.messages.append({
            'sender': sender,
            'content': content,
            'msg_type': msg_type,
            'is_own': is_own,
            'timestamp': timestamp
        })
        
        # Render tin nhắn
        self._render_message(sender, content, msg_type, is_own, timestamp)
        self.chat_display.see(tk.END)
    
    def add_system_message(self, message):
        """Add system message"""
        timestamp = datetime.now().strftime('%H:%M')
        
        # Lưu system message
        if not hasattr(self, 'messages'):
            self.messages = []
        
        self.messages.append({
            'sender': 'SYSTEM',
            'content': message,
            'msg_type': 'system',
            'is_own': False,
            'timestamp': timestamp
        })
        
        # Render system message
        self.chat_display.config(state=tk.NORMAL)
        
        # Center the system message
        try:
            widget_width = self.chat_display.winfo_width()
            char_width = self.chat_display.tk.call("font", "measure", self.chat_display['font'], "0")
            
            if widget_width > 1 and char_width > 0:
                max_chars = (widget_width - 50) // char_width
                spaces_needed = max(0, (max_chars - len(message)) // 2)
            else:
                spaces_needed = max(0, (50 - len(message)) // 2)
        except:
            spaces_needed = max(0, (50 - len(message)) // 2)
        
        padding = " " * spaces_needed
        
        start_index = self.chat_display.index(tk.END)
        self.chat_display.insert(tk.END, f"{padding}{message}\n\n")
        end_index = self.chat_display.index(tk.END + "-2c")
        
        # Style system message
        tag_name = f"system_{start_index}"
        self.chat_display.tag_add(tag_name, f"{start_index} +{spaces_needed}c", end_index)
        self.chat_display.tag_config(tag_name,
                                   background=ModernColors.INFO,
                                   foreground=ModernColors.WHITE,
                                   relief="raised",
                                   borderwidth=1)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        """Send message with modern UX"""
        if not self.connected:
            return
        
        message = self.message_entry.get().strip()
        if not message:
            return
        
        msg_type = self.msg_type_var.get()
        
        if msg_type == "private":
            if not self.selected_user:
                messagebox.showwarning("Warning", "Please select a user for private message!")
                return
            receiver = self.selected_user
        else:
            receiver = "ALL"
        
        try:
            # Send message to server
            msg = f"{msg_type.upper()}|{self.username}|{receiver}|{message}|{datetime.now()}"
            self.socket.send(msg.encode('utf-8'))
            
            # Add own message bubble
            self.add_message_bubble(self.username, message, msg_type, is_own=True)
            
            # Clear input
            self.message_entry.delete(0, tk.END)
            
        except Exception as e:
            self.add_system_message(f"❌ Error sending message: {str(e)}")
    
    def on_search_users(self, event=None):
        """Handle user search"""
        search_term = self.search_entry.get().strip()
        
        # Nếu search term là placeholder hoặc rỗng, hiển thị tất cả
        if search_term == "Type username to search..." or not search_term:
            filtered_users = self.online_users
        else:
            # Lọc user theo search term (không phân biệt hoa thường)
            search_lower = search_term.lower()
            filtered_users = [user for user in self.online_users if search_lower in user.lower()]
        
        # Xóa danh sách hiện tại
        for widget in self.users_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Hiển thị user đã lọc
        for user in filtered_users:
            self.add_user_to_list(user)
        
        # Cập nhật số lượng user
        if search_term and search_term != "Type username to search...":
            # Khi đang search, hiển thị số kết quả
            self.users_count_label.config(text=f"👥 {len(filtered_users)} found / {len(self.online_users) + 1} total")
        else:
            # Khi không search, hiển thị tổng số
            total_count = len(self.online_users) + 1
            self.users_count_label.config(text=f"👥 {total_count} users online")
        
        # Đảm bảo focus vẫn ở search box nếu đang search
        if event and event.widget == self.search_entry and search_term != "Type username to search...":
            self.root.after(1, lambda: self.search_entry.focus_set())
    
    def handle_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.disconnect()
    
    def disconnect(self):
        """Disconnect from server"""
        if self.connected:
            try:
                self.socket.close()
            except:
                pass
        
        self.connected = False
        self.on_disconnect()
    
    def _message_listener(self):
        """Listen for messages from server"""
        try:
            self.socket.settimeout(1.0)
        except:
            pass
            
        while self.connected:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                # Parse message
                parts = message.split('|', 4)
                if len(parts) >= 4:
                    msg_type = parts[0]
                    sender = parts[1]
                    receiver = parts[2]
                    content = parts[3]
                    
                    # Update UI in main thread
                    self.root.after(0, lambda m=msg_type, s=sender, r=receiver, c=content: 
                                   self._handle_received_message(m, s, r, c))
                        
            except socket.timeout:
                continue
            except Exception as e:
                if self.connected:
                    self.root.after(0, lambda: self.add_system_message(f"❌ Connection lost: {str(e)}"))
                break
        
        self.connected = False
    
    def _handle_received_message(self, msg_type, sender, receiver, content):
        """Handle received message"""
        print(f"🔍 DEBUG: Nhận message - Type: {msg_type}, Sender: {sender}, Content: {content}")  # Debug
        
        # Don't show own messages again
        if sender == self.username:
            return
            
        if msg_type == "PUBLIC":
            self.add_message_bubble(sender, content, "public", is_own=False)
        elif msg_type == "PRIVATE":
            self.add_message_bubble(sender, content, "private", is_own=False)
        elif msg_type == "JOIN":
            self.add_system_message(f"👋 {sender} joined the chat")
            # Không cần thêm user vào danh sách ở đây vì USERLIST sẽ được gửi sau
        elif msg_type == "LEAVE":
            self.add_system_message(f"👋 {sender} left the chat")
            # Không cần xóa user ở đây vì USERLIST sẽ được gửi sau
        elif msg_type == "USERLIST" or msg_type == "USER_LIST":
            # Nhận danh sách user online từ server - TẤT CẢ CLIENT ĐỀU NHẬN
            print(f"🎯 DEBUG: Nhận USERLIST - Raw content: '{content}'")  # Debug
            
            if content and content.strip():
                users = [user.strip() for user in content.split(',') if user.strip()]
                print(f"🎯 DEBUG: Users sau split: {users}")  # Debug
                
                # Lọc ra những user khác (không bao gồm mình)
                other_users = [user for user in users if user != self.username]
                
                # Cập nhật danh sách
                self.online_users = other_users
                self.update_online_users()
                
                print(f"📋 USERLIST nhận được: {users}")  # Debug
                print(f"📋 Sau khi lọc (không có {self.username}): {other_users}")  # Debug
            else:
                print("🎯 DEBUG: USERLIST content rỗng hoặc None")
                self.online_users = []
                self.update_online_users()
        elif msg_type == "ERROR":
            self.add_system_message(f"❌ Error: {content}")
        elif msg_type == "LOGIN_OK":
            self.add_system_message(f"✅ {content}")
            # Thêm chính mình vào danh sách online
            if self.username not in self.online_users:
                self.online_users.append(self.username)
                self.update_online_users()
    
    def update_online_users(self):
        """Update online users list"""
        # Xóa tất cả user hiện tại
        for widget in self.users_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Thêm từng user online (không bao gồm mình)
        for user in self.online_users:
            self.add_user_to_list(user)
        
        # Cập nhật số lượng user (bao gồm cả mình)
        total_count = len(self.online_users) + 1  # +1 cho chính mình
        self.users_count_label.config(text=f"👥 {total_count} users online")
        
        print(f"🔄 Cập nhật UI: {len(self.online_users)} users khác + mình = {total_count} total")  # Debug
    
    def add_user_to_list(self, username):
        """Add a user to the online users list"""
        user_frame = tk.Frame(self.users_scrollable_frame, bg=ModernColors.WHITE)
        user_frame.pack(fill='x', padx=5, pady=2)
        
        # User avatar - NÚT TRÒN MÀU XANH
        avatar_frame = tk.Frame(user_frame, bg=ModernColors.WHITE)
        avatar_frame.pack(side='left', padx=(10, 10))
        
        avatar_button = tk.Label(
            avatar_frame,
            text="●",  # Nút tròn
            font=('Segoe UI', 20),
            bg=ModernColors.WHITE,
            fg=ModernColors.PRIMARY,  # Màu xanh
            width=2,
            height=1
        )
        avatar_button.pack()
        
        # Username
        name_label = tk.Label(
            user_frame,
            text=username,
            font=('Segoe UI', 12, 'normal'),
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_900,
            anchor='w'
        )
        name_label.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Online status - NÚT XANH NHỎ
        status_label = tk.Label(
            user_frame,
            text="●",
            font=('Segoe UI', 12),
            bg=ModernColors.WHITE,
            fg=ModernColors.SUCCESS  # Màu xanh lá
        )
        status_label.pack(side='right', padx=(0, 10))
        
        # Click event để chọn user cho private chat
        def select_user(event=None):
            self.selected_user = username
            self.on_chat_type_change()
            # Highlight selected user
            for child in self.users_scrollable_frame.winfo_children():
                child.config(bg=ModernColors.WHITE)
            user_frame.config(bg=ModernColors.GRAY_100)
        
        user_frame.bind('<Button-1>', select_user)
        avatar_button.bind('<Button-1>', select_user)
        name_label.bind('<Button-1>', select_user)
        status_label.bind('<Button-1>', select_user)
        
        # Hover effect
        def on_enter(e):
            if user_frame.cget('bg') != ModernColors.GRAY_100:
                user_frame.config(bg=ModernColors.GRAY_50)
        
        def on_leave(e):
            if user_frame.cget('bg') != ModernColors.GRAY_100:
                user_frame.config(bg=ModernColors.WHITE)
        
        user_frame.bind('<Enter>', on_enter)
        user_frame.bind('<Leave>', on_leave)
        """Show chat page with entrance animation"""
        self.main_frame.pack(fill='both', expand=True)
        
        # Focus on message entry
        self.root.after(100, lambda: self.message_entry.focus())
        
        # Entrance animation
        ModernAnimations.fade_in(self.main_frame)
    
    def hide(self):
        """Hide chat page"""
        self.main_frame.pack_forget()
    
    def show(self):
        """Show chat page with entrance animation"""
        self.main_frame.pack(fill='both', expand=True)
        
        # Không tự động focus vào message entry nữa để tránh conflict với search
        # self.root.after(100, lambda: self.message_entry.focus())
        
        # Request danh sách user online ngay khi vào chat - nhiều lần để đảm bảo
        self.root.after(200, self.request_user_list)
        self.root.after(500, self.request_user_list)
        self.root.after(1000, self.request_user_list)
        
        # Entrance animation
        ModernAnimations.fade_in(self.main_frame)
    
    def request_user_list(self):
        """Request danh sách user online từ server"""
        try:
            # Gửi yêu cầu lấy danh sách user
            request_msg = f"GET_USERS|{self.username}|SERVER|request|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.socket.send(request_msg.encode('utf-8'))
            print(f"📤 Đã gửi yêu cầu GET_USERS")
        except Exception as e:
            print(f"❌ Lỗi gửi GET_USERS: {e}")
            # Fallback: thử broadcast để trigger server gửi lại user list
            try:
                ping_msg = f"PING|{self.username}|SERVER|ping|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.socket.send(ping_msg.encode('utf-8'))
            except:
                pass