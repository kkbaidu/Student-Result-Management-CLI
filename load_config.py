import os

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