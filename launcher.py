#!/usr/bin/env python3
"""
Student Result Management System Launcher
Choose between CLI and GUI interface modes.
"""

import sys
import os
from colorama import init, Fore, Back, Style
import pyfiglet

# Initialize colorama for cross-platform colored terminal text
try:
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

def print_colored(text, color=None, style=None):
    """Print colored text if colorama is available."""
    if COLORAMA_AVAILABLE and color:
        if style:
            print(f"{style}{color}{text}{Style.RESET_ALL}")
        else:
            print(f"{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def create_banner():
    """Create an attractive banner for the launcher."""
    try:
        # Create ASCII art title
        title = pyfiglet.figlet_format("STUDENT RESULT\nMANAGEMENT", font="slant")
        if COLORAMA_AVAILABLE:
            print(f"{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        else:
            print(title)
    except ImportError:
        # Fallback if pyfiglet is not available
        title = """
╔══════════════════════════════════════════════════════════════╗
║                    STUDENT RESULT MANAGEMENT                  ║
║                         SYSTEM                               ║
╚══════════════════════════════════════════════════════════════╝
"""
        print_colored(title, Fore.CYAN if COLORAMA_AVAILABLE else None, Style.BRIGHT if COLORAMA_AVAILABLE else None)

def create_menu():
    """Create the main launcher menu."""
    menu = """
┌──────────────────────────────────────────────────────────────┐
│                     🚀 LAUNCH OPTIONS                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 🖥️  CLI Mode    - Command Line Interface                 │
│                     Classic terminal-based interaction       │
│                                                              │
│  2. 🖼️  GUI Mode    - Graphical User Interface               │
│                     Modern, beautiful desktop application    │
│                                                              │
│  3. 📊 Quick Stats  - View system statistics                 │
│                                                              │
│  4. ⚙️  Setup       - Initial system setup                   │
│                                                              │
│  5. 📋 Help         - Show help and documentation            │
│                                                              │
│  6. 🚪 Exit         - Quit launcher                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
    print_colored(menu, Fore.WHITE if COLORAMA_AVAILABLE else None)

def show_system_info():
    """Display system information and requirements."""
    info = """
╔══════════════════════════════════════════════════════════════╗
║                      SYSTEM INFORMATION                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 Features:                                                ║
║     • Secure user authentication                            ║
║     • PostgreSQL database integration                       ║
║     • Advanced analytics and reporting                      ║
║     • Multi-format data import/export                       ║
║     • Beautiful charts and visualizations                   ║
║     • Real-time performance tracking                        ║
║                                                              ║
║  🔧 Requirements:                                            ║
║     • Python 3.7+                                           ║
║     • PostgreSQL database                                   ║
║     • Required packages (see requirements.txt)              ║
║                                                              ║
║  📁 Data Formats Supported:                                 ║
║     • TXT, CSV, JSON, Excel                                 ║
║     • Automatic format detection                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print_colored(info, Fore.GREEN if COLORAMA_AVAILABLE else None)

def show_quick_stats():
    """Show quick system statistics."""
    try:
        from load_config import load_config
        from student_result_manager import StudentResultManager
        
        db_config = load_config()
        manager = StudentResultManager(db_config)
        
        if manager.connect_to_database():
            try:
                # Get basic stats
                manager.cursor.execute("SELECT COUNT(*) as total FROM student_results")
                total_students = manager.cursor.fetchone()['total']
                
                manager.cursor.execute("SELECT AVG(score) as avg FROM student_results")
                avg_result = manager.cursor.fetchone()
                avg_score = round(avg_result['avg'], 1) if avg_result['avg'] else 0
                
                manager.cursor.execute("SELECT COUNT(DISTINCT course) as courses FROM student_results")
                total_courses = manager.cursor.fetchone()['courses']
                
                stats = f"""
╔══════════════════════════════════════════════════════════════╗
║                      QUICK STATISTICS                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 Current Data:                                            ║
║     • Total Students: {total_students:<10}                           ║
║     • Average Score:  {avg_score}%                           ║
║     • Total Courses:  {total_courses:<10}                            ║
║                                                              ║
║  🔗 Database Status:  ✅ Connected                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
                print_colored(stats, Fore.BLUE if COLORAMA_AVAILABLE else None)
                manager.close_connection()
                
            except Exception as e:
                error_stats = f"""
╔══════════════════════════════════════════════════════════════╗
║                      QUICK STATISTICS                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ⚠️  No student data found                                   ║
║     Import data to see statistics                           ║
║                                                              ║
║  🔗 Database Status:  ✅ Connected                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
                print_colored(error_stats, Fore.YELLOW if COLORAMA_AVAILABLE else None)
                manager.close_connection()
        else:
            error_msg = """
╔══════════════════════════════════════════════════════════════╗
║                         ERROR                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ❌ Cannot connect to database                               ║
║     Please check your configuration in config.env           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
            print_colored(error_msg, Fore.RED if COLORAMA_AVAILABLE else None)
            
    except Exception as e:
        error_msg = f"""
╔══════════════════════════════════════════════════════════════╗
║                         ERROR                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ❌ Error accessing database: {str(e)[:30]}...              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print_colored(error_msg, Fore.RED if COLORAMA_AVAILABLE else None)

def show_help():
    """Show help and documentation."""
    help_text = """
╔══════════════════════════════════════════════════════════════╗
║                      HELP & DOCUMENTATION                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🖥️  CLI Mode:                                               ║
║     Classic command-line interface with menu-driven         ║
║     navigation. Perfect for server environments or          ║
║     users who prefer terminal interfaces.                   ║
║                                                              ║
║  🖼️  GUI Mode:                                               ║
║     Modern graphical interface with:                        ║
║     • Beautiful dashboard with charts                       ║
║     • Interactive student management                        ║
║     • Advanced analytics and insights                       ║
║     • Export capabilities (PDF, Excel, CSV)                 ║
║     • Real-time data visualization                          ║
║                                                              ║
║  📁 Data Import:                                             ║
║     Supports multiple formats:                              ║
║     • Text files (.txt) - comma-separated                   ║
║     • CSV files (.csv)                                      ║
║     • JSON files (.json)                                    ║
║     • Excel files (.xlsx)                                   ║
║                                                              ║
║  🔧 Setup Requirements:                                      ║
║     1. Install PostgreSQL database                          ║
║     2. Configure database settings in config.env            ║
║     3. Install Python dependencies                          ║
║     4. Run setup.sh for initial configuration               ║
║                                                              ║
║  📋 Sample Data Format:                                      ║
║     Index, Full Name, Course, Score                         ║
║     20250001, John Doe, Computer Science, 85                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print_colored(help_text, Fore.CYAN if COLORAMA_AVAILABLE else None)

def run_setup():
    """Run initial system setup."""
    print_colored("\n🔧 Starting System Setup...", Fore.YELLOW if COLORAMA_AVAILABLE else None, Style.BRIGHT if COLORAMA_AVAILABLE else None)
    
    setup_steps = """
╔══════════════════════════════════════════════════════════════╗
║                      SETUP CHECKLIST                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. ✅ Check Python version                                  ║
║  2. ✅ Check required packages                               ║
║  3. 🔄 Test database connection                              ║
║  4. 🔄 Initialize database tables                            ║
║  5. 🔄 Create sample data (optional)                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print_colored(setup_steps, Fore.BLUE if COLORAMA_AVAILABLE else None)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 7:
        print_colored("✅ Python version: OK", Fore.GREEN if COLORAMA_AVAILABLE else None)
    else:
        print_colored("❌ Python 3.7+ required", Fore.RED if COLORAMA_AVAILABLE else None)
        return
    
    # Test database connection
    try:
        from load_config import load_config
        from student_result_manager import StudentResultManager
        from auth_manager import AuthManager
        
        print_colored("🔄 Testing database connection...", Fore.YELLOW if COLORAMA_AVAILABLE else None)
        
        db_config = load_config()
        manager = StudentResultManager(db_config)
        auth_manager = AuthManager(db_config)
        
        if manager.connect_to_database() and auth_manager.connect_to_database():
            print_colored("✅ Database connection: OK", Fore.GREEN if COLORAMA_AVAILABLE else None)
            
            # Initialize tables
            print_colored("🔄 Initializing database tables...", Fore.YELLOW if COLORAMA_AVAILABLE else None)
            if manager.create_table() and auth_manager.create_users_table():
                print_colored("✅ Database tables: OK", Fore.GREEN if COLORAMA_AVAILABLE else None)
            else:
                print_colored("❌ Failed to create tables", Fore.RED if COLORAMA_AVAILABLE else None)
                
            manager.close_connection()
            auth_manager.close_connection()
            
            print_colored("\n🎉 Setup completed successfully!", Fore.GREEN if COLORAMA_AVAILABLE else None, Style.BRIGHT if COLORAMA_AVAILABLE else None)
            
        else:
            print_colored("❌ Database connection failed", Fore.RED if COLORAMA_AVAILABLE else None)
            print_colored("   Please check config.env file", Fore.RED if COLORAMA_AVAILABLE else None)
            
    except Exception as e:
        print_colored(f"❌ Setup error: {str(e)}", Fore.RED if COLORAMA_AVAILABLE else None)

def launch_cli():
    """Launch the CLI version."""
    print_colored("\n🖥️  Launching CLI Mode...", Fore.GREEN if COLORAMA_AVAILABLE else None, Style.BRIGHT if COLORAMA_AVAILABLE else None)
    try:
        from main import main
        main()
    except KeyboardInterrupt:
        print_colored("\n\n👋 CLI session ended.", Fore.YELLOW if COLORAMA_AVAILABLE else None)
    except Exception as e:
        print_colored(f"❌ Error launching CLI: {str(e)}", Fore.RED if COLORAMA_AVAILABLE else None)

def launch_gui():
    """Launch the GUI version."""
    print_colored("\n🖼️  Launching GUI Mode...", Fore.GREEN if COLORAMA_AVAILABLE else None, Style.BRIGHT if COLORAMA_AVAILABLE else None)
    try:
        # Check if required GUI packages are available
        import customtkinter as ctk
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        
        from gui_app import ModernGUI
        app = ModernGUI()
        app.run()
        
    except ImportError as e:
        missing_packages = """
╔══════════════════════════════════════════════════════════════╗
║                    MISSING PACKAGES                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ❌ Required GUI packages not found                          ║
║                                                              ║
║  Please install:                                             ║
║  • customtkinter                                             ║
║  • matplotlib                                                ║
║  • pandas                                                    ║
║  • numpy                                                     ║
║  • pillow                                                    ║
║                                                              ║
║  Run: pip install -r requirements.txt                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print_colored(missing_packages, Fore.RED if COLORAMA_AVAILABLE else None)
        print_colored(f"Error details: {str(e)}", Fore.RED if COLORAMA_AVAILABLE else None)
        
    except Exception as e:
        print_colored(f"❌ Error launching GUI: {str(e)}", Fore.RED if COLORAMA_AVAILABLE else None)

def main():
    """Main launcher function."""
    while True:
        # Clear screen (works on both Windows and Unix-like systems)
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Show banner and menu
        create_banner()
        show_system_info()
        create_menu()
        
        # Get user choice
        if COLORAMA_AVAILABLE:
            print(f"{Style.BRIGHT}{Fore.WHITE}Enter your choice (1-6): {Style.RESET_ALL}", end="")
        else:
            print("Enter your choice (1-6): ", end="")
        
        try:
            choice = input().strip()
            
            if choice == '1':
                launch_cli()
                input("\nPress Enter to return to launcher...")
                
            elif choice == '2':
                launch_gui()
                input("\nPress Enter to return to launcher...")
                
            elif choice == '3':
                show_quick_stats()
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                run_setup()
                input("\nPress Enter to continue...")
                
            elif choice == '5':
                show_help()
                input("\nPress Enter to continue...")
                
            elif choice == '6':
                print_colored("\n👋 Thank you for using Student Result Management System!", 
                            Fore.CYAN if COLORAMA_AVAILABLE else None, Style.BRIGHT if COLORAMA_AVAILABLE else None)
                print_colored("🎓 Made with ❤️  for educational excellence", Fore.GREEN if COLORAMA_AVAILABLE else None)
                break
                
            else:
                print_colored("\n❌ Invalid choice. Please enter a number between 1 and 6.", Fore.RED if COLORAMA_AVAILABLE else None)
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye!", Fore.CYAN if COLORAMA_AVAILABLE else None, Style.BRIGHT if COLORAMA_AVAILABLE else None)
            break
        except Exception as e:
            print_colored(f"\n❌ An error occurred: {str(e)}", Fore.RED if COLORAMA_AVAILABLE else None)
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
