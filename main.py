#!/usr/bin/env python3
# Run "sudo -u postgres psql -d student_results_db -c "GRANT CREATE ON SCHEMA public TO student_user;"" before running this script
"""
Student Result Management CLI Tool
A command-line application for managing student results with PostgreSQL database integration.
"""
from student_result_manager import StudentResultManager
from auth_manager import AuthManager
from load_config import load_config



def display_auth_menu():
    """Display the authentication menu."""
    print("\n" + "="*50)
    print("STUDENT RESULT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Login")
    print("2. Sign Up")
    print("3. Exit")
    print("="*50)


def display_main_menu(user_name):
    """Display the main menu."""
    print("\n" + "="*50)
    print(f"WELCOME {user_name.upper()}")
    print("STUDENT RESULT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Load student data from file")
    print("2. View all records")
    print("3. View student by index number")
    print("4. Update student score")
    print("5. Export summary report to file")
    print("6. View user profile")
    print("7. Logout")
    print("8. Exit")
    print("="*50)


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("STUDENT RESULT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Load student data from file")
    print("2. View all records")
    print("3. View student by index number")
    print("4. Update student score")
    print("5. Export summary report to file")
    print("6. Exit")
    print("="*50)


def main():
    """Main application function."""
    print("Student Result Management CLI Tool")
    print("="*40)
    
    # Load configuration
    db_config = load_config()
    
    # Initialize the authentication manager
    auth_manager = AuthManager(db_config)
    
    # Connect to database for authentication
    if not auth_manager.connect_to_database():
        print("Failed to connect to database. Please check your configuration.")
        return
    
    # Create users table
    if not auth_manager.create_users_table():
        print("Failed to create/verify users table. Exiting.")
        return
    
    # Authentication loop
    while True:
        if not auth_manager.is_logged_in():
            display_auth_menu()
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                if auth_manager.login():
                    break  # Successfully logged in, exit auth loop
            elif choice == '2':
                auth_manager.signup()
            elif choice == '3':
                print("Thank you for using Student Result Management System!")
                auth_manager.close_connection()
                return
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
            
            # Wait for user to press Enter before continuing
            input("\nPress Enter to continue...")
        else:
            break
    
    # Initialize the student result manager
    manager = StudentResultManager(db_config)
    
    # Connect to database
    if not manager.connect_to_database():
        print("Failed to connect to database. Please check your configuration.")
        auth_manager.close_connection()
        return
    
    # Create table
    if not manager.create_table():
        print("Failed to create/verify table. Exiting.")
        auth_manager.close_connection()
        return
    
    # Main application loop
    try:
        current_user = auth_manager.get_current_user()
        while auth_manager.is_logged_in():
            display_main_menu(current_user['full_name'])
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                filename = input("Enter the filename to load (default: ug_student_data.txt): ").strip()
                if not filename:
                    filename = 'ug_student_data.txt'
                
                students = manager.read_student_data(filename)
                if students:
                    manager.insert_student_data(students)
            
            elif choice == '2':
                manager.view_all_records()
            
            elif choice == '3':
                index_number = input("Enter student index number: ").strip()
                if index_number:
                    manager.view_student_by_index(index_number)
                else:
                    print("Please enter a valid index number.")
            
            elif choice == '4':
                index_number = input("Enter student index number: ").strip()
                if not index_number:
                    print("Please enter a valid index number.")
                    continue
                
                try:
                    new_score = int(input("Enter new score (0-100): ").strip())
                    if 0 <= new_score <= 100:
                        manager.update_student_score(index_number, new_score)
                    else:
                        print("Score must be between 0 and 100.")
                except ValueError:
                    print("Please enter a valid numeric score.")
            
            elif choice == '5':
                filename = input("Enter report filename (default: summary_report.txt): ").strip()
                if not filename:
                    filename = 'summary_report.txt'
                manager.export_summary_report(filename)
            
            elif choice == '6':
                auth_manager.display_user_info()
            
            elif choice == '7':
                auth_manager.logout()
                break  # Exit main loop to return to auth menu
            
            elif choice == '8':
                print("Thank you for using Student Result Management System!")
                auth_manager.logout()
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
            
            # Wait for user to press Enter before continuing
            input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    finally:
        # Clean up connections
        manager.close_connection()
        auth_manager.close_connection()


if __name__ == "__main__":
    main()