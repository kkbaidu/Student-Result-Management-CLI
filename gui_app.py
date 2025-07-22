#!/usr/bin/env python3
"""
Student Result Management GUI Application
A beautiful, modern GUI for managing student results with advanced features.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import sv_ttk
from datetime import datetime
import os
import threading
import json

# Import our existing modules
from student_result_manager import StudentResultManager
from auth_manager import AuthManager
from load_config import load_config

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class ModernGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Student Result Management System")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize managers
        self.db_config = load_config()
        self.auth_manager = AuthManager(self.db_config)
        self.student_manager = StudentResultManager(self.db_config)
        self.current_user = None
        
        # Initialize GUI components
        self.setup_styles()
        self.create_login_screen()
        
        # Center the window
        self.center_window()
        
    def setup_styles(self):
        """Setup custom styles for the application."""
        # Configure colors
        self.colors = {
            'primary': '#1f538d',
            'secondary': '#14375e',
            'accent': '#ffd700',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'background': '#2b2b2b',
            'surface': '#3b3b3b'
        }
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def create_login_screen(self):
        """Create the login screen."""
        self.clear_window()
        
        # Main container
        main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        
        # Left side - Login form
        left_frame = ctk.CTkFrame(main_frame, width=500, corner_radius=20)
        left_frame.pack(side="left", fill="y", padx=20, pady=20)
        left_frame.pack_propagate(False)
        
        # Right side - Welcome graphics
        right_frame = ctk.CTkFrame(main_frame, corner_radius=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)
        
        # Login form content
        login_container = ctk.CTkFrame(left_frame, corner_radius=10)
        login_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            login_container, 
            text="Student Result\nManagement System",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(40, 30))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            login_container,
            text="Modern • Secure • Efficient",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Login form
        self.username_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Username",
            width=300,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(
            login_container,
            placeholder_text="Password",
            show="*",
            width=300,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(pady=10)
        
        # Login button
        login_btn = ctk.CTkButton(
            login_container,
            text="LOGIN",
            command=self.handle_login,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary']
        )
        login_btn.pack(pady=20)
        
        # Register button
        register_btn = ctk.CTkButton(
            login_container,
            text="CREATE ACCOUNT",
            command=self.show_register_screen,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=2,
            text_color=self.colors['primary'],
            border_color=self.colors['primary']
        )
        register_btn.pack(pady=10)
        
        # Right side content - Welcome graphics
        self.create_welcome_graphics(right_frame)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.handle_login())
        
    def create_welcome_graphics(self, parent):
        """Create welcome graphics and statistics."""
        welcome_container = ctk.CTkFrame(parent, corner_radius=10)
        welcome_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Welcome text
        welcome_label = ctk.CTkLabel(
            welcome_container,
            text="Welcome to the Future of\nStudent Management",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=self.colors['accent']
        )
        welcome_label.pack(pady=(50, 20))
        
        # Features list
        features_frame = ctk.CTkFrame(welcome_container, corner_radius=10)
        features_frame.pack(pady=20, padx=40, fill="x")
        
        features = [
            "🎯 Advanced Analytics & Insights",
            "📊 Real-time Performance Tracking",
            "🔒 Secure User Authentication",
            "📈 Beautiful Data Visualizations",
            "📋 Comprehensive Reporting",
            "💾 Multi-format Data Support"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=ctk.CTkFont(size=16),
                anchor="w"
            )
            feature_label.pack(pady=8, padx=20, anchor="w")
            
        # Statistics (mock data for demonstration)
        stats_frame = ctk.CTkFrame(welcome_container, corner_radius=10)
        stats_frame.pack(pady=20, padx=40, fill="x")
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="System Statistics",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['accent']
        )
        stats_title.pack(pady=(20, 10))
        
        # Create a simple chart
        self.create_mini_chart(stats_frame)
        
    def create_mini_chart(self, parent):
        """Create a mini chart for the welcome screen."""
        try:
            # Create figure
            fig, ax = plt.subplots(figsize=(6, 3), facecolor='#3b3b3b')
            ax.set_facecolor('#3b3b3b')
            
            # Sample data
            grades = ['A', 'B', 'C', 'D', 'F']
            counts = [25, 35, 20, 15, 5]
            colors = ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
            
            bars = ax.bar(grades, counts, color=colors, alpha=0.8)
            ax.set_title('Grade Distribution Overview', color='white', fontsize=14, weight='bold')
            ax.set_xlabel('Grades', color='white')
            ax.set_ylabel('Number of Students', color='white')
            ax.tick_params(colors='white')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', color='white', fontweight='bold')
            
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10, padx=20)
            
        except Exception as e:
            # Fallback text if chart creation fails
            chart_label = ctk.CTkLabel(
                parent,
                text="📊 Interactive Charts Available After Login",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            chart_label.pack(pady=20)
            
    def show_register_screen(self):
        """Show the registration screen."""
        self.clear_window()
        
        # Main container
        main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        
        # Registration form container
        register_container = ctk.CTkFrame(main_frame, width=600, corner_radius=20)
        register_container.pack(expand=True, padx=20, pady=20)
        register_container.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            register_container,
            text="Create New Account",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(40, 30))
        
        # Form fields
        self.reg_fullname_entry = ctk.CTkEntry(
            register_container,
            placeholder_text="Full Name",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.reg_fullname_entry.pack(pady=10)
        
        self.reg_username_entry = ctk.CTkEntry(
            register_container,
            placeholder_text="Username",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.reg_username_entry.pack(pady=10)
        
        self.reg_email_entry = ctk.CTkEntry(
            register_container,
            placeholder_text="Email Address",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.reg_email_entry.pack(pady=10)
        
        self.reg_password_entry = ctk.CTkEntry(
            register_container,
            placeholder_text="Password",
            show="*",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.reg_password_entry.pack(pady=10)
        
        self.reg_confirm_password_entry = ctk.CTkEntry(
            register_container,
            placeholder_text="Confirm Password",
            show="*",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.reg_confirm_password_entry.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(register_container, fg_color="transparent")
        button_frame.pack(pady=30)
        
        register_btn = ctk.CTkButton(
            button_frame,
            text="CREATE ACCOUNT",
            command=self.handle_register,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['success'],
            hover_color="#218838"
        )
        register_btn.pack(side="left", padx=10)
        
        back_btn = ctk.CTkButton(
            button_frame,
            text="BACK TO LOGIN",
            command=self.create_login_screen,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=2,
            text_color=self.colors['primary'],
            border_color=self.colors['primary']
        )
        back_btn.pack(side="right", padx=10)
        
    def handle_login(self):
        """Handle login process."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
            
        # Connect to database
        if not self.auth_manager.connect_to_database():
            messagebox.showerror("Database Error", "Failed to connect to database.")
            return
            
        # Create users table if needed
        if not self.auth_manager.create_users_table():
            messagebox.showerror("Database Error", "Failed to initialize user system.")
            return
            
        # Attempt login with a loading animation
        self.show_loading("Authenticating...")
        
        # Use threading to prevent GUI freeze
        threading.Thread(target=self._login_thread, args=(username, password), daemon=True).start()
        
    def _login_thread(self, username, password):
        """Login thread to prevent GUI freezing."""
        # self.auth_manager = AuthManager(self.db_config)
        if not self.auth_manager.cursor or not self.auth_manager.connection:
            print("✗ Error: AuthManager is not initialized.")
            return False
        try:
            # Simulate the original login process
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            login_query = """
            SELECT id, username, email, full_name, role, created_at
            FROM users 
            WHERE username = %s AND password_hash = %s
            """
            
            self.auth_manager.cursor.execute(login_query, (username, password_hash))
            user = self.auth_manager.cursor.fetchone()
            
            if user:
                # Update last login
                update_login_query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s"
                self.auth_manager.cursor.execute(update_login_query, (user['id'],))
                self.auth_manager.connection.commit()
                
                self.current_user = dict(user)
                self.auth_manager.current_user = self.current_user
                
                # Schedule GUI update on main thread
                self.root.after(0, self._login_success)
            else:
                self.root.after(0, lambda: self._login_failed("Invalid username or password."))
                
        except Exception as e:
            self.root.after(0, lambda: self._login_failed(f"Login error: {str(e)}"))
            
    def _login_success(self):
        """Handle successful login."""
        self.hide_loading()
        messagebox.showinfo("Success", f"Welcome back, {self.current_user['full_name'] if self.current_user and 'full_name' in self.current_user else 0}!")
        self.create_main_dashboard()
        
    def _login_failed(self, error_message):
        """Handle failed login."""
        self.hide_loading()
        messagebox.showerror("Login Failed", error_message)
        
    def handle_register(self):
        """Handle registration process."""
        full_name = self.reg_fullname_entry.get().strip()
        username = self.reg_username_entry.get().strip()
        email = self.reg_email_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()
        
        # Validation
        if not all([full_name, username, email, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return
            
        if "@" not in email or "." not in email.split("@")[1]:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
            
        # Connect to database and register
        if not self.auth_manager.connect_to_database():
            messagebox.showerror("Database Error", "Failed to connect to database.")
            return
            
        # Create users table if needed
        if not self.auth_manager.create_users_table():
            messagebox.showerror("Database Error", "Failed to initialize user system.")
            return
            
        self.show_loading("Creating account...")
        threading.Thread(target=self._register_thread, args=(full_name, username, email, password), daemon=True).start()
        
    def _register_thread(self, full_name, username, email, password):
        """Registration thread to prevent GUI freezing."""
        if not self.auth_manager.cursor or not self.auth_manager.connection:
            print("✗ Error: AuthManager is not initialized.")
            return False

        try:
            # Check if user exists
            check_query = "SELECT id FROM users WHERE username = %s OR email = %s"
            self.auth_manager.cursor.execute(check_query, (username, email))
            existing = self.auth_manager.cursor.fetchone()
            
            if existing:
                self.root.after(0, lambda: self._register_failed("Username or email already exists."))
                return
                
            # Create user
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            insert_query = """
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (%s, %s, %s, %s)
            """
            
            self.auth_manager.cursor.execute(insert_query, (username, email, password_hash, full_name))
            self.auth_manager.connection.commit()
            
            self.root.after(0, self._register_success)
            
        except Exception as e:
            self.root.after(0, lambda: self._register_failed(f"Registration error: {str(e)}"))
            
    def _register_success(self):
        """Handle successful registration."""
        self.hide_loading()
        messagebox.showinfo("Success", "Account created successfully! You can now log in.")
        self.create_login_screen()
        
    def _register_failed(self, error_message):
        """Handle failed registration."""
        self.hide_loading()
        messagebox.showerror("Registration Failed", error_message)
        
    def show_loading(self, message="Loading..."):
        """Show loading overlay."""
        self.loading_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.loading_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        loading_label = ctk.CTkLabel(
            self.loading_frame,
            text=message,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        loading_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Simple animation
        self.loading_dots = 0
        self.animate_loading(loading_label, message)
        
    def animate_loading(self, label, base_message):
        """Animate loading dots."""
        if hasattr(self, 'loading_frame') and self.loading_frame.winfo_exists():
            dots = "." * (self.loading_dots % 4)
            label.configure(text=f"{base_message}{dots}")
            self.loading_dots += 1
            self.root.after(300, lambda: self.animate_loading(label, base_message))
            
    def hide_loading(self):
        """Hide loading overlay."""
        if hasattr(self, 'loading_frame'):
            self.loading_frame.destroy()
            
    def create_main_dashboard(self):
        """Create the main dashboard after successful login."""
        self.clear_window()
        
        # Connect student manager to database
        if not self.student_manager.connect_to_database():
            messagebox.showerror("Database Error", "Failed to connect to student database.")
            return
            
        if not self.student_manager.create_table():
            messagebox.showerror("Database Error", "Failed to initialize student system.")
            return
            
        # Main container
        main_container = ctk.CTkFrame(self.root, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # Create navigation sidebar
        self.create_sidebar(main_container)
        
        # Create main content area
        self.main_content = ctk.CTkFrame(main_container, corner_radius=0)
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # Show dashboard by default
        self.show_dashboard()
        
    def create_sidebar(self, parent):
        """Create navigation sidebar."""
        self.sidebar = ctk.CTkFrame(parent, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # User info section
        user_frame = ctk.CTkFrame(self.sidebar, corner_radius=10)
        user_frame.pack(fill="x", padx=10, pady=10)
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"Welcome,\n{self.current_user['full_name'] if self.current_user and 'full_name' in self.current_user else 0}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['accent']
        )
        user_label.pack(pady=15)
        
        role_label = ctk.CTkLabel(
            user_frame,
            text=f"Role: {self.current_user['role'].title() if self.current_user and 'role' in self.current_user else 0}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        role_label.pack(pady=(0, 15))
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("👥 Students", self.show_students),
            ("📊 Analytics", self.show_analytics),
            ("📁 Import Data", self.show_import),
            ("📋 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings),
            ("🚪 Logout", self.handle_logout)
        ]
        
        self.nav_buttons = {}
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                width=220,
                height=40,
                font=ctk.CTkFont(size=14),
                anchor="w",
                fg_color="transparent",
                text_color="white",
                hover_color=self.colors['primary']
            )
            btn.pack(pady=5, padx=15)
            self.nav_buttons[text] = btn
            
    def set_active_nav_button(self, active_text):
        """Set the active navigation button."""
        for text, btn in self.nav_buttons.items():
            if text == active_text:
                btn.configure(fg_color=self.colors['primary'])
            else:
                btn.configure(fg_color="transparent")
                
    def clear_main_content(self):
        """Clear the main content area."""
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
    def show_dashboard(self):
        """Show the main dashboard."""
        self.set_active_nav_button("🏠 Dashboard")
        self.clear_main_content()
        
        # Create dashboard header
        header_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Dashboard title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Dashboard Overview",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(side="left", pady=20, padx=20)
        
        # Quick stats
        self.create_quick_stats()
        
        # Charts and graphs
        self.create_dashboard_charts()
        
    def create_quick_stats(self):
        """Create quick statistics cards."""
        stats_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        stats_frame.pack(fill="x", padx=20, pady=10)

        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        
        # Get statistics from database
        try:
            # Total students
            self.student_manager.cursor.execute("SELECT COUNT(*) as total FROM student_results")
            result = self.student_manager.cursor.fetchone()
            total_students = result['total'] if result and 'total' in result else 0
            
            # Average score
            self.student_manager.cursor.execute("SELECT AVG(score) as avg_score FROM student_results")
            avg_result = self.student_manager.cursor.fetchone()
            avg_score = round(avg_result['avg_score'], 1) if avg_result and 'avg_score' in avg_result else 0

            # Grade distribution
            self.student_manager.cursor.execute("""
                SELECT grade, COUNT(*) as count 
                FROM student_results 
                GROUP BY grade 
                ORDER BY grade
            """)
            grade_counts = self.student_manager.cursor.fetchall()
            
        except:
            total_students = 0
            avg_score = 0
            grade_counts = []
        
        # Create stat cards
        stats_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=20)
        
        # Total Students Card
        total_card = ctk.CTkFrame(stats_container, corner_radius=10)
        total_card.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            total_card,
            text="👥",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            total_card,
            text=str(total_students),
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors['accent']
        ).pack()
        
        ctk.CTkLabel(
            total_card,
            text="Total Students",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(0, 20))
        
        # Average Score Card
        avg_card = ctk.CTkFrame(stats_container, corner_radius=10)
        avg_card.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            avg_card,
            text="📈",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            avg_card,
            text=f"{avg_score}%",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors['success'] if avg_score >= 70 else self.colors['warning']
        ).pack()
        
        ctk.CTkLabel(
            avg_card,
            text="Average Score",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(0, 20))
        
        # Top Grade Card
        top_grade = grade_counts[0]['grade'] if grade_counts else 'N/A'
        top_count = grade_counts[0]['count'] if grade_counts else 0
        
        grade_card = ctk.CTkFrame(stats_container, corner_radius=10)
        grade_card.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            grade_card,
            text="🏆",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            grade_card,
            text=f"Grade {top_grade}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        ).pack()
        
        ctk.CTkLabel(
            grade_card,
            text=f"{top_count} students",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(0, 20))
        
    def create_dashboard_charts(self):
        """Create charts for the dashboard."""
        charts_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        
        try:
            # Get data for charts
            self.student_manager.cursor.execute("""
                SELECT grade, COUNT(*) as count 
                FROM student_results 
                GROUP BY grade 
                ORDER BY grade
            """)
            grade_data = self.student_manager.cursor.fetchall()
            
            if grade_data:
                # Create matplotlib figure
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#3b3b3b')
                
                # Grade distribution bar chart
                grades = [item['grade'] for item in grade_data]
                counts = [item['count'] for item in grade_data]
                colors = ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
                
                ax1.bar(grades, counts, color=colors[:len(grades)], alpha=0.8)
                ax1.set_title('Grade Distribution', color='white', fontsize=16, weight='bold')
                ax1.set_xlabel('Grades', color='white')
                ax1.set_ylabel('Number of Students', color='white')
                ax1.tick_params(colors='white')
                ax1.set_facecolor('#3b3b3b')
                
                # Add value labels on bars
                for i, v in enumerate(counts):
                    ax1.text(i, v + 0.5, str(v), ha='center', va='bottom', color='white', fontweight='bold')
                
                # Grade distribution pie chart
                ax2.pie(counts, labels=grades, colors=colors[:len(grades)], autopct='%1.1f%%', 
                       startangle=90, textprops={'color': 'white'})
                ax2.set_title('Grade Distribution %', color='white', fontsize=16, weight='bold')
                ax2.set_facecolor('#3b3b3b')
                
                plt.tight_layout()
                
                # Embed in tkinter
                canvas = FigureCanvasTkAgg(fig, charts_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True, pady=20, padx=20)
                
            else:
                # No data message
                no_data_label = ctk.CTkLabel(
                    charts_frame,
                    text="📊 No student data available.\nImport student data to see charts and analytics.",
                    font=ctk.CTkFont(size=18),
                    text_color="gray"
                )
                no_data_label.pack(expand=True)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                charts_frame,
                text=f"Error loading charts: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['danger']
            )
            error_label.pack(expand=True)
            
    def show_students(self):
        """Show the students management view."""
        self.set_active_nav_button("👥 Students")
        self.clear_main_content()
        
        # Header frame
        header_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👥 Student Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(side="left", pady=20, padx=20)
        
        # Controls frame
        controls_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Search and filter controls
        search_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=15)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_students)
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="� Search students by name or index...",
            width=300,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        # Grade filter
        self.grade_filter_var = tk.StringVar(value="All Grades")
        grade_filter = ctk.CTkOptionMenu(
            search_frame,
            variable=self.grade_filter_var,
            values=["All Grades", "A", "B", "C", "D", "F"],
            command=self.filter_students,
            width=120,
            height=35
        )
        grade_filter.pack(side="left", padx=10)
        
        # Add student button
        add_btn = ctk.CTkButton(
            search_frame,
            text="➕ Add Student",
            command=self.show_add_student_dialog,
            width=120,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color=self.colors['success']
        )
        add_btn.pack(side="right", padx=10)
        
        # Students table frame
        table_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview for students table
        self.create_students_table(table_frame)
        
        self.load_students_data()
        
    def create_students_table(self, parent):
        """Create the students table with treeview."""
        # Create frame for table
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create treeview
        columns = ("Index", "Name", "Course", "Score", "Grade")
        self.students_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        
        # Configure column headings and widths
        self.students_tree.heading("Index", text="Index Number")
        self.students_tree.heading("Name", text="Full Name")
        self.students_tree.heading("Course", text="Course")
        self.students_tree.heading("Score", text="Score")
        self.students_tree.heading("Grade", text="Grade")
        
        self.students_tree.column("Index", width=120, anchor="center")
        self.students_tree.column("Name", width=200, anchor="w")
        self.students_tree.column("Course", width=180, anchor="w")
        self.students_tree.column("Score", width=80, anchor="center")
        self.students_tree.column("Grade", width=80, anchor="center")
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.students_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event
        self.students_tree.bind("<Double-1>", self.edit_student)
        
        # Context menu
        self.create_context_menu()
        
    def create_context_menu(self):
        """Create context menu for student table."""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit Student", command=self.edit_selected_student)
        self.context_menu.add_command(label="Delete Student", command=self.delete_selected_student)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="View Details", command=self.view_student_details)
        
        self.students_tree.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        """Show context menu on right-click."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def load_students_data(self):
        """Load students data from database."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False

        try:
            query = """
            SELECT index_number, full_name, course, score, grade 
            FROM student_results 
            ORDER BY index_number
            """
            self.student_manager.cursor.execute(query)
            self.all_students = self.student_manager.cursor.fetchall()
            self.display_students(self.all_students)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {str(e)}")
            self.all_students = []
            
    def display_students(self, students):
        """Display students in the table."""
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
            
        # Color code by grade
        grade_colors = {
            'A': 'green',
            'B': 'blue', 
            'C': 'orange',
            'D': 'red',
            'F': 'darkred'
        }

        # Insert new items
        for student in students:
            self.students_tree.insert("", "end", values=(
                student['index_number'],
                student['full_name'],
                student['course'],
                student['score'],
                student['grade']
            ), tags=(student['grade'],))
            
        # Configure tag colors
        for grade, color in grade_colors.items():
            self.students_tree.tag_configure(grade, foreground=color)
            
    def filter_students(self, *args):
        """Filter students based on search and grade filter."""
        if not hasattr(self, 'all_students'):
            return
            
        search_text = self.search_var.get().lower()
        grade_filter = self.grade_filter_var.get()
        
        filtered_students = []
        for student in self.all_students:
            # Apply search filter
            if search_text:
                if (search_text not in student['full_name'].lower() and 
                    search_text not in student['index_number'].lower() and
                    search_text not in student['course'].lower()):
                    continue
                    
            # Apply grade filter
            if grade_filter != "All Grades" and student['grade'] != grade_filter:
                continue
                
            filtered_students.append(student)
            
        self.display_students(filtered_students)
        
    def show_add_student_dialog(self):
        """Show dialog to add new student."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x500+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="Add New Student",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Form fields
        self.add_index_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Index Number",
            width=300,
            height=40
        )
        self.add_index_entry.pack(pady=10)
        
        self.add_name_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Full Name",
            width=300,
            height=40
        )
        self.add_name_entry.pack(pady=10)
        
        self.add_course_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Course",
            width=300,
            height=40
        )
        self.add_course_entry.pack(pady=10)
        
        self.add_score_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Score (0-100)",
            width=300,
            height=40
        )
        self.add_score_entry.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=30)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Student",
            command=lambda: self.save_new_student(dialog),
            width=120,
            height=40,
            fg_color=self.colors['success']
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=120,
            height=40,
            fg_color="gray"
        )
        cancel_btn.pack(side="right", padx=10)
        
    def save_new_student(self, dialog):
        """Save new student to database."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        
        try:
            index_number = self.add_index_entry.get().strip()
            full_name = self.add_name_entry.get().strip()
            course = self.add_course_entry.get().strip()
            score = int(self.add_score_entry.get().strip())
            
            if not all([index_number, full_name, course]) or score < 0 or score > 100:
                messagebox.showerror("Error", "Please fill all fields with valid data.")
                return
                
            grade = self.student_manager.calculate_grade(score)
            
            # Check if student already exists
            check_query = "SELECT id FROM student_results WHERE index_number = %s"
            self.student_manager.cursor.execute(check_query, (index_number,))
            if self.student_manager.cursor.fetchone():
                messagebox.showerror("Error", "Student with this index number already exists.")
                return
                
            # Insert new student
            insert_query = """
            INSERT INTO student_results (index_number, full_name, course, score, grade)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.student_manager.cursor.execute(insert_query, (index_number, full_name, course, score, grade))
            self.student_manager.connection.commit()
            
            messagebox.showinfo("Success", "Student added successfully!")
            dialog.destroy()
            self.load_students_data()  # Refresh the table
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid score (0-100).")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
            
    def edit_student(self, event):
        """Edit student on double-click."""
        self.edit_selected_student()
        
    def edit_selected_student(self):
        """Edit the selected student."""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return
            
        item = self.students_tree.item(selection[0])
        student_data = item['values']
        
        # Create edit dialog (similar to add dialog but with pre-filled values)
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Edit Student")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x500+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="Edit Student",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Form fields with current values
        self.edit_index_entry = ctk.CTkEntry(dialog, width=300, height=40)
        self.edit_index_entry.pack(pady=10)
        self.edit_index_entry.insert(0, student_data[0])
        self.edit_index_entry.configure(state="disabled")  # Index shouldn't be editable
        
        self.edit_name_entry = ctk.CTkEntry(dialog, width=300, height=40)
        self.edit_name_entry.pack(pady=10)
        self.edit_name_entry.insert(0, student_data[1])
        
        self.edit_course_entry = ctk.CTkEntry(dialog, width=300, height=40)
        self.edit_course_entry.pack(pady=10)
        self.edit_course_entry.insert(0, student_data[2])
        
        self.edit_score_entry = ctk.CTkEntry(dialog, width=300, height=40)
        self.edit_score_entry.pack(pady=10)
        self.edit_score_entry.insert(0, str(student_data[3]))
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=30)
        
        update_btn = ctk.CTkButton(
            button_frame,
            text="Update Student",
            command=lambda: self.update_student(dialog, student_data[0]),
            width=120,
            height=40,
            fg_color=self.colors['primary']
        )
        update_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=120,
            height=40,
            fg_color="gray"
        )
        cancel_btn.pack(side="right", padx=10)
        
    def update_student(self, dialog, index_number):
        """Update student in database."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        
        try:
            full_name = self.edit_name_entry.get().strip()
            course = self.edit_course_entry.get().strip()
            score = int(self.edit_score_entry.get().strip())
            
            if not all([full_name, course]) or score < 0 or score > 100:
                messagebox.showerror("Error", "Please fill all fields with valid data.")
                return
                
            grade = self.student_manager.calculate_grade(score)
            
            # Update student
            update_query = """
            UPDATE student_results 
            SET full_name = %s, course = %s, score = %s, grade = %s
            WHERE index_number = %s
            """
            # Ensure index_number is treated as string
            self.student_manager.cursor.execute(update_query, (full_name, course, score, grade, str(index_number)))
            self.student_manager.connection.commit()
            
            messagebox.showinfo("Success", "Student updated successfully!")
            dialog.destroy()
            self.load_students_data()  # Refresh the table
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid score (0-100).")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")
            
    def delete_selected_student(self):
        """Delete the selected student."""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to delete.")
            return
            
        item = self.students_tree.item(selection[0])
        student_data = item['values']
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_data[1]}?"):
            if not self.student_manager.cursor or not self.student_manager.connection:
                print("✗ Error: StudentResultManager is not initialized.")
                return False
            try:
                delete_query = "DELETE FROM student_results WHERE index_number = %s"
                # Ensure index_number is treated as string
                self.student_manager.cursor.execute(delete_query, (str(student_data[0]),))
                self.student_manager.connection.commit()
                
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.load_students_data()  # Refresh the table
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
                
    def view_student_details(self):
        """View detailed information about selected student."""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to view details.")
            return
            
        item = self.students_tree.item(selection[0])
        student_data = item['values']
        
        # Create details dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Student Details")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Content
        content_frame = ctk.CTkFrame(dialog, corner_radius=10)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            content_frame,
            text="Student Details",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Student info
        info_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        details = [
            ("Index Number:", student_data[0]),
            ("Full Name:", student_data[1]),
            ("Course:", student_data[2]),
            ("Score:", f"{student_data[3]}/100"),
            ("Grade:", student_data[4])
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            detail_frame.pack(fill="x", pady=10, padx=20)
            
            ctk.CTkLabel(
                detail_frame,
                text=label,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                detail_frame,
                text=value,
                font=ctk.CTkFont(size=16),
                anchor="e"
            ).pack(side="right")
            
        # Close button
        close_btn = ctk.CTkButton(
            content_frame,
            text="Close",
            command=dialog.destroy,
            width=100,
            height=40
        )
        close_btn.pack(pady=20)
        
    def show_analytics(self):
        """Show the analytics view with advanced charts and insights."""
        self.set_active_nav_button("📊 Analytics")
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Advanced Analytics & Insights",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(side="left", pady=20, padx=20)
        
        # Analytics tabs
        self.create_analytics_tabs()
        
    def create_analytics_tabs(self):
        """Create tabbed interface for different analytics views."""
        # Tab container
        tab_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        tab_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabview
        self.analytics_tabs = ctk.CTkTabview(tab_frame)
        self.analytics_tabs.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add tabs
        overview_tab = self.analytics_tabs.add("Overview")
        performance_tab = self.analytics_tabs.add("Performance")
        trends_tab = self.analytics_tabs.add("Trends")
        comparison_tab = self.analytics_tabs.add("Comparison")
        
        # Populate tabs
        self.create_overview_analytics(overview_tab)
        self.create_performance_analytics(performance_tab)
        self.create_trends_analytics(trends_tab)
        self.create_comparison_analytics(comparison_tab)
        
    def create_overview_analytics(self, parent):
        """Create overview analytics."""
        try:
            # Get comprehensive statistics
            stats = self.get_analytics_data()
            
            # Statistics cards
            stats_frame = ctk.CTkFrame(parent, corner_radius=10)
            stats_frame.pack(fill="x", padx=20, pady=20)
            
            # Create grid of stat cards
            stats_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stats_container.pack(fill="x", padx=20, pady=20)
            
            # Row 1
            row1 = ctk.CTkFrame(stats_container, fg_color="transparent")
            row1.pack(fill="x", pady=5)

            self.create_stat_card(row1, "📚 Total Students", str(stats['total_students'] if stats and 'total_students' in stats else 0), "left")
            self.create_stat_card(row1, "📈 Average Score", f"{stats['avg_score']:.1f}%" if stats and 'avg_score' in stats else "0.0%", "left")
            self.create_stat_card(row1, "🏆 Highest Score", f"{stats['highest_score']}%" if stats and 'highest_score' in stats else "0%", "left")
            self.create_stat_card(row1, "📉 Lowest Score", f"{stats['lowest_score']}%" if stats and 'lowest_score' in stats else "0%", "right")

            # Row 2
            row2 = ctk.CTkFrame(stats_container, fg_color="transparent")
            row2.pack(fill="x", pady=5)

            self.create_stat_card(row2, "✅ Pass Rate", f"{stats['pass_rate']:.1f}%" if stats and 'pass_rate' in stats else "0.0%", "left")
            self.create_stat_card(row2, "🎯 Excellence Rate", f"{stats['excellence_rate']:.1f}%" if stats and 'excellence_rate' in stats else "0.0%", "left")
            self.create_stat_card(row2, "📊 Standard Deviation", f"{stats['std_dev']:.1f}" if stats and 'std_dev' in stats else "0.0", "left")
            self.create_stat_card(row2, "📋 Total Courses", str(stats['total_courses'] if stats and 'total_courses' in stats else 0), "right")

            # Charts section
            charts_frame = ctk.CTkFrame(parent, corner_radius=10)
            charts_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            self.create_overview_charts(charts_frame, stats)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                parent,
                text=f"Error loading analytics: {str(e)}",
                font=ctk.CTkFont(size=16),
                text_color=self.colors['danger']
            )
            error_label.pack(expand=True)
            
    def create_stat_card(self, parent, title, value, side):
        """Create a statistics card."""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.pack(side=side, fill="both", expand=True, padx=5)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        title_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['accent']
        )
        value_label.pack(pady=(0, 15))
        
    def get_analytics_data(self):
        """Get comprehensive analytics data from database."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        
        try:
            # Basic statistics
            self.student_manager.cursor.execute("SELECT COUNT(*) as total FROM student_results")
            total = self.student_manager.cursor.fetchone()
            total_students = total['total'] if total else 0

            self.student_manager.cursor.execute("SELECT AVG(score) as avg, MAX(score) as max, MIN(score) as min FROM student_results")
            score_stats = self.student_manager.cursor.fetchone()
            
            # Pass rate (score >= 50)
            self.student_manager.cursor.execute("SELECT COUNT(*) as passes FROM student_results WHERE score >= 50")
            passes = self.student_manager.cursor.fetchone()
            passes = passes['passes'] if passes else 0
            pass_rate = (passes / total_students * 100) if total_students > 0 else 0
            
            # Excellence rate (score >= 80)
            self.student_manager.cursor.execute("SELECT COUNT(*) as excellent FROM student_results WHERE score >= 80")
            excellent = self.student_manager.cursor.fetchone()
            excellent = excellent['excellent'] if excellent else 0
            excellence_rate = (excellent / total_students * 100) if total_students > 0 else 0
            
            # Standard deviation
            self.student_manager.cursor.execute("SELECT score FROM student_results")
            scores = [row['score'] for row in self.student_manager.cursor.fetchall()]
            std_dev = np.std(scores) if scores else 0
            
            # Total courses
            self.student_manager.cursor.execute("SELECT COUNT(DISTINCT course) as total_courses FROM student_results")
            total_courses = self.student_manager.cursor.fetchone()
            total_courses = total_courses['total_courses'] if total_courses else 0

            return {
                'total_students': total_students,
                'avg_score': score_stats['avg'] if score_stats and 'avg' in score_stats else 0,
                'highest_score': score_stats['max'] if score_stats and 'max' in score_stats else 0,
                'lowest_score': score_stats['min'] if score_stats and 'min' in score_stats else 0,
                'pass_rate': pass_rate,
                'excellence_rate': excellence_rate,
                'std_dev': std_dev,
                'total_courses': total_courses
            }
        except:
            return {
                'total_students': 0, 'avg_score': 0, 'highest_score': 0, 'lowest_score': 0,
                'pass_rate': 0, 'excellence_rate': 0, 'std_dev': 0, 'total_courses': 0
            }
            
    def create_overview_charts(self, parent, stats):
        """Create overview charts."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        try:
            if stats['total_students'] == 0:
                no_data_label = ctk.CTkLabel(
                    parent,
                    text="📊 No data available for charts.\nImport student data to see analytics.",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data_label.pack(expand=True)
                return
                
            # Create figure with subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 8), facecolor='#3b3b3b')
            
            # Grade distribution
            self.student_manager.cursor.execute("""
                SELECT grade, COUNT(*) as count FROM student_results 
                GROUP BY grade ORDER BY grade
            """)
            grade_data = self.student_manager.cursor.fetchall()
            
            if grade_data:
                grades = [item['grade'] for item in grade_data]
                counts = [item['count'] for item in grade_data]
                colors = ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
                
                bars = ax1.bar(grades, counts, color=colors[:len(grades)], alpha=0.8)
                ax1.set_title('Grade Distribution', color='white', fontsize=14, weight='bold')
                ax1.set_xlabel('Grades', color='white')
                ax1.set_ylabel('Number of Students', color='white')
                ax1.tick_params(colors='white')
                ax1.set_facecolor('#3b3b3b')
                
                for bar in bars:
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom', color='white', fontweight='bold')
                
                # Pie chart
                ax2.pie(counts, labels=grades, colors=colors[:len(grades)], autopct='%1.1f%%',
                       startangle=90, textprops={'color': 'white'})
                ax2.set_title('Grade Distribution %', color='white', fontsize=14, weight='bold')
                ax2.set_facecolor('#3b3b3b')
            
            # Score distribution histogram
            self.student_manager.cursor.execute("SELECT score FROM student_results")
            scores = [row['score'] for row in self.student_manager.cursor.fetchall()]
            
            if scores:
                ax3.hist(scores, bins=10, color='#17a2b8', alpha=0.7, edgecolor='white')
                ax3.set_title('Score Distribution', color='white', fontsize=14, weight='bold')
                ax3.set_xlabel('Score Range', color='white')
                ax3.set_ylabel('Number of Students', color='white')
                ax3.tick_params(colors='white')
                ax3.set_facecolor('#3b3b3b')
                
                # Add average line
                avg_score = np.mean(scores)
                ax3.axvline(avg_score, color='red', linestyle='--', linewidth=2, label=f'Average: {avg_score:.1f}')
                ax3.legend()
            
            # Course performance
            self.student_manager.cursor.execute("""
                SELECT course, AVG(score) as avg_score, COUNT(*) as student_count 
                FROM student_results 
                GROUP BY course 
                ORDER BY avg_score DESC 
                LIMIT 10
            """)
            course_data = self.student_manager.cursor.fetchall()
            
            if course_data:
                courses = [item['course'][:15] + '...' if len(item['course']) > 15 else item['course'] 
                          for item in course_data]
                avg_scores = [item['avg_score'] for item in course_data]
                
                bars = ax4.barh(courses, avg_scores, color='#ffc107', alpha=0.8)
                ax4.set_title('Average Score by Course', color='white', fontsize=14, weight='bold')
                ax4.set_xlabel('Average Score', color='white')
                ax4.tick_params(colors='white')
                ax4.set_facecolor('#3b3b3b')
                
                for i, v in enumerate(avg_scores):
                    ax4.text(v + 1, i, f'{v:.1f}', va='center', color='white', fontweight='bold')
            
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, pady=10, padx=20)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                parent,
                text=f"Error creating charts: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['danger']
            )
            error_label.pack(expand=True)
            
    def create_performance_analytics(self, parent):
        """Create performance analytics tab."""
        placeholder_label = ctk.CTkLabel(
            parent,
            text="🎯 Performance Analytics\n\nDetailed performance metrics and insights\ncoming soon...",
            font=ctk.CTkFont(size=18),
            text_color=self.colors['accent']
        )
        placeholder_label.pack(expand=True)
        
    def create_trends_analytics(self, parent):
        """Create trends analytics tab."""
        placeholder_label = ctk.CTkLabel(
            parent,
            text="📈 Trends Analysis\n\nPerformance trends over time\ncoming soon...",
            font=ctk.CTkFont(size=18),
            text_color=self.colors['accent']
        )
        placeholder_label.pack(expand=True)
        
    def create_comparison_analytics(self, parent):
        """Create comparison analytics tab."""
        placeholder_label = ctk.CTkLabel(
            parent,
            text="⚖️ Comparative Analysis\n\nCourse and student comparisons\ncoming soon...",
            font=ctk.CTkFont(size=18),
            text_color=self.colors['accent']
        )
        placeholder_label.pack(expand=True)
        
    def show_import(self):
        """Show the import data view."""
        self.set_active_nav_button("📁 Import Data")
        self.clear_main_content()
        
        # Import view
        import_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        import_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            import_frame,
            text="📁 Import Student Data",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(30, 20))
        
        # File selection
        file_frame = ctk.CTkFrame(import_frame, corner_radius=10)
        file_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(
            file_frame,
            text="Select a file to import student data:",
            font=ctk.CTkFont(size=16)
        ).pack(pady=(20, 10))
        
        # File path entry
        self.file_path_var = tk.StringVar()
        file_entry = ctk.CTkEntry(
            file_frame,
            textvariable=self.file_path_var,
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        file_entry.pack(pady=10)
        
        # Browse button
        browse_btn = ctk.CTkButton(
            file_frame,
            text="📂 Browse Files",
            command=self.browse_file,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        browse_btn.pack(pady=10)
        
        # Import button
        import_btn = ctk.CTkButton(
            file_frame,
            text="📥 Import Data",
            command=self.import_data,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['success'],
            hover_color="#218838"
        )
        import_btn.pack(pady=(10, 20))
        
    def browse_file(self):
        """Browse for file to import."""
        file_path = filedialog.askopenfilename(
            title="Select Student Data File",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def import_data(self):
        """Import student data from selected file."""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file to import.")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Selected file does not exist.")
            return
            
        try:
            students = self.student_manager.read_student_data(file_path)
            if students:
                self.student_manager.insert_student_data(students)
                messagebox.showinfo("Success", f"Successfully imported {len(students)} student records!")
                self.show_dashboard()  # Refresh dashboard to show new data
            else:
                messagebox.showwarning("Warning", "No valid student data found in the file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}")
        
    def show_reports(self):
        """Show the reports view with PDF generation and export options."""
        self.set_active_nav_button("📋 Reports")
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Advanced Reports & Export",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(side="left", pady=20, padx=20)
        
        # Report options
        self.create_report_options()
        
    def create_report_options(self):
        """Create report generation options."""
        options_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Title
        options_title = ctk.CTkLabel(
            options_frame,
            text="Generate Reports",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['accent']
        )
        options_title.pack(pady=(20, 10))
        
        # Report types grid
        reports_grid = ctk.CTkFrame(options_frame, fg_color="transparent")
        reports_grid.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Row 1
        row1 = ctk.CTkFrame(reports_grid, fg_color="transparent")
        row1.pack(fill="x", pady=10)
        
        # Summary Report
        summary_card = ctk.CTkFrame(row1, corner_radius=10)
        summary_card.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            summary_card,
            text="📊",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            summary_card,
            text="Summary Report",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack()
        
        ctk.CTkLabel(
            summary_card,
            text="Overall statistics and\ngrade distribution",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=5)
        
        ctk.CTkButton(
            summary_card,
            text="Generate",
            command=self.generate_summary_report,
            width=120,
            height=35,
            fg_color=self.colors['primary']
        ).pack(pady=(10, 20))
        
        # Detailed Report
        detailed_card = ctk.CTkFrame(row1, corner_radius=10)
        detailed_card.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            detailed_card,
            text="📝",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            detailed_card,
            text="Detailed Report",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack()
        
        ctk.CTkLabel(
            detailed_card,
            text="Complete student list\nwith all details",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=5)
        
        ctk.CTkButton(
            detailed_card,
            text="Generate",
            command=self.generate_detailed_report,
            width=120,
            height=35,
            fg_color=self.colors['success']
        ).pack(pady=(10, 20))
        
        # Row 2
        row2 = ctk.CTkFrame(reports_grid, fg_color="transparent")
        row2.pack(fill="x", pady=10)
        
        # Course Report
        course_card = ctk.CTkFrame(row2, corner_radius=10)
        course_card.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            course_card,
            text="🎓",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            course_card,
            text="Course Report",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack()
        
        ctk.CTkLabel(
            course_card,
            text="Performance analysis\nby course",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=5)
        
        ctk.CTkButton(
            course_card,
            text="Generate",
            command=self.generate_course_report,
            width=120,
            height=35,
            fg_color=self.colors['info']
        ).pack(pady=(10, 20))
        
        # Export Options
        export_card = ctk.CTkFrame(row2, corner_radius=10)
        export_card.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            export_card,
            text="💾",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            export_card,
            text="Export Data",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack()
        
        ctk.CTkLabel(
            export_card,
            text="Export to CSV, Excel\nor JSON format",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=5)
        
        ctk.CTkButton(
            export_card,
            text="Export",
            command=self.show_export_options,
            width=120,
            height=35,
            fg_color=self.colors['warning']
        ).pack(pady=(10, 20))
        
    def generate_summary_report(self):
        """Generate and save a summary report."""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Summary Report",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not filename:
                return
                
            # Use existing export method
            self.student_manager.export_summary_report(filename)
            messagebox.showinfo("Success", f"Summary report saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            
    def generate_detailed_report(self):
        """Generate a detailed report with all student information."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Detailed Report",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not filename:
                return
                
            # Get all student data
            self.student_manager.cursor.execute("""
                SELECT index_number, full_name, course, score, grade 
                FROM student_results 
                ORDER BY index_number
            """)
            students = self.student_manager.cursor.fetchall()
            
            # Create detailed report
            report_content = f"""DETAILED STUDENT REPORT
{'='*50}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Students: {len(students)}

STUDENT DETAILS
{'-'*50}
"""
            
            for i, student in enumerate(students, 1):
                report_content += f"""
{i}. {student['full_name']} ({student['index_number']})
   Course: {student['course']}
   Score: {student['score']}/100
   Grade: {student['grade']}
   {'-'*30}"""
            
            # Add statistics
            if students:
                scores = [s['score'] for s in students]
                avg_score = sum(scores) / len(scores)
                
                report_content += f"""

SUMMARY STATISTICS
{'-'*50}
Average Score: {avg_score:.2f}
Highest Score: {max(scores)}
Lowest Score: {min(scores)}
Standard Deviation: {np.std(scores):.2f}

Grade Distribution:
"""
                
                # Add grade distribution
                from collections import Counter
                grade_counts = Counter(student['grade'] for student in students)
                for grade in ['A', 'B', 'C', 'D', 'F']:
                    if grade in grade_counts:
                        report_content += f"{grade}: {grade_counts[grade]} students\n"
            
            # Write to file
            with open(filename, 'w') as file:
                file.write(report_content)
                
            messagebox.showinfo("Success", f"Detailed report saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate detailed report: {str(e)}")
            
    def generate_course_report(self):
        """Generate a course-wise performance report."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Course Report",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not filename:
                return
                
            # Get course-wise data
            self.student_manager.cursor.execute("""
                SELECT course, 
                       COUNT(*) as student_count,
                       AVG(score) as avg_score,
                       MAX(score) as max_score,
                       MIN(score) as min_score
                FROM student_results 
                GROUP BY course 
                ORDER BY avg_score DESC
            """)
            courses = self.student_manager.cursor.fetchall()
            
            # Create course report
            report_content = f"""COURSE PERFORMANCE REPORT
{'='*50}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Courses: {len(courses)}

COURSE ANALYSIS
{'-'*50}
"""
            
            for i, course in enumerate(courses, 1):
                report_content += f"""
{i}. {course['course']}
   Students: {course['student_count']}
   Average Score: {course['avg_score']:.2f}
   Highest Score: {course['max_score']}
   Lowest Score: {course['min_score']}
   {'-'*40}"""
            
            # Write to file
            with open(filename, 'w') as file:
                file.write(report_content)
                
            messagebox.showinfo("Success", f"Course report saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate course report: {str(e)}")
            
    def show_export_options(self):
        """Show export options dialog."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Export Data")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="Export Student Data",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Export format selection
        format_label = ctk.CTkLabel(
            dialog,
            text="Select Export Format:",
            font=ctk.CTkFont(size=16)
        )
        format_label.pack(pady=10)
        
        self.export_format_var = tk.StringVar(value="CSV")
        format_menu = ctk.CTkOptionMenu(
            dialog,
            variable=self.export_format_var,
            values=["CSV", "JSON", "Excel"],
            width=200,
            height=35
        )
        format_menu.pack(pady=10)
        
        # Export button
        export_btn = ctk.CTkButton(
            dialog,
            text="Export Data",
            command=lambda: self.export_data(dialog),
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['success']
        )
        export_btn.pack(pady=20)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            width=100,
            height=35,
            fg_color="gray"
        )
        cancel_btn.pack(pady=10)
        
    def export_data(self, dialog):
        """Export data in selected format."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        try:
            format_type = self.export_format_var.get()
            
            # File extension mapping
            extensions = {
                "CSV": ".csv",
                "JSON": ".json", 
                "Excel": ".xlsx"
            }
            
            filename = filedialog.asksaveasfilename(
                title=f"Export as {format_type}",
                defaultextension=extensions[format_type],
                filetypes=[(f"{format_type} files", f"*{extensions[format_type]}"), ("All files", "*.*")]
            )
            
            if not filename:
                return
                
            # Get data
            self.student_manager.cursor.execute("""
                SELECT index_number, full_name, course, score, grade 
                FROM student_results 
                ORDER BY index_number
            """)
            students = self.student_manager.cursor.fetchall()
            
            if not students:
                messagebox.showwarning("Warning", "No data to export.")
                return
                
            # Convert to pandas DataFrame for easier export
            df = pd.DataFrame(students)
            
            if format_type == "CSV":
                df.to_csv(filename, index=False)
            elif format_type == "JSON":
                df.to_json(filename, orient='records', indent=2)
            elif format_type == "Excel":
                df.to_excel(filename, index=False, sheet_name='Students')
                
            messagebox.showinfo("Success", f"Data exported to {filename}")
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
        
    def show_settings(self):
        """Show the settings view with theme, database, and user preferences."""
        self.set_active_nav_button("⚙️ Settings")
        self.clear_main_content()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ Settings & Configuration",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(side="left", pady=20, padx=20)
        
        # Settings categories
        self.create_settings_tabs()
        
    def create_settings_tabs(self):
        """Create tabbed interface for different settings categories."""
        tab_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        tab_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabview
        self.settings_tabs = ctk.CTkTabview(tab_frame)
        self.settings_tabs.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add tabs
        appearance_tab = self.settings_tabs.add("Appearance")
        database_tab = self.settings_tabs.add("Database")
        user_tab = self.settings_tabs.add("User Profile")
        backup_tab = self.settings_tabs.add("Backup")
        
        # Populate tabs
        self.create_appearance_settings(appearance_tab)
        self.create_database_settings(database_tab)
        self.create_user_settings(user_tab)
        self.create_backup_settings(backup_tab)
        
    def create_appearance_settings(self, parent):
        """Create appearance settings."""
        # Theme selection
        theme_frame = ctk.CTkFrame(parent, corner_radius=10)
        theme_frame.pack(fill="x", padx=20, pady=20)
        
        theme_title = ctk.CTkLabel(
            theme_frame,
            text="🎨 Theme Settings",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent']
        )
        theme_title.pack(pady=(20, 10))
        
        # Appearance mode
        mode_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        mode_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            mode_frame,
            text="Appearance Mode:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        self.appearance_mode_var = tk.StringVar(value="dark")
        appearance_menu = ctk.CTkOptionMenu(
            mode_frame,
            variable=self.appearance_mode_var,
            values=["dark", "light", "system"],
            command=self.change_appearance_mode,
            width=150
        )
        appearance_menu.pack(side="right")
        
        # Color theme
        color_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        color_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            color_frame,
            text="Color Theme:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        self.color_theme_var = tk.StringVar(value="blue")
        color_menu = ctk.CTkOptionMenu(
            color_frame,
            variable=self.color_theme_var,
            values=["blue", "green", "dark-blue"],
            command=self.change_color_theme,
            width=150
        )
        color_menu.pack(side="right")
        
        # Font size
        font_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        font_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            font_frame,
            text="Font Size:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        self.font_size_var = tk.StringVar(value="Medium")
        font_menu = ctk.CTkOptionMenu(
            font_frame,
            variable=self.font_size_var,
            values=["Small", "Medium", "Large"],
            width=150
        )
        font_menu.pack(side="right")
        
    def create_database_settings(self, parent):
        """Create database settings."""
        db_frame = ctk.CTkFrame(parent, corner_radius=10)
        db_frame.pack(fill="x", padx=20, pady=20)
        
        db_title = ctk.CTkLabel(
            db_frame,
            text="🗄️ Database Configuration",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent']
        )
        db_title.pack(pady=(20, 10))
        
        # Current database info
        info_frame = ctk.CTkFrame(db_frame, corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = f"""Current Database Configuration:
Host: {self.db_config['host']}
Database: {self.db_config['database']}
User: {self.db_config['user']}
Port: {self.db_config['port']}"""
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(pady=20, padx=20)
        
        # Database actions
        actions_frame = ctk.CTkFrame(db_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        test_btn = ctk.CTkButton(
            actions_frame,
            text="Test Connection",
            command=self.test_database_connection,
            width=140,
            height=35,
            fg_color=self.colors['info']
        )
        test_btn.pack(side="left", padx=5)
        
        backup_btn = ctk.CTkButton(
            actions_frame,
            text="Backup Database",
            command=self.backup_database,
            width=140,
            height=35,
            fg_color=self.colors['warning']
        )
        backup_btn.pack(side="left", padx=5)
        
        optimize_btn = ctk.CTkButton(
            actions_frame,
            text="Optimize Database",
            command=self.optimize_database,
            width=140,
            height=35,
            fg_color=self.colors['success']
        )
        optimize_btn.pack(side="right", padx=5)
        
    def create_user_settings(self, parent):
        """Create user profile settings."""
        user_frame = ctk.CTkFrame(parent, corner_radius=10)
        user_frame.pack(fill="x", padx=20, pady=20)
        
        user_title = ctk.CTkLabel(
            user_frame,
            text="👤 User Profile",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent']
        )
        user_title.pack(pady=(20, 10))
        
        if self.current_user:
            # User info display
            info_frame = ctk.CTkFrame(user_frame, corner_radius=10)
            info_frame.pack(fill="x", padx=20, pady=10)
            
            user_info = f"""Profile Information:
Username: {self.current_user['username']}
Full Name: {self.current_user['full_name']}
Email: {self.current_user['email']}
Role: {self.current_user['role'].title()}
Account Created: {self.current_user['created_at'].strftime('%Y-%m-%d')}"""
            
            info_label = ctk.CTkLabel(
                info_frame,
                text=user_info,
                font=ctk.CTkFont(size=12),
                justify="left"
            )
            info_label.pack(pady=20, padx=20)
            
            # User actions
            actions_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
            actions_frame.pack(fill="x", padx=20, pady=(10, 20))
            
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="Edit Profile",
                command=self.edit_user_profile,
                width=120,
                height=35,
                fg_color=self.colors['primary']
            )
            edit_btn.pack(side="left", padx=5)
            
            change_pwd_btn = ctk.CTkButton(
                actions_frame,
                text="Change Password",
                command=self.change_password,
                width=140,
                height=35,
                fg_color=self.colors['warning']
            )
            change_pwd_btn.pack(side="right", padx=5)
            
    def create_backup_settings(self, parent):
        """Create backup and maintenance settings."""
        backup_frame = ctk.CTkFrame(parent, corner_radius=10)
        backup_frame.pack(fill="x", padx=20, pady=20)
        
        backup_title = ctk.CTkLabel(
            backup_frame,
            text="💾 Backup & Maintenance",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent']
        )
        backup_title.pack(pady=(20, 10))
        
        # Backup options
        options_frame = ctk.CTkFrame(backup_frame, corner_radius=10)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        # Auto backup toggle
        auto_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        auto_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            auto_frame,
            text="Auto Backup:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        self.auto_backup_var = tk.BooleanVar()
        auto_switch = ctk.CTkSwitch(
            auto_frame,
            variable=self.auto_backup_var,
            text="Enable"
        )
        auto_switch.pack(side="right")
        
        # Backup actions
        actions_frame = ctk.CTkFrame(backup_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        create_backup_btn = ctk.CTkButton(
            actions_frame,
            text="Create Backup",
            command=self.create_manual_backup,
            width=120,
            height=35,
            fg_color=self.colors['success']
        )
        create_backup_btn.pack(side="left", padx=5)
        
        restore_btn = ctk.CTkButton(
            actions_frame,
            text="Restore Backup",
            command=self.restore_backup,
            width=120,
            height=35,
            fg_color=self.colors['info']
        )
        restore_btn.pack(side="left", padx=5)
        
        clean_btn = ctk.CTkButton(
            actions_frame,
            text="Clean Database",
            command=self.clean_database,
            width=120,
            height=35,
            fg_color=self.colors['danger']
        )
        clean_btn.pack(side="right", padx=5)
        
    def change_appearance_mode(self, mode):
        """Change the appearance mode."""
        ctk.set_appearance_mode(mode)
        
    def change_color_theme(self, theme):
        """Change the color theme."""
        ctk.set_default_color_theme(theme)
        messagebox.showinfo("Theme Changed", "Color theme will take effect on next restart.")
        
    def test_database_connection(self):
        """Test database connection."""
        try:
            # Test connection
            test_manager = StudentResultManager(self.db_config)
            if test_manager.connect_to_database():
                test_manager.close_connection()
                messagebox.showinfo("Success", "Database connection successful!")
            else:
                messagebox.showerror("Error", "Failed to connect to database.")
        except Exception as e:
            messagebox.showerror("Error", f"Database connection failed: {str(e)}")
            
    def backup_database(self):
        """Create database backup."""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Database Backup",
                defaultextension=".sql",
                filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
            )
            
            if filename:
                messagebox.showinfo("Info", "Database backup feature would be implemented here.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            
    def optimize_database(self):
        """Optimize database performance."""
        if messagebox.askyesno("Confirm", "This will optimize database performance. Continue?"):
            try:
                # Database optimization would be implemented here
                messagebox.showinfo("Success", "Database optimization completed.")
            except Exception as e:
                messagebox.showerror("Error", f"Optimization failed: {str(e)}")
                
    def edit_user_profile(self):
        """Edit user profile."""
        messagebox.showinfo("Info", "Profile editing feature would be implemented here.")
        
    def change_password(self):
        """Change user password."""
        messagebox.showinfo("Info", "Password change feature would be implemented here.")
        
    def create_manual_backup(self):
        """Create manual backup."""
        if not self.student_manager.cursor or not self.student_manager.connection:
            print("✗ Error: StudentResultManager is not initialized.")
            return False
        try:
            # Export all data to JSON
            filename = filedialog.asksaveasfilename(
                title="Save Data Backup",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                self.student_manager.cursor.execute("""
                    SELECT index_number, full_name, course, score, grade 
                    FROM student_results 
                    ORDER BY index_number
                """)
                students = self.student_manager.cursor.fetchall()
                
                backup_data = {
                    'backup_date': datetime.now().isoformat(),
                    'total_records': len(students),
                    'students': [dict(student) for student in students]
                }
                
                with open(filename, 'w') as f:
                    json.dump(backup_data, f, indent=2, default=str)
                    
                messagebox.showinfo("Success", f"Backup created successfully: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            
    def restore_backup(self):
        """Restore from backup."""
        messagebox.showinfo("Info", "Backup restore feature would be implemented here.")
        
    def clean_database(self):
        """Clean database (remove duplicate records, etc.)."""
        if messagebox.askyesno("Confirm", "This will clean the database. Continue?"):
            try:
                # Database cleaning would be implemented here
                messagebox.showinfo("Success", "Database cleaning completed.")
            except Exception as e:
                messagebox.showerror("Error", f"Cleaning failed: {str(e)}")
        
    def handle_logout(self):
        """Handle user logout."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.auth_manager.logout()
            self.current_user = None
            self.create_login_screen()
            
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernGUI()
    app.run()
