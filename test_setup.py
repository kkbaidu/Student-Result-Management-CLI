#!/usr/bin/env python3
"""
Test script to verify the setup and database connection
"""

import sys
import os

def test_imports():
    """Test if required modules can be imported"""
    print("Testing imports...")
    try:
        import psycopg2
        print("✓ psycopg2 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import psycopg2: {e}")
        return False
    
    try:
        from main import StudentResultManager
        print("✓ StudentResultManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import StudentResultManager: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from main import StudentResultManager
        
        # Database configuration
        db_config = {
            'host': 'localhost',
            'database': 'student_results_db',
            'user': 'student_user',
            'password': 'password123',
            'port': 5432
        }
        
        manager = StudentResultManager(db_config)
        if manager.connect_to_database():
            print("✓ Database connection successful")
            if manager.connection is not None:
                manager.connection.close()
            return True
        else:
            print("✗ Database connection failed")
            return False
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False

def test_sample_data_file():
    """Test if sample data file exists"""
    print("\nTesting sample data file...")
    if os.path.exists("sample_data.txt"):
        print("✓ Sample data file exists")
        with open("sample_data.txt", "r") as f:
            lines = f.readlines()
            print(f"✓ Found {len(lines)} student records")
        return True
    else:
        print("✗ Sample data file not found")
        return False

def main():
    """Run all tests"""
    print("Student Result Management CLI - Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database_connection,
        test_sample_data_file
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n✓ All tests passed! The application is ready to use.")
        print("Run 'python main.py' to start the application.")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
