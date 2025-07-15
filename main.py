#!/usr/bin/env python3
# Run "sudo -u postgres psql -d student_results_db -c "GRANT CREATE ON SCHEMA public TO student_user;"" before running this script
"""
Student Result Management CLI Tool
A command-line application for managing student results with PostgreSQL database integration.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


class StudentResultManager:
    def __init__(self, db_config):
        """Initialize the Student Result Manager with database configuration."""
        self.db_config = db_config
        self.connection = None
        self.cursor = None
    
    def connect_to_database(self):
        """Establish connection to PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("✓ Connected to PostgreSQL database successfully!")
            return True
        except psycopg2.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def create_table(self):
        """Create the student_results table if it doesn't exist."""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS student_results (
                id SERIAL PRIMARY KEY,
                index_number VARCHAR(10) NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                course TEXT NOT NULL,
                score INTEGER NOT NULL,
                grade CHAR(1)
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("✓ Table 'student_results' created/verified successfully!")
            return True
        except psycopg2.Error as e:
            print(f"✗ Error creating table: {e}")
            return False
    
    def calculate_grade(self, score):
        """Calculate grade based on score"""
        if score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    def read_student_data(self, filename):
        """Read student data from file."""
        students = []
        try:
            with open(filename, 'r') as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if line:  # Skip empty lines
                        try:
                            parts = line.split(',')
                            if len(parts) != 4:
                                print(f"⚠ Warning: Line {line_number} has incorrect format. Skipping.")
                                continue
                            
                            index_number = parts[0].strip()
                            full_name = parts[1].strip()
                            course = parts[2].strip()
                            score = int(parts[3].strip())
                            
                            grade = self.calculate_grade(score)
                            
                            students.append({
                                'index_number': index_number,
                                'full_name': full_name,
                                'course': course,
                                'score': score,
                                'grade': grade
                            })
                        except ValueError:
                            print(f"⚠ Warning: Line {line_number} has invalid score. Skipping.")
                            continue
            
            print(f"✓ Successfully read {len(students)} student records from {filename}")
            return students
        except FileNotFoundError:
            print(f"✗ Error: File '{filename}' not found.")
            return []
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return []
    
    def insert_student_data(self, students):
        """Insert student data into database."""
        inserted_count = 0
        updated_count = 0
        
        for student in students:
            try:
                # Check if student already exists
                check_query = "SELECT id FROM student_results WHERE index_number = %s"
                self.cursor.execute(check_query, (student['index_number'],))
                existing = self.cursor.fetchone()
                
                if existing:
                    # Update existing record
                    update_query = """
                    UPDATE student_results 
                    SET full_name = %s, course = %s, score = %s, grade = %s
                    WHERE index_number = %s
                    """
                    self.cursor.execute(update_query, (
                        student['full_name'],
                        student['course'],
                        student['score'],
                        student['grade'],
                        student['index_number']
                    ))
                    updated_count += 1
                else:
                    # Insert new record
                    insert_query = """
                    INSERT INTO student_results (index_number, full_name, course, score, grade)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    self.cursor.execute(insert_query, (
                        student['index_number'],
                        student['full_name'],
                        student['course'],
                        student['score'],
                        student['grade']
                    ))
                    inserted_count += 1
                
            except psycopg2.Error as e:
                print(f"✗ Error processing student {student['index_number']}: {e}")
                continue
        
        try:
            self.connection.commit()
            print(f"✓ Successfully inserted {inserted_count} new records and updated {updated_count} existing records.")
            return True
        except psycopg2.Error as e:
            print(f"✗ Error committing changes: {e}")
            self.connection.rollback()
            return False
    
    def view_all_records(self):
        """View all student records."""
        try:
            query = """
            SELECT index_number, full_name, course, score, grade 
            FROM student_results 
            ORDER BY index_number
            """
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            
            if not records:
                print("No records found in the database.")
                return
            
            print("\n" + "="*80)
            print("ALL STUDENT RECORDS")
            print("="*80)
            print(f"{'Index':<10} {'Name':<20} {'Course':<15} {'Score':<6} {'Grade':<5}")
            print("-" * 80)
            
            for record in records:
                print(f"{record['index_number']:<10} {record['full_name']:<20} {record['course']:<15} {record['score']:<6} {record['grade']:<5}")
            
            print(f"\nTotal Records: {len(records)}")
            print("="*80)
            
        except psycopg2.Error as e:
            print(f"✗ Error retrieving records: {e}")
    
    def view_student_by_index(self, index_number):
        """View a specific student by index number."""
        try:
            query = """
            SELECT index_number, full_name, course, score, grade 
            FROM student_results 
            WHERE index_number = %s
            """
            self.cursor.execute(query, (index_number,))
            record = self.cursor.fetchone()
            
            if not record:
                print(f"No student found with index number: {index_number}")
                return
            
            print("\n" + "="*50)
            print("STUDENT DETAILS")
            print("="*50)
            print(f"Index Number: {record['index_number']}")
            print(f"Full Name: {record['full_name']}")
            print(f"Course: {record['course']}")
            print(f"Score: {record['score']}")
            print(f"Grade: {record['grade']}")
            print("="*50)
            
        except psycopg2.Error as e:
            print(f"✗ Error retrieving student: {e}")
    
    def update_student_score(self, index_number, new_score):
        """Update a student's score and recalculate grade."""
        try:
            # Check if student exists
            check_query = "SELECT id FROM student_results WHERE index_number = %s"
            self.cursor.execute(check_query, (index_number,))
            existing = self.cursor.fetchone()
            
            if not existing:
                print(f"No student found with index number: {index_number}")
                return False
            
            # Calculate new grade
            new_grade = self.calculate_grade(new_score)
            
            # Update the record
            update_query = """
            UPDATE student_results 
            SET score = %s, grade = %s
            WHERE index_number = %s
            """
            self.cursor.execute(update_query, (new_score, new_grade, index_number))
            self.connection.commit()
            
            print(f"✓ Successfully updated score for {index_number} to {new_score} (Grade: {new_grade})")
            return True
            
        except psycopg2.Error as e:
            print(f"✗ Error updating student score: {e}")
            self.connection.rollback()
            return False
    
    def export_summary_report(self, filename):
        """Export summary report to file."""
        try:
            # Get total count
            self.cursor.execute("SELECT COUNT(*) as total FROM student_results")
            total_students = self.cursor.fetchone()['total']
            
            # Get grade distribution
            self.cursor.execute("""
                SELECT grade, COUNT(*) as count 
                FROM student_results 
                GROUP BY grade 
                ORDER BY grade
            """)
            grade_distribution = self.cursor.fetchall()
            
            # Get top performers
            self.cursor.execute("""
                SELECT index_number, full_name, course, score, grade 
                FROM student_results 
                ORDER BY score DESC 
                LIMIT 5
            """)
            top_performers = self.cursor.fetchall()
            
            # Create report content
            report_content = f"""Summary Report
            ==============
            Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            Total Students: {total_students}

            Grade Distribution:
            """
            
            for grade_info in grade_distribution:
                report_content += f"{grade_info['grade']}: {grade_info['count']}\n"
            
            report_content += f"\nTop 5 Performers:\n"
            report_content += "-" * 50 + "\n"
            
            for i, student in enumerate(top_performers, 1):
                report_content += f"{i}. {student['full_name']} ({student['index_number']}) - {student['course']}: {student['score']} ({student['grade']})\n"
            
            # Write to file
            with open(filename, 'w') as file:
                file.write(report_content)
            
            print(f"✓ Summary report exported to {filename}")
            print(f"Total Students: {total_students}")
            print("Grade Distribution:")
            for grade_info in grade_distribution:
                print(f"  {grade_info['grade']}: {grade_info['count']}")
            
            return True
            
        except psycopg2.Error as e:
            print(f"✗ Database error generating report: {e}")
            return False
        except Exception as e:
            print(f"✗ Error writing report file: {e}")
            return False
    
    def close_connection(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✓ Database connection closed.")


def load_config():
    """Load database configuration from environment variables or config file."""
    config = {}
    
    # Try to read from config.env file
    config_file = 'config.env'
    if os.path.exists(config_file):
        print(f"Loading configuration from {config_file}")
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    # Override with environment variables if they exist
    db_config = {
        'host': os.getenv('DB_HOST', config.get('DB_HOST', 'localhost')),
        'database': os.getenv('DB_NAME', config.get('DB_NAME', 'student_results')),
        'user': os.getenv('DB_USER', config.get('DB_USER', 'postgres')),
        'password': os.getenv('DB_PASSWORD', config.get('DB_PASSWORD', 'password')),
        'port': int(os.getenv('DB_PORT', config.get('DB_PORT', '5432')))
    }
    
    return db_config


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
                filename = input("Enter the filename to load (default: sample_data.txt): ").strip()
                if not filename:
                    filename = 'sample_data.txt'
                
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