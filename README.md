# 💬 ChatBox - Real-time Chat Application

<div align="center">

![ChatBox Logo](https://img.shields.io/badge/ChatBox-v1.0-blue?style=for-the-badge&logo=chat)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A modern, real-time chat application built with Python, featuring Material Design 3 UI and comprehensive file sharing capabilities.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 🌟 Features

### 💬 **Real-time Messaging**
- **Public Chat**: Broadcast messages to all online users
- **Private Chat**: Send direct messages to specific users
- **Real-time Updates**: Instant message delivery using TCP sockets
- **Message History**: Persistent chat history with SQLite database

### 👥 **User Management**
- **Authentication System**: Secure login/registration with SHA256 password hashing
- **Online Status**: Real-time user presence indicators
- **User Search**: Quick search functionality for finding users
- **Session Management**: Automatic session handling and cleanup

### 📁 **File Transfer System**
- **Multi-format Support**: Text files, images, documents, and binary files
- **Smart Detection**: Automatic text/binary file type detection
- **File Browser**: Modern interface for browsing and downloading files
- **Size Limits**: Configurable file size restrictions (default: 5MB)
- **Security**: File validation and user-based access control

### 🎨 **Modern UI/UX**
- **Material Design 3**: Contemporary design language with glassmorphism effects
- **Responsive Layout**: Adaptive interface that works on different screen sizes
- **Dark/Light Themes**: Modern color schemes with smooth animations
- **Intuitive Navigation**: User-friendly interface with clear visual hierarchy

### 🔧 **Technical Features**
- **Multi-threading**: Concurrent client handling with thread-safe operations
- **Error Handling**: Comprehensive error management and recovery
- **Logging System**: Detailed logging for debugging and monitoring
- **Modular Architecture**: Clean, maintainable code structure

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+** installed on your system
- **Git** for cloning the repository

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chatbox.git
   cd chatbox
   ```

2. **Install dependencies** (if any)
   ```bash
   # No external dependencies required - uses Python built-ins only!
   # tkinter, socket, sqlite3, threading are all built-in modules
   ```

3. **Initialize the database**
   ```bash
   python Database/database.py
   ```

4. **Start the server**
   ```bash
   python server/start_server.py
   ```

5. **Launch the client** (in a new terminal)
   ```bash
   python client/chatbox.py
   ```

### Alternative Server Management
For advanced server management with monitoring and admin features:
```bash
python server/server_manager.py
```

---

## 📖 Usage

### 🖥️ **Server Setup**

1. **Basic Server Start**
   ```bash
   python server/start_server.py
   ```
   - Default: `localhost:5000`
   - Supports up to 50+ concurrent users

2. **Advanced Server Management**
   ```bash
   python server/server_manager.py
   ```
   - Real-time monitoring
   - User management (kick users)
   - Server broadcasting
   - Statistics dashboard

### 💻 **Client Usage**

1. **Launch Application**
   ```bash
   python client/chatbox.py
   ```

2. **Create Account**
   - Click "Create Account"
   - Enter username, password, and confirm password
   - Username must be unique and 3+ characters

3. **Login**
   - Enter your credentials
   - Click "Sign In"
   - You'll be connected to the chat room

4. **Chat Features**
   - **Public Messages**: Select "Public" and type your message
   - **Private Messages**: Select "Private", choose a user, then send
   - **File Sharing**: Click the 📎 button to upload or download files

### 📁 **File Transfer**

#### Upload Files
1. Click the **📎** button next to the send button
2. Select **"📤 Upload File"**
3. Choose your file (up to 5MB)
4. File will be shared with all users (public) or selected user (private)

#### Download Files
1. Click the **📎** button
2. Select **"📥 Browse & Download Files"**
3. Browse available files with uploader information
4. Select a file and click **"Download Selected"**
5. Choose where to save the file

#### Supported File Types
- **Text Files**: `.txt`, `.md`, `.py`, `.js`, `.html`, `.css`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`
- **Documents**: `.pdf`, `.doc`, `.docx`
- **All Files**: Any file type under 5MB

---

## 🏗️ Architecture

### 📊 **System Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT-SERVER ARCHITECTURE                │
└─────────────────────────────────────────────────────────────┘

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Client    │    │   Client    │    │   Client    │
    │     #1      │    │     #2      │    │     #N      │
    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │ TCP/IP Socket
                              ▼
                    ┌─────────────────────┐
                    │       SERVER        │
                    │  ┌───────────────┐  │
                    │  │ Multi-thread  │  │
                    │  │   Handler     │  │
                    │  └───────────────┘  │
                    │  ┌───────────────┐  │
                    │  │   SQLite DB   │  │
                    │  └───────────────┘  │
                    └─────────────────────┘
```

### 🔧 **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.8+ | Server logic and networking |
| **GUI** | Tkinter | Cross-platform desktop interface |
| **Database** | SQLite | User data and message storage |
| **Networking** | TCP Sockets | Real-time communication |
| **Threading** | Python threading | Concurrent client handling |
| **Security** | SHA256 | Password hashing |
| **Design** | Material Design 3 | Modern UI components |

### 📁 **Project Structure**

```
ChatBox/
├── 📁 client/                    # Client-side application
│   ├── chatbox.py               # Main client application
│   ├── modern_styles.py         # UI styling and themes
│   └── 📁 ui/                   # User interface components
│       ├── modern_login_page.py # Login interface
│       ├── modern_register_page.py # Registration interface
│       └── modern_chat_page.py  # Main chat interface
│
├── 📁 server/                    # Server-side application
│   ├── server.py                # Main server logic
│   ├── client_handler.py        # Individual client management
│   ├── server_manager.py        # Advanced server management
│   └── start_server.py          # Simple server launcher
│
├── 📁 Database/                  # Database management
│   ├── database.py              # SQLite database operations
│   └── chatbox.db               # SQLite database file
│
├── 📁 docs/                      # Documentation
│   ├── SRS_ChatBox.md           # Software Requirements Specification
│   ├── KienTrucHeThong.md       # System Architecture (Vietnamese)
│   └── ThietKeDatabase.md       # Database Design (Vietnamese)
│
├── 📁 files/                     # File storage directory
│   └── (uploaded files stored here)
│
├── README.md                     # This file
└── PRESENTATION_SPEECH.md        # Presentation script
```

---

## 🔌 **Message Protocol**

ChatBox uses a simple pipe-delimited protocol for client-server communication:

```
FORMAT: TYPE|SENDER|RECEIVER|CONTENT|TIMESTAMP

Examples:
- LOGIN|user1|SERVER|password123|2024-01-20 10:00:00
- PUBLIC|user1|ALL|Hello everyone!|2024-01-20 10:01:00
- PRIVATE|user1|user2|Hi there!|2024-01-20 10:02:00
- FILE_SHARE|user1|ALL|filename:type:content|2024-01-20 10:03:00
```

### Message Types
- `LOGIN` / `REGISTER` - Authentication
- `PUBLIC` / `PRIVATE` - Chat messages
- `FILE_SHARE` - File uploads
- `FILE_DOWNLOAD` / `FILE_LIST` - File operations
- `USERLIST` - Online users updates
- `JOIN` / `LEAVE` - User presence notifications

---

## 🗄️ **Database Schema**

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,        -- SHA256 hashed
    display_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER,                   -- NULL for public messages
    content TEXT NOT NULL,
    msg_type VARCHAR(20) DEFAULT 'PUBLIC',
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);
```

---

## 🔧 **Configuration**

### Server Configuration
- **Default Host**: `localhost`
- **Default Port**: `5000`
- **Max Clients**: `50+` (configurable)
- **Buffer Size**: `1MB` for file transfers

### File Transfer Settings
- **Max File Size**: `5MB` (configurable in code)
- **Storage Location**: `./files/` directory
- **Naming Convention**: `{username}_{filename}`
- **Supported Encodings**: UTF-8 for text, Base64 for binary

### Security Settings
- **Password Hashing**: SHA256
- **Session Management**: Automatic cleanup on disconnect
- **File Validation**: Size and type checking

---

## 🧪 **Testing**

### Manual Testing
1. **Start server**: `python server/start_server.py`
2. **Open multiple clients**: Run `python client/chatbox.py` in different terminals
3. **Test scenarios**:
   - User registration and login
   - Public and private messaging
   - File upload and download
   - User presence updates
   - Connection handling

### Test Accounts
The database includes sample accounts for testing:
- `admin` / `admin123`
- `user1` / `123456`
- `user2` / `123456`
- `demo` / `demo`

---

## 🚨 **Troubleshooting**

### Common Issues

#### Server Won't Start
```bash
# Check if port is already in use
netstat -an | grep :5000

# Try different port
python server/start_server.py
# Then enter different port when prompted
```

#### Client Can't Connect
- Ensure server is running
- Check firewall settings
- Verify IP address and port
- Try `localhost` or `127.0.0.1`

#### File Upload Fails
- Check file size (must be < 5MB)
- Ensure `files/` directory exists
- Verify file permissions
- Check server console for error messages

#### Database Issues
```bash
# Reinitialize database
python Database/database.py
```

---

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### Areas for Contribution
- 🎨 UI/UX improvements
- 🔒 Enhanced security features
- 📱 Mobile client development
- 🌐 Web-based interface
- 🔧 Performance optimizations
- 📚 Documentation improvements

---

## 📚 **Documentation**

### Available Documents
- **[SRS_ChatBox.md](docs/SRS_ChatBox.md)**: Complete software requirements specification
- **[KienTrucHeThong.md](docs/KienTrucHeThong.md)**: Detailed system architecture (Vietnamese)
- **[ThietKeDatabase.md](docs/ThietKeDatabase.md)**: Database design documentation (Vietnamese)
- **[PRESENTATION_SPEECH.md](PRESENTATION_SPEECH.md)**: Presentation script for demos

### API Reference
For detailed API documentation, see the docstrings in:
- `server/client_handler.py` - Server-side message handling
- `client/ui/modern_chat_page.py` - Client-side UI interactions
- `Database/database.py` - Database operations

---

## 🔮 **Future Roadmap**

### Short-term (1-2 months)
- [ ] Enhanced file preview capabilities
- [ ] Message search functionality
- [ ] User profile management
- [ ] Emoji and sticker support
- [ ] Message encryption

### Long-term (3-6 months)
- [ ] Web-based client (HTML/CSS/JavaScript)
- [ ] Mobile applications (React Native/Flutter)
- [ ] Voice and video calling
- [ ] Group chat rooms
- [ ] Cloud deployment (AWS/Azure)
- [ ] Load balancing for scalability

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 ChatBox Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 **Team**

### Development Team
- **Project Lead**: [Your Name]
- **Backend Developer**: [Team Member]
- **Frontend Developer**: [Team Member]
- **Database Designer**: [Team Member]

### Acknowledgments
- Material Design 3 for UI inspiration
- Python community for excellent documentation
- SQLite team for the reliable database engine

---

## 📞 **Support**

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/yourusername/chatbox/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/chatbox/discussions)
- **Email**: support@chatbox.com

### Reporting Bugs
When reporting bugs, please include:
- Operating system and Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Console output/error messages
- Screenshots (if applicable)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ by the ChatBox Team

[⬆ Back to Top](#-chatbox---real-time-chat-application)

</div>