# 🎓 Student Result Management System

A modern, feature-rich student result management application with both CLI and GUI interfaces. This system demonstrates advanced Python programming concepts while maintaining clean, maintainable code without heavy frameworks.

## ✨ Features

### 🖥️ Beautiful GUI Interface

- **Modern Dark Theme**: Sleek CustomTkinter-based interface
- **Interactive Dashboard**: Real-time statistics and visualizations
- **Advanced Charts**: Matplotlib integration for data visualization
- **User Authentication**: Secure login and registration system
- **File Import**: Easy drag-and-drop data import functionality

### 💻 Powerful CLI Interface

- **Command-line Interface**: Perfect for automation and server environments
- **Full Feature Parity**: All GUI features available in CLI
- **Efficient Operations**: Optimized for performance and speed
- **Batch Processing**: Handle large datasets efficiently

### 🔐 Security & Authentication

- **User Management**: Multi-user support with role-based access
- **Secure Authentication**: SHA-256 password hashing
- **Session Management**: Secure session handling
- **Data Protection**: Input validation and SQL injection prevention

### 📊 Advanced Analytics

- **Grade Distribution**: Visual representation of student performance
- **Performance Metrics**: Average scores, top performers, trends
- **Statistical Analysis**: Comprehensive data insights
- **Export Capabilities**: Multiple output formats

### 💾 Data Management

- **Multi-format Support**: CSV, TXT, Excel file imports
- **Database Integration**: PostgreSQL for robust data storage
- **Data Validation**: Comprehensive input validation
- **Backup & Export**: Multiple export options

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- PostgreSQL database
- Git (for cloning)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kkbaidu/Student-Result-Management-CLI.git
   cd Student-Result-Management-CLI
   ```

2. **Set up virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database:**

   - Update `config.env` with your PostgreSQL credentials
   - Ensure PostgreSQL is running and accessible

5. **Run the application:**
   ```bash
   python launcher.py
   ```

## 🎯 Usage

### Using the Launcher

The launcher provides an intuitive menu to choose between interfaces:

```bash
python launcher.py
```

Choose from:

1. 🖥️ GUI Application (Recommended for desktop use)
2. 💻 CLI Application (Perfect for servers/automation)
3. ❓ Help & Information
4. 🚪 Exit

### GUI Interface Features

#### 🏠 Dashboard

- Real-time student statistics
- Interactive grade distribution charts
- Performance overview cards
- Quick navigation sidebar

#### 👥 Student Management

- View all student records
- Search and filter capabilities
- Individual student profiles
- Grade updates and modifications

#### 📁 Data Import

- Browse and select data files
- Support for multiple formats
- Validation and error reporting
- Bulk import capabilities

#### 📊 Analytics

- Advanced performance metrics
- Trend analysis and predictions
- Comparative studies
- Export analysis reports

### CLI Interface Features

#### Core Operations

```bash
# View all students
python main.py

# Import data from file
python main.py --import ug_student_data.txt

# Generate reports
python main.py --report summary_report.txt
```

## 📁 Project Structure

```
├── gui_app.py              # Main GUI application
├── main.py                 # CLI application entry point
├── launcher.py             # Application launcher
├── student_result_manager.py # Core student management logic
├── auth_manager.py         # Authentication and user management
├── load_config.py          # Configuration management
├── config.env              # Database configuration
├── requirements.txt        # Python dependencies
├── ug_student_data.txt     # Sample student data
└── README.md              # This file
```

## 🛠️ Technical Highlights

### Advanced Python Concepts Demonstrated

1. **Object-Oriented Programming**

   - Clean class hierarchies
   - Proper encapsulation and abstraction
   - Inheritance and polymorphism

2. **Database Integration**

   - PostgreSQL with psycopg2
   - Prepared statements and security
   - Transaction management

3. **GUI Programming**

   - Modern CustomTkinter interface
   - Event-driven programming
   - Threading for responsive UI

4. **Data Visualization**

   - Matplotlib integration
   - Interactive charts and graphs
   - Real-time data updates

5. **Security Implementation**

   - Password hashing and validation
   - SQL injection prevention
   - Input sanitization

6. **Error Handling**
   - Comprehensive exception handling
   - Graceful failure recovery
   - User-friendly error messages

## 🎨 GUI Screenshots

### Login Screen

![Login Screen](screenshots/login.png)
_Modern authentication with welcome graphics_

### Dashboard

![Dashboard](screenshots/dashboard.png)
_Real-time analytics and statistics_

### Student Management

![Students](screenshots/students.png)
_Comprehensive student record management_

## 📊 Sample Data Format

The system accepts student data in the following format:

```csv
20250001, Kwesi Mensah, Information Technology, 78
20250002, Adwoa Serwaa, Actuarial Science, 85
20250003, Kofi Opoku, Geological Engineering, 70
```

Format: `Index Number, Full Name, Course, Score`

## 🔧 Configuration

### Database Configuration (`config.env`)

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_results_db
DB_USER=your_username
DB_PASSWORD=your_password
```

### Grading Scale

- A: 80-100
- B: 70-79
- C: 60-69
- D: 50-59
- F: 0-49

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter** for the modern GUI framework
- **Matplotlib** for beautiful data visualizations
- **PostgreSQL** for robust database capabilities
- **Python Community** for excellent libraries and documentation

## 📞 Support

For support, questions, or suggestions:

- Open an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [Wiki Page]

---

**Made with ❤️ for educational excellence and innovative learning**
