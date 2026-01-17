#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatBox Client - Styles and Themes
Beautiful styling for the chat application
"""

import tkinter as tk
from tkinter import ttk

class ModernStyles:
    """Modern styling class for ChatBox"""
    
    # Color palette
    COLORS = {
        'primary': '#3498db',      # Blue
        'secondary': '#2c3e50',    # Dark blue
        'success': '#27ae60',      # Green
        'danger': '#e74c3c',       # Red
        'warning': '#f39c12',      # Orange
        'info': '#17a2b8',         # Light blue
        'light': '#ecf0f1',        # Light gray
        'dark': '#34495e',         # Dark gray
        'muted': '#bdc3c7',        # Muted gray
        'white': '#ffffff',
        'black': '#2c3e50'
    }
    
    # Fonts
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'subtitle': ('Segoe UI', 16, 'bold'),
        'heading': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 11),
        'small': ('Segoe UI', 9),
        'button': ('Segoe UI', 11, 'bold'),
        'input': ('Segoe UI', 12)
    }
    
    @classmethod
    def apply_chat_text_tags(cls, text_widget):
        """Apply text tags for chat messages"""
        # Own messages
        text_widget.tag_configure("own_message", 
                                 foreground=cls.COLORS['primary'],
                                 font=cls.FONTS['body'])
        
        # Other messages
        text_widget.tag_configure("other_message",
                                 foreground=cls.COLORS['black'],
                                 font=cls.FONTS['body'])
        
        # Private own messages
        text_widget.tag_configure("private_own",
                                 foreground=cls.COLORS['success'],
                                 font=cls.FONTS['body'])
        
        # Private other messages
        text_widget.tag_configure("private_other",
                                 foreground=cls.COLORS['warning'],
                                 font=cls.FONTS['body'])
        
        # System messages
        text_widget.tag_configure("system",
                                 foreground=cls.COLORS['muted'],
                                 font=('Segoe UI', 10, 'italic'))
    
    @classmethod
    def create_modern_button(cls, parent, text, command=None, style='primary', **kwargs):
        """Create a modern styled button"""
        colors = {
            'primary': (cls.COLORS['primary'], cls.COLORS['white']),
            'success': (cls.COLORS['success'], cls.COLORS['white']),
            'danger': (cls.COLORS['danger'], cls.COLORS['white']),
            'warning': (cls.COLORS['warning'], cls.COLORS['white']),
            'secondary': (cls.COLORS['dark'], cls.COLORS['white'])
        }
        
        bg_color, fg_color = colors.get(style, colors['primary'])
        
        button = tk.Button(parent, text=text, command=command,
                          font=cls.FONTS['button'],
                          bg=bg_color, fg=fg_color,
                          relief='flat', bd=0, cursor='hand2',
                          **kwargs)
        
        # Hover effects
        def on_enter(e):
            button.config(bg=cls._darken_color(bg_color))
        
        def on_leave(e):
            button.config(bg=bg_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    @classmethod
    def create_modern_entry(cls, parent, placeholder="", **kwargs):
        """Create a modern styled entry"""
        entry = tk.Entry(parent,
                        font=cls.FONTS['input'],
                        bg=cls.COLORS['light'],
                        fg=cls.COLORS['black'],
                        relief='flat', bd=0,
                        highlightthickness=2,
                        highlightcolor=cls.COLORS['primary'],
                        **kwargs)
        
        # Placeholder functionality
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=cls.COLORS['muted'])
            
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=cls.COLORS['black'])
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=cls.COLORS['muted'])
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        return entry
    
    @classmethod
    def create_card_frame(cls, parent, **kwargs):
        """Create a card-like frame"""
        frame = tk.Frame(parent,
                        bg=cls.COLORS['dark'],
                        relief='raised',
                        bd=1,
                        **kwargs)
        return frame
    
    @classmethod
    def _darken_color(cls, color):
        """Darken a hex color"""
        # Simple darkening by reducing RGB values
        if color.startswith('#'):
            color = color[1:]
        
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

class AnimationHelper:
    """Helper class for simple animations"""
    
    @staticmethod
    def fade_in(widget, duration=300):
        """Fade in animation"""
        # Simple implementation - can be enhanced
        widget.config(state='normal')
    
    @staticmethod
    def slide_in(widget, direction='left', duration=300):
        """Slide in animation"""
        # Simple implementation - can be enhanced
        widget.pack()
    
    @staticmethod
    def bounce_button(button):
        """Bounce effect for button"""
        original_relief = button.cget('relief')
        button.config(relief='sunken')
        button.after(100, lambda: button.config(relief=original_relief))

class IconHelper:
    """Helper class for emoji icons"""
    
    ICONS = {
        'chat': '💬',
        'user': '👤',
        'users': '👥',
        'online': '🟢',
        'offline': '🔴',
        'send': '📤',
        'receive': '📥',
        'login': '🔐',
        'register': '📝',
        'logout': '🚪',
        'settings': '⚙️',
        'notification': '🔔',
        'private': '🔒',
        'public': '🌐',
        'warning': '⚠️',
        'error': '❌',
        'success': '✅',
        'info': 'ℹ️'
    }
    
    @classmethod
    def get(cls, name):
        """Get icon by name"""
        return cls.ICONS.get(name, '•')