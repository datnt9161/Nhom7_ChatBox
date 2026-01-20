#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Login Page - Material Design 3 + Glassmorphism
"""

import tkinter as tk
from tkinter import messagebox
import threading
import socket
from datetime import datetime
import math
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from modern_styles import ModernColors, ModernFonts, ModernWidgets, ModernAnimations

class ModernLoginPage:
    def __init__(self, root, on_login_success, on_switch_to_register):
        self.root = root
        self.on_login_success = on_login_success
        self.on_switch_to_register = on_switch_to_register
        
        # Animation variables
        self.animation_step = 0
        self.is_loading = False
        
        self.create_modern_ui()
    
    def create_modern_ui(self):
        """Create ultra-modern login interface"""
        self.main_frame = tk.Frame(self.root, bg=ModernColors.GRAY_900)
        
        # Create animated gradient background
        self.create_animated_background()
        
        # Create floating login card
        self.create_login_card()
        
        # Add floating particles effect
        self.create_particles_effect()
    
    def create_animated_background(self):
        """Create animated gradient background"""
        self.bg_canvas = tk.Canvas(
            self.main_frame,
            highlightthickness=0,
            bg=ModernColors.GRAY_900
        )
        self.bg_canvas.pack(fill='both', expand=True)
        
        # Start background animation
        self.animate_background()
    
    def animate_background(self):
        """Animate the gradient background"""
        self.animation_step += 1
        
        canvas_width = self.bg_canvas.winfo_width()
        canvas_height = self.bg_canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            self.bg_canvas.delete("bg_gradient")
            
            # Create animated gradient
            for i in range(canvas_height):
                # Calculate animated color
                ratio = i / canvas_height
                time_factor = math.sin(self.animation_step * 0.02) * 0.1
                
                # Base gradient from purple to blue
                r = int(102 + (116 - 102) * (ratio + time_factor))
                g = int(126 + (75 - 126) * (ratio + time_factor))
                b = int(234 + (162 - 234) * (ratio + time_factor))
                
                # Clamp values
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.bg_canvas.create_line(
                    0, i, canvas_width, i, 
                    fill=color, tags="bg_gradient"
                )
        
        # Continue animation
        self.root.after(50, self.animate_background)
    
    def create_login_card(self):
        """Create floating glassmorphism login card"""
        # Card container with glassmorphism effect
        self.card_frame = tk.Frame(
            self.bg_canvas,
            bg=ModernColors.WHITE,
            relief='flat',
            bd=0,
            padx=0,
            pady=0
        )
        
        # Create card window
        self.card_window = self.bg_canvas.create_window(
            0, 0,
            window=self.card_frame,
            anchor='center'
        )
        
        # Update card position when canvas resizes
        def update_card_position(event=None):
            canvas_width = self.bg_canvas.winfo_width()
            canvas_height = self.bg_canvas.winfo_height()
            if canvas_width > 1 and canvas_height > 1:
                self.bg_canvas.coords(
                    self.card_window,
                    canvas_width // 2,
                    canvas_height // 2
                )
        
        self.bg_canvas.bind('<Configure>', update_card_position)
        self.root.after(100, update_card_position)
        
        # Card content
        self.create_card_content()
    
    def create_card_content(self):
        """Create the login card content"""
        # Card header with logo and title
        header_frame = tk.Frame(self.card_frame, bg=ModernColors.WHITE)
        header_frame.pack(pady=(40, 20))
        
        # Animated logo
        logo_frame = tk.Frame(header_frame, bg=ModernColors.WHITE)
        logo_frame.pack()
        
        self.logo_label = tk.Label(
            logo_frame,
            text="💬",
            font=('Segoe UI', 48),
            bg=ModernColors.WHITE,
            fg=ModernColors.PRIMARY
        )
        self.logo_label.pack()
        
        # Animate logo
        self.animate_logo()
        
        # App title
        title_label = tk.Label(
            header_frame,
            text="ChatBox",
            font=ModernFonts.DISPLAY_MEDIUM,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_800
        )
        title_label.pack(pady=(10, 0))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Connect • Chat • Collaborate",
            font=ModernFonts.BODY_MEDIUM,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_500
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Form section
        form_frame = tk.Frame(self.card_frame, bg=ModernColors.WHITE)
        form_frame.pack(pady=20, padx=40)
        
        # Welcome text
        welcome_label = tk.Label(
            form_frame,
            text="Welcome back!",
            font=ModernFonts.HEADLINE_SMALL,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_800
        )
        welcome_label.pack(pady=(0, 20))
        
        # Username field
        username_label = tk.Label(
            form_frame,
            text="Username",
            font=ModernFonts.LABEL_MEDIUM,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_600
        )
        username_label.pack(anchor='w', pady=(0, 5))
        
        self.username_frame, self.username_entry = ModernWidgets.create_modern_entry(
            form_frame, 
            placeholder="Enter your username",
            width=25
        )
        self.username_frame.pack(fill='x', pady=(0, 15))
        
        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password",
            font=ModernFonts.LABEL_MEDIUM,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_600
        )
        password_label.pack(anchor='w', pady=(0, 5))
        
        password_frame = tk.Frame(form_frame, bg=ModernColors.WHITE)
        password_frame.pack(fill='x', pady=(0, 20))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=ModernFonts.BODY_MEDIUM,
            bg=ModernColors.GRAY_50,
            fg=ModernColors.GRAY_800,
            relief='flat',
            bd=0,
            width=25,
            show='*',
            insertbackground=ModernColors.PRIMARY
        )
        self.password_entry.pack(padx=16, pady=12, ipady=8)
        
        # Add focus effects to password field
        def on_password_focus_in(e):
            password_frame.config(
                highlightbackground=ModernColors.PRIMARY,
                highlightcolor=ModernColors.PRIMARY,
                highlightthickness=2
            )
        
        def on_password_focus_out(e):
            password_frame.config(highlightthickness=0)
        
        self.password_entry.bind('<FocusIn>', on_password_focus_in)
        self.password_entry.bind('<FocusOut>', on_password_focus_out)
        
        # Login button
        self.login_btn = ModernWidgets.create_modern_button(
            form_frame,
            text="Sign In",
            command=self.handle_login,
            style='primary',
            size='large'
        )
        self.login_btn.pack(fill='x', pady=(0, 15))
        
        # Loading indicator
        self.loading_frame = tk.Frame(form_frame, bg=ModernColors.WHITE)
        
        self.loading_label = tk.Label(
            self.loading_frame,
            text="🔄 Connecting...",
            font=ModernFonts.BODY_MEDIUM,
            bg=ModernColors.WHITE,
            fg=ModernColors.PRIMARY
        )
        self.loading_label.pack()
        
        # Divider
        divider_frame = tk.Frame(form_frame, bg=ModernColors.WHITE)
        divider_frame.pack(fill='x', pady=15)
        
        divider_line = tk.Frame(divider_frame, bg=ModernColors.GRAY_200, height=1)
        divider_line.pack(fill='x')
        
        divider_text = tk.Label(
            divider_frame,
            text="or",
            font=ModernFonts.LABEL_SMALL,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_400
        )
        divider_text.place(relx=0.5, rely=0.5, anchor='center')
        
        # Register button
        register_btn = ModernWidgets.create_modern_button(
            form_frame,
            text="Create Account",
            command=self.on_switch_to_register,
            style='outline',
            size='large'
        )
        register_btn.pack(fill='x', pady=(15, 0))
        
        # Status message
        self.status_label = tk.Label(
            form_frame,
            text="",
            font=ModernFonts.BODY_SMALL,
            bg=ModernColors.WHITE,
            wraplength=300
        )
        self.status_label.pack(pady=(15, 0))
        
        # Footer
        footer_frame = tk.Frame(self.card_frame, bg=ModernColors.WHITE)
        footer_frame.pack(pady=(0, 30))
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2024 ChatBox. Made with ❤️",
            font=ModernFonts.LABEL_SMALL,
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_400
        )
        footer_label.pack()
        
        # Bind events
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
    
    def animate_logo(self):
        """Animate the logo with subtle rotation"""
        current_text = self.logo_label.cget('text')
        
        # Rotate through different chat emojis
        emojis = ['💬', '💭', '🗨️', '💬']
        current_index = emojis.index(current_text) if current_text in emojis else 0
        next_index = (current_index + 1) % len(emojis)
        
        self.logo_label.config(text=emojis[next_index])
        
        # Continue animation every 2 seconds
        self.root.after(2000, self.animate_logo)
    
    def create_particles_effect(self):
        """Create floating particles background effect"""
        # Simple particle effect - can be enhanced
        pass
    
    def handle_login(self):
        """Handle login with modern UX"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validate input
        if not username or username == "Enter your username":
            self.show_status("Please enter your username", "error")
            self.username_entry.focus()
            return
        
        if not password:
            self.show_status("Please enter your password", "error")
            self.password_entry.focus()
            return
        
        # Start loading state
        self.set_loading_state(True)
        
        # Connect in background
        threading.Thread(
            target=self._connect_to_server,
            args=(username, password),
            daemon=True
        ).start()
    
    def _connect_to_server(self, username, password):
        """Connect to server with error handling"""
        try:
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)  # 10 second timeout
            sock.connect(("127.0.0.1", 5000))
            
            # Send login request
            login_msg = f"LOGIN|{username}|SERVER|{password}|{datetime.now()}"
            sock.send(login_msg.encode('utf-8'))
            
            # Wait for response
            response = sock.recv(1024).decode('utf-8')
            
            if "LOGIN_OK" in response:
                # Success
                self.root.after(0, lambda: self.show_status("Login successful! 🎉", "success"))
                self.root.after(500, lambda: self.on_login_success(username, sock))
            else:
                # Failed
                self.root.after(0, lambda: self.show_status("Invalid username or password", "error"))
                self.root.after(0, lambda: self.set_loading_state(False))
                sock.close()
                
        except socket.timeout:
            self.root.after(0, lambda: self.show_status("Connection timeout. Please try again.", "error"))
            self.root.after(0, lambda: self.set_loading_state(False))
        except ConnectionRefusedError:
            self.root.after(0, lambda: self.show_status("Cannot connect to server. Is it running?", "error"))
            self.root.after(0, lambda: self.set_loading_state(False))
        except Exception as e:
            self.root.after(0, lambda: self.show_status(f"Connection error: {str(e)}", "error"))
            self.root.after(0, lambda: self.set_loading_state(False))
    
    def set_loading_state(self, loading):
        """Set loading state with animations"""
        self.is_loading = loading
        
        if loading:
            self.login_btn.config(state='disabled', text="Signing In...")
            self.loading_frame.pack(pady=(10, 0))
            self.animate_loading()
        else:
            self.login_btn.config(state='normal', text="Sign In")
            self.loading_frame.pack_forget()
    
    def animate_loading(self):
        """Animate loading indicator"""
        if self.is_loading:
            current_text = self.loading_label.cget('text')
            
            # Rotate loading animation
            animations = [
                "🔄 Connecting...",
                "⏳ Authenticating...",
                "✨ Almost there...",
                "🔄 Connecting..."
            ]
            
            try:
                current_index = animations.index(current_text)
                next_index = (current_index + 1) % len(animations)
                self.loading_label.config(text=animations[next_index])
            except ValueError:
                self.loading_label.config(text=animations[0])
            
            # Continue animation
            self.root.after(500, self.animate_loading)
    
    def show_status(self, message, msg_type="info"):
        """Show status message with modern styling"""
        colors = {
            "info": ModernColors.INFO,
            "success": ModernColors.SUCCESS,
            "error": ModernColors.ERROR,
            "warning": ModernColors.WARNING
        }
        
        self.status_label.config(
            text=message,
            fg=colors.get(msg_type, ModernColors.INFO)
        )
        
        # Auto-hide success messages
        if msg_type == "success":
            self.root.after(3000, lambda: self.status_label.config(text=""))
    
    def clear_form(self):
        """Clear form with animations"""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, "Enter your username")
        self.username_entry.config(fg=ModernColors.GRAY_400)
        
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="")
        self.set_loading_state(False)
    
    def show(self):
        """Show page with entrance animation"""
        self.main_frame.pack(fill='both', expand=True)
        
        # Focus on username field
        self.root.after(100, lambda: self.username_entry.focus())
        
        # Entrance animation
        ModernAnimations.fade_in(self.main_frame)
    
    def hide(self):
        """Hide page"""
        self.main_frame.pack_forget()