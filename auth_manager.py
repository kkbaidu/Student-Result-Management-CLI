import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import getpass
from datetime import datetime


class AuthManager:
    def __init__(self, db_config):
        """Initialize the Authentication Manager with database configuration."""
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        self.current_user = None
    
    def connect_to_database(self):
        """Establish connection to PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            return True
        except psycopg2.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def create_users_table(self):
        """Create the users table if it doesn't exist."""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(64) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            return True
        except psycopg2.Error as e:
            print(f"✗ Error creating users table: {e}")
            return False
    
    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email):
        """Basic email validation."""
        return "@" in email and "." in email.split("@")[1]
    
    def validate_password(self, password):
        """Validate password strength."""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        return True, "Password is valid"
    
    def signup(self):
        """Handle user registration."""
        print("\n" + "="*50)
        print("USER REGISTRATION")
        print("="*50)
        
        try:
            # Get user input
            full_name = input("Enter your full name: ").strip()
            if not full_name:
                print("✗ Full name cannot be empty.")
                return False
            
            username = input("Enter username: ").strip()
            if not username:
                print("✗ Username cannot be empty.")
                return False
            
            email = input("Enter email address: ").strip()
            if not self.validate_email(email):
                print("✗ Please enter a valid email address.")
                return False
            
            password = getpass.getpass("Enter password: ")
            is_valid, message = self.validate_password(password)
            if not is_valid:
                print(f"✗ {message}")
                return False
            
            confirm_password = getpass.getpass("Confirm password: ")
            if password != confirm_password:
                print("✗ Passwords do not match.")
                return False
            
            # Check if username or email already exists
            check_query = "SELECT id FROM users WHERE username = %s OR email = %s"
            self.cursor.execute(check_query, (username, email))
            existing_user = self.cursor.fetchone()
            
            if existing_user:
                print("✗ Username or email already exists. Please choose different credentials.")
                return False
            
            # Hash password and insert user
            password_hash = self.hash_password(password)
            insert_query = """
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (%s, %s, %s, %s)
            """
            
            self.cursor.execute(insert_query, (username, email, password_hash, full_name))
            self.connection.commit()
            
            print(f"✓ Account created successfully for {username}!")
            print("You can now login with your credentials.")
            return True
            
        except psycopg2.Error as e:
            print(f"✗ Database error during registration: {e}")
            self.connection.rollback()
            return False
        except KeyboardInterrupt:
            print("\n✗ Registration cancelled.")
            return False
        except Exception as e:
            print(f"✗ An error occurred during registration: {e}")
            return False
    
    def login(self):
        """Handle user login."""
        print("\n" + "="*50)
        print("USER LOGIN")
        print("="*50)
        
        try:
            username = input("Enter username: ").strip()
            if not username:
                print("✗ Username cannot be empty.")
                return False
            
            password = getpass.getpass("Enter password: ")
            if not password:
                print("✗ Password cannot be empty.")
                return False
            
            # Hash the entered password
            password_hash = self.hash_password(password)
            
            # Check credentials
            login_query = """
            SELECT id, username, email, full_name, role, created_at
            FROM users 
            WHERE username = %s AND password_hash = %s
            """
            
            self.cursor.execute(login_query, (username, password_hash))
            user = self.cursor.fetchone()
            
            if not user:
                print("✗ Invalid username or password.")
                return False
            
            # Update last login time
            update_login_query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s"
            self.cursor.execute(update_login_query, (user['id'],))
            self.connection.commit()
            
            # Set current user
            self.current_user = dict(user)
            
            print(f"✓ Welcome back, {user['full_name']}!")
            print(f"Role: {user['role'].title()}")
            print(f"Account created: {user['created_at'].strftime('%Y-%m-%d')}")
            return True
            
        except psycopg2.Error as e:
            print(f"✗ Database error during login: {e}")
            return False
        except KeyboardInterrupt:
            print("\n✗ Login cancelled.")
            return False
        except Exception as e:
            print(f"✗ An error occurred during login: {e}")
            return False
    
    def logout(self):
        """Handle user logout."""
        if self.current_user:
            print(f"✓ Goodbye, {self.current_user['full_name']}!")
            self.current_user = None
        else:
            print("No user is currently logged in.")
    
    def is_logged_in(self):
        """Check if a user is currently logged in."""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get the currently logged in user."""
        return self.current_user
    
    def display_user_info(self):
        """Display current user information."""
        if not self.current_user:
            print("No user is currently logged in.")
            return
        
        user = self.current_user
        print("\n" + "="*50)
        print("CURRENT USER INFORMATION")
        print("="*50)
        print(f"Username: {user['username']}")
        print(f"Full Name: {user['full_name']}")
        print(f"Email: {user['email']}")
        print(f"Role: {user['role'].title()}")
        print(f"Account Created: {user['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
    
    def close_connection(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
