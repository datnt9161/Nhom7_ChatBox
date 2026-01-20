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
                
                # Make card responsive to window size
                if canvas_width < 600:
                    # Small screen - reduce card width
                    self.card_frame.config(width=canvas_width - 40)
                else:
                    # Normal screen
                    self.card_frame.config(width=450)
        
        self.bg_canvas.bind('<Configure>', update_card_position)
        self.root.after(100, update_card_position)
        
        # Card content
        self.create_card_content()
    
    def create_card_content(self):
        """Create the login card content"""
        # Card header with logo and title
        header_frame = tk.Frame(self.card_frame, bg=ModernColors.WHITE)
        header_frame.pack(pady=(30, 15))  # Giảm padding
        
        # Animated logo
        logo_frame = tk.Frame(header_frame, bg=ModernColors.WHITE)
        logo_frame.pack()
        
        self.logo_label = tk.Label(
            logo_frame,
            text="💬",
            font=('Segoe UI', 36),  # Giảm kích thước logo
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
            font=('Segoe UI', 24, 'bold'),  # Giảm kích thước title
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_900
        )
        title_label.pack(pady=(8, 0))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Connect • Chat • Collaborate",
            font=('Segoe UI', 11, 'normal'),  # Giảm kích thước subtitle
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_600
        )
        subtitle_label.pack(pady=(3, 0))
        
        # Form section
        form_frame = tk.Frame(self.card_frame, bg=ModernColors.WHITE)
        form_frame.pack(pady=15, padx=30)  # Giảm padding
        
        # Welcome text
        welcome_label = tk.Label(
            form_frame,
            text="Welcome back!",
            font=('Segoe UI', 16, 'bold'),  # Giảm kích thước
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_900
        )
        welcome_label.pack(pady=(0, 20))  # Tăng padding để tạo thêm khoảng trống
        
        # Username field
        username_label = tk.Label(
            form_frame,
            text="Username",
            font=('Segoe UI', 10, 'normal'),  # Giảm kích thước font
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_700
        )
        username_label.pack(anchor='w', pady=(0, 3))  # Giảm padding
        
        self.username_frame, self.username_entry = self.create_beautiful_entry(
            form_frame, 
            placeholder="Enter your username",
            width=25
        )
        self.username_frame.pack(fill='x', pady=(0, 18))  # Tăng padding
        
        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password",
            font=('Segoe UI', 10, 'normal'),  # Giảm kích thước font
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_700
        )
        password_label.pack(anchor='w', pady=(0, 3))  # Giảm padding
        
        # Beautiful password field
        self.password_frame = tk.Frame(form_frame, bg=ModernColors.WHITE)
        self.password_frame.pack(fill='x', pady=(0, 25))  # Tăng padding để tạo thêm khoảng trống
        
        # Outer container with border and shadow effect
        password_outer = tk.Frame(
            self.password_frame,
            bg=ModernColors.GRAY_200,
            relief='flat',
            bd=1
        )
        password_outer.pack(fill='x', padx=2, pady=2)
        
        # Inner container
        password_inner = tk.Frame(
            password_outer,
            bg=ModernColors.WHITE,
            relief='flat',
            bd=0
        )
        password_inner.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Password entry container
        password_entry_frame = tk.Frame(password_inner, bg=ModernColors.WHITE)
        password_entry_frame.pack(fill='x', padx=16, pady=8)  # Giảm padding từ 12 xuống 8
        
        self.password_entry = tk.Entry(
            password_entry_frame,
            font=('Segoe UI', 12, 'normal'),
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_900,
            relief='flat',
            bd=0,
            show='*',
            insertbackground=ModernColors.PRIMARY
        )
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=6)  # Giảm ipady từ 8 xuống 6
        
        # Eye button to toggle password visibility
        self.password_visible = False
        self.eye_button = tk.Button(
            password_entry_frame,
            text="👁️",
            font=('Segoe UI', 12),
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_600,
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.toggle_password_visibility
        )
        self.eye_button.pack(side='right', padx=(5, 0))
        
        # Add focus effects to password field
        def on_password_focus_in(e):
            password_outer.config(
                bg=ModernColors.PRIMARY,
                highlightbackground=ModernColors.PRIMARY,
                highlightcolor=ModernColors.PRIMARY,
                highlightthickness=1
            )
        
        def on_password_focus_out(e):
            password_outer.config(
                bg=ModernColors.GRAY_200,
                highlightthickness=0
            )
        
        self.password_entry.bind('<FocusIn>', on_password_focus_in)
        self.password_entry.bind('<FocusOut>', on_password_focus_out)
        
        # Login button
        login_btn_container = tk.Frame(form_frame, bg=ModernColors.WHITE)
        login_btn_container.pack(fill='x', pady=(10, 20))  # Tăng padding
        
        self.login_btn = tk.Button(
            login_btn_container,
            text="Sign In",
            command=self.handle_login,
            font=('Segoe UI', 12, 'bold'),
            bg=ModernColors.PRIMARY,
            fg=ModernColors.WHITE,
            relief='flat',
            bd=0,
            cursor='hand2',
            padx=32,
            pady=16
        )
        self.login_btn.pack(fill='x')
        
        # Add hover effect to login button
        def on_login_enter(e):
            self.login_btn.config(bg='#4f46e5')
        
        def on_login_leave(e):
            self.login_btn.config(bg=ModernColors.PRIMARY)
        
        self.login_btn.bind('<Enter>', on_login_enter)
        self.login_btn.bind('<Leave>', on_login_leave)
        
        # Loading indicator
        self.loading_frame = tk.Frame(form_frame, bg=ModernColors.WHITE)
        
        self.loading_label = tk.Label(
            self.loading_frame,
            text="🔄 Connecting...",
            font=('Segoe UI', 12, 'normal'),
            bg=ModernColors.WHITE,
            fg=ModernColors.PRIMARY
        )
        self.loading_label.pack()
        
        # Divider
        divider_frame = tk.Frame(form_frame, bg=ModernColors.WHITE)
        divider_frame.pack(fill='x', pady=20)  # Tăng padding
        
        divider_line = tk.Frame(divider_frame, bg=ModernColors.GRAY_200, height=1)
        divider_line.pack(fill='x')
        
        divider_text = tk.Label(
            divider_frame,
            text="or",
            font=('Segoe UI', 10, 'normal'),
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_500
        )
        divider_text.place(relx=0.5, rely=0.5, anchor='center')
        
        # Register button
        register_btn_container = tk.Frame(form_frame, bg=ModernColors.WHITE)
        register_btn_container.pack(fill='x', pady=(20, 10))  # Tăng padding
        
        register_btn = tk.Button(
            register_btn_container,
            text="Create Account",
            command=self.on_switch_to_register,
            font=('Segoe UI', 12, 'normal'),
            bg=ModernColors.WHITE,
            fg=ModernColors.PRIMARY,
            relief='flat',
            bd=1,
            cursor='hand2',
            padx=32,
            pady=16,
            highlightbackground=ModernColors.PRIMARY,
            highlightcolor=ModernColors.PRIMARY,
            highlightthickness=1
        )
        register_btn.pack(fill='x')
        
        # Add hover effect to register button
        def on_register_enter(e):
            register_btn.config(bg=ModernColors.GRAY_50)
        
        def on_register_leave(e):
            register_btn.config(bg=ModernColors.WHITE)
        
        register_btn.bind('<Enter>', on_register_enter)
        register_btn.bind('<Leave>', on_register_leave)
        
        # Status message
        self.status_label = tk.Label(
            form_frame,
            text="",
            font=('Segoe UI', 10, 'normal'),
            bg=ModernColors.WHITE,
            wraplength=300
        )
        self.status_label.pack(pady=(20, 40))  # Tăng padding để tạo thêm khoảng trống
        
        # Bind events
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
    
    def create_beautiful_entry(self, parent, placeholder="", width=30):
        """Create beautiful entry field with modern design"""
        # Main container
        main_frame = tk.Frame(parent, bg=ModernColors.WHITE)
        
        # Outer container with border and shadow effect
        outer_frame = tk.Frame(
            main_frame,
            bg=ModernColors.GRAY_200,
            relief='flat',
            bd=1
        )
        outer_frame.pack(fill='x', padx=2, pady=2)
        
        # Inner container
        inner_frame = tk.Frame(
            outer_frame,
            bg=ModernColors.WHITE,
            relief='flat',
            bd=0
        )
        inner_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Entry field
        entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 12, 'normal'),
            bg=ModernColors.WHITE,
            fg=ModernColors.GRAY_900,
            relief='flat',
            bd=0,
            insertbackground=ModernColors.PRIMARY
        )
        entry.pack(fill='x', padx=16, pady=8, ipady=6)  # Giảm padding và ipady để match với password field
        
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
            outer_frame.config(
                bg=ModernColors.PRIMARY,
                highlightbackground=ModernColors.PRIMARY,
                highlightcolor=ModernColors.PRIMARY,
                highlightthickness=1
            )
        
        def on_focus_out_border(e):
            outer_frame.config(
                bg=ModernColors.GRAY_200,
                highlightthickness=0
            )
        
        entry.bind('<FocusIn>', on_focus_in_border)
        entry.bind('<FocusOut>', on_focus_out_border)
        
        return main_frame, entry
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_visible:
            # Hide password
            self.password_entry.config(show='*')
            self.eye_button.config(text="👁️", fg=ModernColors.GRAY_600)
            self.password_visible = False
        else:
            # Show password
            self.password_entry.config(show='')
            self.eye_button.config(text="🙈", fg=ModernColors.PRIMARY)
            self.password_visible = True
    
    def animate_logo(self):
        """Animate the logo with subtle rotation"""
        current_text = self.logo_label.cget('text')
        
        # Rotate through different chat emojis
        emojis = ['💬']
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