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
            
            print(f"Student with index number {index_number} found. Find details below:")
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

