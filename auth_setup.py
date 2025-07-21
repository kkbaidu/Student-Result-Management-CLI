#!/usr/bin/env python3
"""
Setup script for Student Result Management CLI with Authentication
"""

from load_config import load_config
from auth_manager import AuthManager
from student_result_manager import StudentResultManager


def test_database_connection():
    """Test database connection."""
    print("Testing database connection...")
    
    # Load configuration
    db_config = load_config()
    print(f"Database configuration loaded:")
    print(f"  Host: {db_config['host']}")
    print(f"  Database: {db_config['database']}")
    print(f"  User: {db_config['user']}")
    print(f"  Port: {db_config['port']}")
    
    # Test auth manager connection
    auth_manager = AuthManager(db_config)
    if auth_manager.connect_to_database():
        print("✓ Authentication manager connected successfully!")
        
        # Create users table
        if auth_manager.create_users_table():
            print("✓ Users table created/verified successfully!")
        else:
            print("✗ Failed to create users table.")
            return False
        
        auth_manager.close_connection()
    else:
        print("✗ Failed to connect with authentication manager.")
        return False
    
    return True


if __name__ == "__main__":
    print("Student Result Management CLI - Setup & Test")
    print("=" * 50)
    test_database_connection()
