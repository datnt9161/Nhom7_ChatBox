#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatBox Client - UI Components
Reusable UI components for the chat application
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
from styles import ModernStyles, IconHelper

class ModernScrollableFrame(tk.Frame):
    """A modern scrollable frame"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=ModernStyles.COLORS['light'])
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=ModernStyles.COLORS['light'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class ChatMessage(tk.Frame):
    """A single chat message component"""
    
    def __init__(self, parent, sender, content, timestamp, msg_type="public", is_own=False):
        super().__init__(parent, bg=ModernStyles.COLORS['light'])
        
        self.sender = sender
        self.content = content
        self.timestamp = timestamp
        self.msg_type = msg_type
        self.is_own = is_own
        
        self.create_message()
    
    def create_message(self):
        """Create message layout"""
        # Message container
        container = tk.Frame(self, bg=ModernStyles.COLORS['light'])
        
        if self.is_own:
            container.pack(fill='x', padx=(50, 10), pady=2, anchor='e')
            bg_color = ModernStyles.COLORS['primary']
            fg_color = ModernStyles.COLORS['white']
        else:
            container.pack(fill='x', padx=(10, 50), pady=2, anchor='w')
            bg_color = ModernStyles.COLORS['white']
            fg_color = ModernStyles.COLORS['black']
        
        # Message bubble
        bubble = tk.Frame(container, bg=bg_color, relief='raised', bd=1)
        bubble.pack(fill='x')
        
        # Header (sender and time)
        header = tk.Frame(bubble, bg=bg_color)
        header.pack(fill='x', padx=10, pady=(5, 0))
        
        sender_label = tk.Label(header, text=self.sender,
                               font=ModernStyles.FONTS['small'],
                               fg=fg_color, bg=bg_color)
        sender_label.pack(side='left')
        
        time_label = tk.Label(header, text=self.timestamp,
                             font=('Segoe UI', 8),
                             fg=fg_color if self.is_own else ModernStyles.COLORS['muted'],
                             bg=bg_color)
        time_label.pack(side='right')
        
        # Message content
        content_label = tk.Label(bubble, text=self.content,
                                font=ModernStyles.FONTS['body'],
                                fg=fg_color, bg=bg_color,
                                wraplength=300, justify='left')
        content_label.pack(fill='x', padx=10, pady=(0, 8))
        
        # Private message indicator
        if self.msg_type == "private":
            indicator = tk.Label(bubble, text=f"{IconHelper.get('private')} Riêng tư",
                                font=('Segoe UI', 8, 'italic'),
                                fg=fg_color if self.is_own else ModernStyles.COLORS['warning'],
                                bg=bg_color)
            indicator.pack(padx=10, pady=(0, 5))

class UserListItem(tk.Frame):
    """A user list item component"""
    
    def __init__(self, parent, username, status="online", **kwargs):
        super().__init__(parent, bg=ModernStyles.COLORS['light'], **kwargs)
        
        self.username = username
        self.status = status
        
        self.create_item()
    
    def create_item(self):
        """Create user item layout"""
        # Status indicator
        status_icon = IconHelper.get('online') if self.status == 'online' else IconHelper.get('offline')
        status_label = tk.Label(self, text=status_icon,
                               font=ModernStyles.FONTS['body'],
                               bg=ModernStyles.COLORS['light'])
        status_label.pack(side='left', padx=(10, 5))
        
        # Username
        username_label = tk.Label(self, text=self.username,
                                 font=ModernStyles.FONTS['body'],
                                 fg=ModernStyles.COLORS['black'],
                                 bg=ModernStyles.COLORS['light'])
        username_label.pack(side='left', fill='x', expand=True)
        
        # Hover effects
        def on_enter(e):
            self.config(bg=ModernStyles.COLORS['primary'])
            status_label.config(bg=ModernStyles.COLORS['primary'])
            username_label.config(bg=ModernStyles.COLORS['primary'], 
                                 fg=ModernStyles.COLORS['white'])
        
        def on_leave(e):
            self.config(bg=ModernStyles.COLORS['light'])
            status_label.config(bg=ModernStyles.COLORS['light'])
            username_label.config(bg=ModernStyles.COLORS['light'],
                                 fg=ModernStyles.COLORS['black'])
        
        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
        status_label.bind("<Enter>", on_enter)
        status_label.bind("<Leave>", on_leave)
        username_label.bind("<Enter>", on_enter)
        username_label.bind("<Leave>", on_leave)

class NotificationToast(tk.Toplevel):
    """A notification toast component"""
    
    def __init__(self, parent, message, toast_type="info", duration=3000):
        super().__init__(parent)
        
        self.message = message
        self.toast_type = toast_type
        self.duration = duration
        
        self.setup_toast()
        self.show_toast()
    
    def setup_toast(self):
        """Setup toast window"""
        self.withdraw()  # Hide initially
        self.overrideredirect(True)  # Remove window decorations
        
        # Colors based on type
        colors = {
            'info': (ModernStyles.COLORS['info'], ModernStyles.COLORS['white']),
            'success': (ModernStyles.COLORS['success'], ModernStyles.COLORS['white']),
            'warning': (ModernStyles.COLORS['warning'], ModernStyles.COLORS['white']),
            'error': (ModernStyles.COLORS['danger'], ModernStyles.COLORS['white'])
        }
        
        bg_color, fg_color = colors.get(self.toast_type, colors['info'])
        
        # Main frame
        main_frame = tk.Frame(self, bg=bg_color, relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True)
        
        # Icon
        icon = {
            'info': IconHelper.get('info'),
            'success': IconHelper.get('success'),
            'warning': IconHelper.get('warning'),
            'error': IconHelper.get('error')
        }.get(self.toast_type, IconHelper.get('info'))
        
        icon_label = tk.Label(main_frame, text=icon,
                             font=ModernStyles.FONTS['heading'],
                             fg=fg_color, bg=bg_color)
        icon_label.pack(side='left', padx=(10, 5), pady=10)
        
        # Message
        message_label = tk.Label(main_frame, text=self.message,
                                font=ModernStyles.FONTS['body'],
                                fg=fg_color, bg=bg_color,
                                wraplength=250)
        message_label.pack(side='left', padx=(0, 10), pady=10)
    
    def show_toast(self):
        """Show toast notification"""
        # Position at top-right of screen
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        screen_width = self.winfo_screenwidth()
        x = screen_width - width - 20
        y = 50
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()  # Show window
        
        # Auto-hide after duration
        self.after(self.duration, self.hide_toast)
    
    def hide_toast(self):
        """Hide toast notification"""
        self.destroy()

class LoadingSpinner(tk.Frame):
    """A loading spinner component"""
    
    def __init__(self, parent, text="Đang tải...", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.text = text
        self.is_spinning = False
        self.current_frame = 0
        
        self.create_spinner()
    
    def create_spinner(self):
        """Create spinner layout"""
        # Spinner frames (simple text animation)
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        
        self.spinner_label = tk.Label(self, text=self.frames[0],
                                     font=ModernStyles.FONTS['heading'],
                                     fg=ModernStyles.COLORS['primary'],
                                     bg=self.cget('bg'))
        self.spinner_label.pack(pady=(10, 5))
        
        self.text_label = tk.Label(self, text=self.text,
                                  font=ModernStyles.FONTS['body'],
                                  fg=ModernStyles.COLORS['muted'],
                                  bg=self.cget('bg'))
        self.text_label.pack(pady=(0, 10))
    
    def start(self):
        """Start spinning animation"""
        self.is_spinning = True
        self._animate()
    
    def stop(self):
        """Stop spinning animation"""
        self.is_spinning = False
    
    def _animate(self):
        """Animate spinner"""
        if self.is_spinning:
            self.spinner_label.config(text=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.after(100, self._animate)

class StatusBar(tk.Frame):
    """A status bar component"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernStyles.COLORS['dark'], height=30, **kwargs)
        self.pack_propagate(False)
        
        # Status text
        self.status_label = tk.Label(self, text="Sẵn sàng",
                                    font=ModernStyles.FONTS['small'],
                                    fg=ModernStyles.COLORS['light'],
                                    bg=ModernStyles.COLORS['dark'])
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Connection indicator
        self.connection_label = tk.Label(self, text="⚫ Chưa kết nối",
                                        font=ModernStyles.FONTS['small'],
                                        fg=ModernStyles.COLORS['muted'],
                                        bg=ModernStyles.COLORS['dark'])
        self.connection_label.pack(side='right', padx=10, pady=5)
    
    def set_status(self, text, status_type="info"):
        """Set status text"""
        colors = {
            'info': ModernStyles.COLORS['light'],
            'success': ModernStyles.COLORS['success'],
            'warning': ModernStyles.COLORS['warning'],
            'error': ModernStyles.COLORS['danger']
        }
        
        color = colors.get(status_type, colors['info'])
        self.status_label.config(text=text, fg=color)
    
    def set_connection_status(self, connected=False):
        """Set connection status"""
        if connected:
            self.connection_label.config(text="🟢 Đã kết nối", 
                                        fg=ModernStyles.COLORS['success'])
        else:
            self.connection_label.config(text="⚫ Chưa kết nối",
                                        fg=ModernStyles.COLORS['muted'])