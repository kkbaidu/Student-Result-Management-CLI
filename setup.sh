#!/bin/bash

# Student Result Management CLI - Setup Script
# This script sets up the complete environment for the application

echo "Student Result Management CLI - Setup Script"
echo "============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if PostgreSQL service is running
check_postgres_service() {
    sudo systemctl is-active --quiet postgresql
}

# 1. Check Python installation
echo "1. Checking Python installation..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION found"
else
    echo "✗ Python3 not found. Please install Python3 first."
    exit 1
fi

# 2. Install required Python packages
echo ""
echo "2. Installing Python dependencies..."
if command_exists pip3; then
    pip3 install psycopg2-binary
    echo "✓ psycopg2-binary installed"
else
    echo "✗ pip3 not found. Please install pip3 first."
    exit 1
fi

# 3. Check PostgreSQL installation
echo ""
echo "3. Checking PostgreSQL installation..."
if command_exists psql; then
    echo "✓ PostgreSQL client found"
else
    echo "Installing PostgreSQL..."
    sudo apt update
    sudo apt install postgresql postgresql-contrib -y
    echo "✓ PostgreSQL installed"
fi

# 4. Start PostgreSQL service
echo ""
echo "4. Starting PostgreSQL service..."
if check_postgres_service; then
    echo "✓ PostgreSQL service is already running"
else
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    echo "✓ PostgreSQL service started and enabled"
fi

# 5. Create database and user
echo ""
echo "5. Setting up database and user..."

# Create database
echo "Creating database 'student_results_db'..."
sudo -u postgres createdb student_results_db 2>/dev/null || echo "Database may already exist"

# Create user
echo "Creating user 'student_user'..."
sudo -u postgres psql -c "CREATE USER student_user WITH PASSWORD 'password123';" 2>/dev/null || echo "User may already exist"

# Grant privileges
echo "Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE student_results_db TO student_user;"
sudo -u postgres psql -d student_results_db -c "GRANT CREATE ON SCHEMA public TO student_user;"
sudo -u postgres psql -d student_results_db -c "GRANT USAGE ON SCHEMA public TO student_user;"

echo "✓ Database setup completed"

# 6. Test the setup
echo ""
echo "6. Testing the setup..."
if python3 test_setup.py; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "You can now run the application with:"
    echo "  python3 main.py"
    echo ""
    echo "Sample data file 'sample_data.txt' is ready to be loaded."
    echo "Use option 1 in the menu to load the sample data."
else
    echo ""
    echo "❌ Setup test failed. Please check the errors above."
    exit 1
fi

echo ""
echo "Setup script completed!"
