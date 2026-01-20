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
        
        # Control buttons
        controls_frame = tk.Frame(right_frame, bg=ModernColors.PRIMARY)
        controls_frame.pack(side='right')
        
        # Settings button
        settings_btn = self.create_header_button(
            controls_frame, "⚙️", "Settings", self.show_settings
        )
        settings_btn.pack(side='left', padx=(0, 10))
        
        # Theme toggle
        theme_btn = self.create_header_button(
            controls_frame, "🌙", "Dark Mode", self.toggle_theme
        )
        theme_btn.pack(side='left', padx=(0, 10))
        
        # Logout button
        logout_btn = tk.Button(
            controls_frame,
            text="🚪 Logout",
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
        logout_btn.pack(side='left', padx=(10, 0))
        
        # Add hover effect
        ModernAnimations.button_hover_effect(
            logout_btn, ModernColors.ERROR, '#dc2626'
        )
        
        # Update header canvas size
        def update_header_size(event=None):
            self.header_canvas.configure(scrollregion=self.header_canvas.bbox("all"))
            canvas_width = self.header_canvas.winfo_width()
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
            font=ModernFonts.HEADLINE_SMALL,
            fg=ModernColors.GRAY_800,
            bg=ModernColors.GRAY_50
        ).pack(pady=20)
        
        # Search box
        search_frame = tk.Frame(self.sidebar, bg=ModernColors.WHITE)
        search_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.search_frame, self.search_entry = ModernWidgets.create_modern_entry(
            search_frame,
            placeholder="Search users...",
            width=25
        )
        self.search_frame.pack(fill='x')
        
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
        
        # Chat type selector
        type_frame = tk.Frame(self.sidebar, bg=ModernColors.GRAY_50, height=80)
        type_frame.pack(fill='x')
        type_frame.pack_propagate(False)
        
        tk.Label(
            type_frame,
            text="💬 Message Type",
            font=ModernFonts.TITLE_SMALL,
            fg=ModernColors.GRAY_800,
            bg=ModernColors.GRAY_50
        ).pack(pady=(15, 5))
        
        radio_frame = tk.Frame(type_frame, bg=ModernColors.GRAY_50)
        radio_frame.pack()
        
        # Modern radio buttons
        public_radio = tk.Radiobutton(
            radio_frame,
            text="🌐 Public",
            variable=self.msg_type_var,
            value="public",
            font=ModernFonts.BODY_MEDIUM,
            fg=ModernColors.GRAY_700,
            bg=ModernColors.GRAY_50,
            selectcolor=ModernColors.PRIMARY,
            activebackground=ModernColors.GRAY_50,
            command=self.on_chat_type_change
        )
        public_radio.pack(side='left', padx=(0, 30))
        
        private_radio = tk.Radiobutton(
            radio_frame,
            text="🔒 Private",
            variable=self.msg_type_var,
            value="private",
            font=ModernFonts.BODY_MEDIUM,
            fg=ModernColors.GRAY_700,
            bg=ModernColors.GRAY_50,
            selectcolor=ModernColors.SECONDARY,
            activebackground=ModernColors.GRAY_50,
            command=self.on_chat_type_change
        )
        private_radio.pack(side='left')
    
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
            font=ModernFonts.HEADLINE_SMALL,
            fg=ModernColors.GRAY_800,
            bg=ModernColors.GRAY_50
        )
        self.chat_title_label.pack(pady=20)
        
        # Messages area with custom styling
        messages_container = tk.Frame(chat_container, bg=ModernColors.GRAY_50)
        messages_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Custom chat display
        self.chat_frame = tk.Frame(messages_container, bg=ModernColors.WHITE)
        self.chat_frame.pack(fill='both', expand=True)
        
        # Scrollable chat area
        self.chat_canvas = tk.Canvas(
            self.chat_frame,
            bg=ModernColors.WHITE,
            highlightthickness=0
        )
        self.chat_scrollbar = ttk.Scrollbar(
            self.chat_frame,
            orient="vertical",
            command=self.chat_canvas.yview
        )
        self.chat_scrollable_frame = tk.Frame(self.chat_canvas, bg=ModernColors.WHITE)
        
        self.chat_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )
        )
        
        self.chat_canvas.create_window(
            (0, 0), window=self.chat_scrollable_frame, anchor="nw"
        )
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_scrollbar.pack(side="right", fill="y")
        
        # Message input area
        self.create_modern_input_area(chat_container)
        
        # Welcome message
        self.add_system_message("🎉 Welcome to ChatBox! Start chatting now!")
    
    def create_modern_input_area(self, parent):
        """Create modern message input area"""
        input_container = tk.Frame(parent, bg=ModernColors.WHITE)
        input_container.pack(fill='x', padx=20, pady=(0, 20))
        
        # Input frame with glassmorphism
        input_frame = tk.Frame(
            input_container,
            bg=ModernColors.GRAY_50,
            relief='flat',
            bd=0
        )
        input_frame.pack(fill='x', pady=10)
        
        # Message entry container
        entry_container = tk.Frame(input_frame, bg=ModernColors.GRAY_50)
        entry_container.pack(fill='x', padx=20, pady=15)
        
        # Message entry
        self.message_entry = tk.Entry(
            entry_container,
            font=ModernFonts.BODY_LARGE,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_800,
            relief='flat',
            bd=0,
            insertbackground=ModernColors.PRIMARY
        )
        self.message_entry.pack(side='left', fill='x', expand=True, padx=(0, 15), ipady=12)
        
        # Send button
        self.send_btn = tk.Button(
            entry_container,
            text="📤 Send",
            font=ModernFonts.BODY_MEDIUM,
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
            font=ModernFonts.BODY_SMALL,
            fg=ModernColors.SUCCESS,
            bg=ModernColors.GRAY_800
        )
        self.status_label.pack(side='left', pady=8)
        
        # Online users count
        self.users_count_label = tk.Label(
            status_content,
            text="👥 0 users online",
            font=ModernFonts.BODY_SMALL,
            fg=ModernColors.GRAY_300,
            bg=ModernColors.GRAY_800
        )
        self.users_count_label.pack(side='right', pady=8)
    
    def animate_interface(self):
        """Animate interface elements"""
        self.animation_step += 1
        
        # Animate logo
        if hasattr(self, 'logo_label'):
            # Subtle color animation
            colors = [ModernColors.WHITE, ModernColors.GRAY_100, ModernColors.WHITE]
            color_index = (self.animation_step // 30) % len(colors)
            self.logo_label.config(fg=colors[color_index])
        
        # Continue animation
        self.root.after(100, self.animate_interface)
    
    def add_message_bubble(self, sender, content, msg_type, is_own=False):
        """Add modern message bubble"""
        # Message container
        msg_container = tk.Frame(self.chat_scrollable_frame, bg=ModernColors.WHITE)
        msg_container.pack(fill='x', padx=10, pady=5)
        
        if is_own:
            # Own message - right aligned, blue bubble
            bubble_frame = tk.Frame(msg_container, bg=ModernColors.WHITE)
            bubble_frame.pack(anchor='e', padx=(50, 0))
            
            # Message bubble
            bubble = tk.Frame(
                bubble_frame,
                bg=ModernColors.PRIMARY,
                relief='flat',
                bd=0
            )
            bubble.pack(anchor='e')
            
            # Message text
            msg_label = tk.Label(
                bubble,
                text=content,
                font=ModernFonts.BODY_MEDIUM,
                fg=ModernColors.WHITE,
                bg=ModernColors.PRIMARY,
                wraplength=300,
                justify='left'
            )
            msg_label.pack(padx=15, pady=10)
            
            # Timestamp
            time_label = tk.Label(
                bubble_frame,
                text=datetime.now().strftime("%H:%M"),
                font=ModernFonts.LABEL_SMALL,
                fg=ModernColors.GRAY_400,
                bg=ModernColors.WHITE
            )
            time_label.pack(anchor='e', pady=(2, 0))
            
        else:
            # Other's message - left aligned, gray bubble
            bubble_frame = tk.Frame(msg_container, bg=ModernColors.WHITE)
            bubble_frame.pack(anchor='w', padx=(0, 50))
            
            # Sender name
            sender_label = tk.Label(
                bubble_frame,
                text=sender,
                font=ModernFonts.LABEL_MEDIUM,
                fg=ModernColors.GRAY_600,
                bg=ModernColors.WHITE
            )
            sender_label.pack(anchor='w', pady=(0, 2))
            
            # Message bubble
            bubble = tk.Frame(
                bubble_frame,
                bg=ModernColors.GRAY_100,
                relief='flat',
                bd=0
            )
            bubble.pack(anchor='w')
            
            # Message text
            msg_label = tk.Label(
                bubble,
                text=content,
                font=ModernFonts.BODY_MEDIUM,
                fg=ModernColors.GRAY_800,
                bg=ModernColors.GRAY_100,
                wraplength=300,
                justify='left'
            )
            msg_label.pack(padx=15, pady=10)
            
            # Timestamp
            time_label = tk.Label(
                bubble_frame,
                text=datetime.now().strftime("%H:%M"),
                font=ModernFonts.LABEL_SMALL,
                fg=ModernColors.GRAY_400,
                bg=ModernColors.WHITE
            )
            time_label.pack(anchor='w', pady=(2, 0))
        
        # Auto-scroll to bottom
        self.root.after(10, lambda: self.chat_canvas.yview_moveto(1.0))
    
    def add_system_message(self, message):
        """Add system message"""
        msg_container = tk.Frame(self.chat_scrollable_frame, bg=ModernColors.WHITE)
        msg_container.pack(fill='x', padx=10, pady=10)
        
        # System message bubble
        bubble = tk.Frame(
            msg_container,
            bg=ModernColors.INFO,
            relief='flat',
            bd=0
        )
        bubble.pack(anchor='center')
        
        msg_label = tk.Label(
            bubble,
            text=message,
            font=ModernFonts.BODY_SMALL,
            fg=ModernColors.WHITE,
            bg=ModernColors.INFO,
            wraplength=400
        )
        msg_label.pack(padx=20, pady=8)
        
        # Auto-scroll to bottom
        self.root.after(10, lambda: self.chat_canvas.yview_moveto(1.0))
    
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
    
    def on_chat_type_change(self):
        """Handle chat type change"""
        if self.msg_type_var.get() == "public":
            self.chat_title_label.config(text="💬 Public Chat")
            self.selected_user = None
        elif self.selected_user:
            self.chat_title_label.config(text=f"🔒 Private Chat with {self.selected_user}")
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", "Settings panel coming soon!")
    
    def toggle_theme(self):
        """Toggle dark/light theme"""
        messagebox.showinfo("Theme", "Theme toggle coming soon!")
    
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
        # Don't show own messages again
        if sender == self.username:
            return
            
        if msg_type == "PUBLIC":
            self.add_message_bubble(sender, content, "public", is_own=False)
        elif msg_type == "PRIVATE":
            self.add_message_bubble(sender, content, "private", is_own=False)
        elif msg_type == "JOIN":
            self.add_system_message(f"👋 {sender} joined the chat")
        elif msg_type == "LEAVE":
            self.add_system_message(f"👋 {sender} left the chat")
        elif msg_type == "ERROR":
            self.add_system_message(f"❌ Error: {content}")
        elif msg_type == "LOGIN_OK":
            self.add_system_message(f"✅ {content}")
    
    def show(self):
        """Show chat page with entrance animation"""
        self.main_frame.pack(fill='both', expand=True)
        
        # Focus on message entry
        self.root.after(100, lambda: self.message_entry.focus())
        
        # Entrance animation
        ModernAnimations.fade_in(self.main_frame)
    
    def hide(self):
        """Hide chat page"""
        self.main_frame.pack_forget()