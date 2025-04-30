# Python-Sentinel
Integration Project: RSI 2

## Description
Python-Sentinel is a web-based system monitoring and remote SSH management tool that provides real-time system metrics visualization and remote server management capabilities. It offers a secure interface for monitoring system resources, managing processes, and executing remote commands via SSH.

## Features
- **Secure SSH Authentication**: Remote server access with username/password authentication
- **Real-time System Monitoring**:
  - CPU usage tracking
  - Memory utilization
  - Disk usage statistics
  - Network traffic monitoring
- **Process Management**:
  - View running processes
  - Monitor process CPU and memory usage
  - Kill processes remotely
- **Interactive Terminal**:
  - Execute commands remotely
  - Real-time command output
  - Persistent SSH session management

## Technologies Used
- Python 3.12.6
- Flask 3.1.0
- Paramiko 3.5.1 (SSH client)
- psutil 5.9.8 (System monitoring)
- Chart.js (Data visualization)
- Docker support

## Installation

### Local Setup
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
   The application will be available at http://localhost:5000

### Docker Setup
1. Build and run using Docker Compose:
   ```
   docker compose up --build
   ```
   The application will be available at http://localhost:8000

## Usage
1. Access the web interface
2. Log in with your SSH credentials:
   - Username
   - Server IP
   - Password
3. Navigate through the available features:
   - Dashboard: View system metrics
   - Processes: Manage running processes
   - Terminal: Execute remote commands

## Security Note
- Ensure secure password handling in production
- Use environment variables for sensitive data
- Consider implementing SSH key authentication

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
UCHIHAA CLAN
