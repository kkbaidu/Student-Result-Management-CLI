#!/usr/bin/env python3
# Run "sudo -u postgres psql -d student_results_db -c "GRANT CREATE ON SCHEMA public TO student_user;"" before running this script
"""
Student Result Management CLI Tool
A command-line application for managing student results with PostgreSQL database integration.
"""
from student_result_manager import StudentResultManager
from load_config import load_config



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
    
    # Initialize the manager
    manager = StudentResultManager(db_config)
    
    # Connect to database
    if not manager.connect_to_database():
        print("Failed to connect to database. Please check your configuration.")
        return
    
    # Create table
    if not manager.create_table():
        print("Failed to create/verify table. Exiting.")
        return
    
    try:
        while True:
            display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
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
                print("Thank you for using Student Result Management System!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
            
            # Wait for user to press Enter before continuing
            input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    
    finally:
        manager.close_connection()


if __name__ == "__main__":
    main()