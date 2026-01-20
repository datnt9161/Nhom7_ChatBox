#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Styles - Material Design 3 + Glassmorphism
"""

import tkinter as tk
from tkinter import ttk

class ModernColors:
    """Modern color palette inspired by Material Design 3"""
    
    # Primary colors
    PRIMARY = '#6366f1'  # Indigo
    PRIMARY_LIGHT = '#818cf8'
    PRIMARY_DARK = '#4f46e5'
    
    # Secondary colors  
    SECONDARY = '#06b6d4'  # Cyan
    SECONDARY_LIGHT = '#22d3ee'
    SECONDARY_DARK = '#0891b2'
    
    # Accent colors
    ACCENT = '#f59e0b'  # Amber
    ACCENT_LIGHT = '#fbbf24'
    ACCENT_DARK = '#d97706'
    
    # Semantic colors
    SUCCESS = '#10b981'  # Emerald
    WARNING = '#f59e0b'  # Amber
    ERROR = '#ef4444'    # Red
    INFO = '#3b82f6'     # Blue
    
    # Neutral colors
    WHITE = '#ffffff'
    GRAY_50 = '#f9fafb'
    GRAY_100 = '#f3f4f6'
    GRAY_200 = '#e5e7eb'
    GRAY_300 = '#d1d5db'
    GRAY_400 = '#6b7280'  # Làm đậm hơn
    GRAY_500 = '#4b5563'  # Làm đậm hơn
    GRAY_600 = '#374151'  # Làm đậm hơn
    GRAY_700 = '#1f2937'  # Làm đậm hơn
    GRAY_800 = '#111827'  # Làm đậm hơn
    GRAY_900 = '#000000'  # Đen hoàn toàn
    BLACK = '#000000'
    
    # Glass effect colors (using solid colors since Tkinter doesn't support alpha)
    GLASS_WHITE = '#f8fafc'
    GLASS_DARK = '#e2e8f0'
    
    # Gradient colors
    GRADIENT_START = '#667eea'
    GRADIENT_MID = '#764ba2'
    GRADIENT_END = '#f093fb'

class ModernFonts:
    """Modern typography system"""
    
    # Font families
    PRIMARY_FONT = 'Segoe UI'
    SECONDARY_FONT = 'Inter'
    MONO_FONT = 'Consolas'
    
    # Font sizes and weights
    DISPLAY_LARGE = (PRIMARY_FONT, 32, 'bold')
    DISPLAY_MEDIUM = (PRIMARY_FONT, 28, 'bold')
    DISPLAY_SMALL = (PRIMARY_FONT, 24, 'bold')
    
    HEADLINE_LARGE = (PRIMARY_FONT, 22, 'bold')
    HEADLINE_MEDIUM = (PRIMARY_FONT, 20, 'bold')
    HEADLINE_SMALL = (PRIMARY_FONT, 18, 'bold')
    
    TITLE_LARGE = (PRIMARY_FONT, 16, 'bold')
    TITLE_MEDIUM = (PRIMARY_FONT, 14, 'bold')
    TITLE_SMALL = (PRIMARY_FONT, 12, 'bold')
    
    BODY_LARGE = (PRIMARY_FONT, 14, 'normal')
    BODY_MEDIUM = (PRIMARY_FONT, 12, 'normal')
    BODY_SMALL = (PRIMARY_FONT, 11, 'normal')
    
    LABEL_LARGE = (PRIMARY_FONT, 12, 'normal')
    LABEL_MEDIUM = (PRIMARY_FONT, 11, 'normal')
    LABEL_SMALL = (PRIMARY_FONT, 10, 'normal')

class ModernShadows:
    """Modern shadow system"""
    
    ELEVATION_1 = {'relief': 'flat', 'bd': 0}
    ELEVATION_2 = {'relief': 'raised', 'bd': 1}
    ELEVATION_3 = {'relief': 'raised', 'bd': 2}
    ELEVATION_4 = {'relief': 'raised', 'bd': 3}

class ModernAnimations:
    """Animation utilities"""
    
    @staticmethod
    def fade_in(widget, duration=300):
        """Fade in animation"""
        steps = 20
        step_time = duration // steps
        
        def animate(step=0):
            if step <= steps:
                alpha = step / steps
                # Simulate fade by changing colors
                widget.after(step_time, lambda: animate(step + 1))
        
        animate()
    
    @staticmethod
    def slide_in(widget, direction='left', duration=300):
        """Slide in animation"""
        # Simple implementation - can be enhanced
        widget.pack()
    
    @staticmethod
    def button_hover_effect(button, normal_bg, hover_bg, normal_fg=None, hover_fg=None):
        """Add hover effect to button"""
        def on_enter(e):
            button.config(bg=hover_bg)
            if hover_fg:
                button.config(fg=hover_fg)
        
        def on_leave(e):
            button.config(bg=normal_bg)
            if normal_fg:
                button.config(fg=normal_fg)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

class ModernWidgets:
    """Modern widget factory"""
    
    @staticmethod
    def create_gradient_frame(parent, width, height, start_color, end_color):
        """Create gradient background frame"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        def draw_gradient():
            canvas.delete("gradient")
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Parse colors
                start_rgb = ModernWidgets._hex_to_rgb(start_color)
                end_rgb = ModernWidgets._hex_to_rgb(end_color)
                
                # Draw gradient
                for i in range(canvas_height):
                    ratio = i / canvas_height
                    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(0, i, canvas_width, i, fill=color, tags="gradient")
        
        canvas.bind('<Configure>', lambda e: canvas.after_idle(draw_gradient))
        canvas.after(100, draw_gradient)
        
        return canvas
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def create_modern_button(parent, text, command=None, style='primary', size='medium'):
        """Create modern button with Material Design styling"""
        styles = {
            'primary': {
                'bg': ModernColors.PRIMARY,
                'fg': ModernColors.WHITE,
                'hover_bg': ModernColors.PRIMARY_DARK,
                'hover_fg': ModernColors.WHITE
            },
            'secondary': {
                'bg': ModernColors.SECONDARY,
                'fg': ModernColors.WHITE,
                'hover_bg': ModernColors.SECONDARY_DARK,
                'hover_fg': ModernColors.WHITE
            },
            'outline': {
                'bg': ModernColors.WHITE,
                'fg': ModernColors.PRIMARY,
                'hover_bg': ModernColors.GRAY_50,
                'hover_fg': ModernColors.PRIMARY_DARK
            },
            'ghost': {
                'bg': ModernColors.GRAY_100,
                'fg': ModernColors.GRAY_700,
                'hover_bg': ModernColors.GRAY_200,
                'hover_fg': ModernColors.GRAY_800
            }
        }
        
        sizes = {
            'small': {'font': ('Segoe UI', 10, 'normal'), 'padx': 16, 'pady': 8},
            'medium': {'font': ('Segoe UI', 11, 'normal'), 'padx': 24, 'pady': 12},
            'large': {'font': ('Segoe UI', 12, 'bold'), 'padx': 32, 'pady': 16}
        }
        
        style_config = styles.get(style, styles['primary'])
        size_config = sizes.get(size, sizes['medium'])
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=size_config['font'],
            bg=style_config['bg'],
            fg=style_config['fg'],
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=size_config['padx'],
            pady=size_config['pady']
        )
        
        # Add hover effect
        ModernAnimations.button_hover_effect(
            button,
            style_config['bg'],
            style_config['hover_bg'],
            style_config['fg'],
            style_config['hover_fg']
        )
        
        return button
    
    @staticmethod
    def create_modern_entry(parent, placeholder="", width=30):
        """Create modern entry with Material Design styling"""
        frame = tk.Frame(parent, bg=ModernColors.WHITE)
        
        entry = tk.Entry(
            frame,
            font=('Segoe UI', 12, 'normal'),
            bg=ModernColors.GRAY_50,
            fg=ModernColors.GRAY_900,
            relief='flat',
            bd=0,
            width=width,
            insertbackground=ModernColors.PRIMARY
        )
        entry.pack(padx=16, pady=12, ipady=8)
        
        # Add placeholder effect
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=ModernColors.GRAY_500)
            
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=ModernColors.GRAY_900)
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg=ModernColors.GRAY_500)
            
            def on_key_press(e):
                # Clear placeholder when user starts typing
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=ModernColors.GRAY_900)
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
            entry.bind('<KeyPress>', on_key_press)
        
        # Add focus border effect
        def on_focus_in_border(e):
            frame.config(highlightbackground=ModernColors.PRIMARY, 
                        highlightcolor=ModernColors.PRIMARY, 
                        highlightthickness=2)
        
        def on_focus_out_border(e):
            frame.config(highlightthickness=0)
        
        entry.bind('<FocusIn>', on_focus_in_border)
        entry.bind('<FocusOut>', on_focus_out_border)
        
        return frame, entry
    
    @staticmethod
    def create_glass_card(parent, width=400, height=300):
        """Create glassmorphism card effect"""
        card = tk.Frame(
            parent,
            bg=ModernColors.WHITE,
            relief='flat',
            bd=1,
            width=width,
            height=height,
            highlightbackground=ModernColors.GRAY_200,
            highlightthickness=1
        )
        card.pack_propagate(False)
        
        return card