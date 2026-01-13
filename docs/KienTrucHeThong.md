# THIẾT KẾ KIẾN TRÚC HỆ THỐNG - CHAT BOX APPLICATION

---

## 1. TỔNG QUAN KIẾN TRÚC

### 1.1 Mô hình Client-Server

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INTERNET / LAN                                  │
└─────────────────────────────────────────────────────────────────────────────┘
        ▲               ▲               ▲               ▲
        │ TCP           │ TCP           │ TCP           │ TCP
        │ Socket        │ Socket        │ Socket        │ Socket
        ▼               ▼               ▼               ▼
┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│  Client   │   │  Client   │   │  Client   │   │  Client   │
│    #1     │   │    #2     │   │    #3     │   │    #N     │
│  (User)   │   │  (User)   │   │  (User)   │   │  (User)   │
└───────────┘   └───────────┘   └───────────┘   └───────────┘
        │               │               │               │
        └───────────────┴───────┬───────┴───────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │                       │
                    │       SERVER          │
                    │   (Central Hub)       │
                    │                       │
                    │  ┌─────────────────┐  │
                    │  │  Thread Pool    │  │
                    │  │  (Multi-client) │  │
                    │  └─────────────────┘  │
                    │                       │
                    │  ┌─────────────────┐  │
                    │  │    Database     │  │
                    │  │    (SQLite)     │  │
                    │  └─────────────────┘  │
                    │                       │
                    └───────────────────────┘
```

### 1.2 Luồng dữ liệu tổng quan

```
┌──────────┐  1.Connect   ┌──────────┐  2.Auth    ┌──────────┐
│  Client  │─────────────►│  Server  │───────────►│ Database │
└──────────┘              └──────────┘            └──────────┘
     │                         │                       │
     │  3.Send Message         │  4.Query User         │
     │────────────────────────►│◄──────────────────────│
     │                         │                       │
     │  5.Broadcast/Forward    │                       │
     │◄────────────────────────│                       │
     │                         │                       │
```

---

## 2. KIẾN TRÚC SERVER

### 2.1 Sơ đồ thành phần Server

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            SERVER APPLICATION                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      NETWORK LAYER                                  │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │  ┌──────────────────┐    ┌──────────────────────────────────────┐  │ │
│  │  │  ServerSocket    │    │         ClientHandler                │  │ │
│  │  │  (Port 5000)     │    │  ┌────────┐ ┌────────┐ ┌────────┐   │  │ │
│  │  │                  │───►│  │Thread 1│ │Thread 2│ │Thread N│   │  │ │
│  │  │  - accept()      │    │  └────────┘ └────────┘ └────────┘   │  │ │
│  │  │  - listen()      │    │                                      │  │ │
│  │  └──────────────────┘    └──────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      BUSINESS LOGIC LAYER                          │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │ │
│  │  │ AuthService     │  │ MessageService  │  │ UserService     │    │ │
│  │  │                 │  │                 │  │                 │    │ │
│  │  │ - login()       │  │ - broadcast()   │  │ - getOnline()   │    │ │
│  │  │ - register()    │  │ - sendPrivate() │  │ - addUser()     │    │ │
│  │  │ - validate()    │  │ - parseMsg()    │  │ - removeUser()  │    │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      DATA ACCESS LAYER                             │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────────┐           ┌─────────────────────────────┐    │ │
│  │  │ DatabaseManager │──────────►│      SQLite Database        │    │ │
│  │  │                 │           │  ┌───────┐  ┌───────────┐   │    │ │
│  │  │ - connect()     │           │  │ users │  │ messages  │   │    │ │
│  │  │ - query()       │           │  └───────┘  └───────────┘   │    │ │
│  │  │ - insert()      │           │                             │    │ │
│  │  └─────────────────┘           └─────────────────────────────┘    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Class Diagram - Server

```
┌─────────────────────────────────────┐
│            ChatServer               │
├─────────────────────────────────────┤
│ - serverSocket: ServerSocket        │
│ - port: int                         │
│ - clients: List<ClientHandler>      │
│ - isRunning: boolean                │
├─────────────────────────────────────┤
│ + start(): void                     │
│ + stop(): void                      │
│ + broadcast(msg: String): void      │
│ + getOnlineUsers(): List<String>    │
└─────────────────────────────────────┘
                 │
                 │ creates
                 ▼
┌─────────────────────────────────────┐
│          ClientHandler              │
│         <<Thread>>                  │
├─────────────────────────────────────┤
│ - socket: Socket                    │
│ - in: BufferedReader                │
│ - out: PrintWriter                  │
│ - username: String                  │
│ - server: ChatServer                │
├─────────────────────────────────────┤
│ + run(): void                       │
│ + sendMessage(msg: String): void    │
│ + handleMessage(msg: String): void  │
│ + disconnect(): void                │
└─────────────────────────────────────┘
                 │
                 │ uses
                 ▼
┌─────────────────────────────────────┐
│         DatabaseManager             │
├─────────────────────────────────────┤
│ - connection: Connection            │
│ - dbPath: String                    │
├─────────────────────────────────────┤
│ + connect(): void                   │
│ + createUser(u, p): boolean         │
│ + validateUser(u, p): boolean       │
│ + close(): void                     │
└─────────────────────────────────────┘
```

---

## 3. KIẾN TRÚC CLIENT

### 3.1 Sơ đồ thành phần Client

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT APPLICATION                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      PRESENTATION LAYER (GUI)                       │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │                                                                     │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │ │
│  │  │   LoginForm     │  │   ChatWindow    │  │  UserListPanel  │    │ │
│  │  │                 │  │                 │  │                 │    │ │
│  │  │ - txtUsername   │  │ - txtMessage    │  │ - listUsers     │    │ │
│  │  │ - txtPassword   │  │ - chatArea      │  │ - btnRefresh    │    │ │
│  │  │ - btnLogin      │  │ - btnSend       │  │                 │    │ │
│  │  │ - btnRegister   │  │ - btnPrivate    │  │                 │    │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘    │ │
│  │                                                                     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      CONTROLLER LAYER                               │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │ │
│  │  │ LoginController │  │ ChatController  │  │ MessageHandler  │    │ │
│  │  │                 │  │                 │  │                 │    │ │
│  │  │ - onLogin()     │  │ - onSend()      │  │ - parse()       │    │ │
│  │  │ - onRegister()  │  │ - onReceive()   │  │ - format()      │    │ │
│  │  │ - validate()    │  │ - updateUI()    │  │ - display()     │    │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      NETWORK LAYER                                  │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │                    SocketClient                              │   │ │
│  │  │                                                              │   │ │
│  │  │  - socket: Socket                                            │   │ │
│  │  │  - serverIP: String                                          │   │ │
│  │  │  - serverPort: int                                           │   │ │
│  │  │  - inputStream: BufferedReader                               │   │ │
│  │  │  - outputStream: PrintWriter                                 │   │ │
│  │  │                                                              │   │ │
│  │  │  + connect(): boolean                                        │   │ │
│  │  │  + send(message: String): void                               │   │ │
│  │  │  + receive(): String                                         │   │ │
│  │  │  + disconnect(): void                                        │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Class Diagram - Client

```
┌─────────────────────────────────────┐
│           ChatClient                │
├─────────────────────────────────────┤
│ - socket: Socket                    │
│ - serverIP: String                  │
│ - serverPort: int                   │
│ - in: BufferedReader                │
│ - out: PrintWriter                  │
│ - username: String                  │
│ - isConnected: boolean              │
├─────────────────────────────────────┤
│ + connect(): boolean                │
│ + disconnect(): void                │
│ + sendMessage(msg: String): void    │
│ + login(user, pass): boolean        │
│ + register(user, pass): boolean     │
└─────────────────────────────────────┘
          │
          │ uses
          ▼
┌─────────────────────────────────────┐
│        MessageListener              │
│          <<Thread>>                 │
├─────────────────────────────────────┤
│ - client: ChatClient                │
│ - callback: MessageCallback         │
├─────────────────────────────────────┤
│ + run(): void                       │
│ + onMessageReceived(msg): void      │
└─────────────────────────────────────┘
          │
          │ updates
          ▼
┌─────────────────────────────────────┐
│          ChatGUI                    │
├─────────────────────────────────────┤
│ - client: ChatClient                │
│ - chatArea: TextArea                │
│ - messageInput: TextField           │
│ - userList: ListView                │
├─────────────────────────────────────┤
│ + displayMessage(msg): void         │
│ + updateUserList(users): void       │
│ + showNotification(text): void      │
└─────────────────────────────────────┘
```

---

## 4. GIAO THỨC TRUYỀN THÔNG

### 4.1 Định dạng Message Protocol

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MESSAGE FORMAT                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   [TYPE]|[SENDER]|[RECEIVER]|[CONTENT]|[TIMESTAMP]                      │
│                                                                          │
│   Ví dụ:                                                                 │
│   - LOGIN|user1|SERVER|password123|2024-01-15 10:00:00                  │
│   - REGISTER|user1|SERVER|password123|2024-01-15 10:00:00               │
│   - PUBLIC|user1|ALL|Hello everyone!|2024-01-15 10:01:00                │
│   - PRIVATE|user1|user2|Hi there!|2024-01-15 10:02:00                   │
│   - USERLIST|SERVER|user1|user2,user3,user4|2024-01-15 10:00:00         │
│   - JOIN|user1|ALL|has joined|2024-01-15 10:00:00                       │
│   - LEAVE|user1|ALL|has left|2024-01-15 10:05:00                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Message Types

| Type | Mô tả | Sender | Receiver |
|------|-------|--------|----------|
| LOGIN | Đăng nhập | Client | SERVER |
| REGISTER | Đăng ký | Client | SERVER |
| LOGIN_OK | Đăng nhập thành công | SERVER | Client |
| LOGIN_FAIL | Đăng nhập thất bại | SERVER | Client |
| PUBLIC | Tin nhắn công khai | Client | ALL |
| PRIVATE | Tin nhắn riêng tư | Client | Username |
| USERLIST | Danh sách online | SERVER | Client |
| JOIN | Thông báo vào phòng | SERVER | ALL |
| LEAVE | Thông báo rời phòng | SERVER | ALL |
| ERROR | Thông báo lỗi | SERVER | Client |

### 4.3 Sequence Diagram - Đăng nhập

```
┌────────┐                    ┌────────┐                    ┌──────────┐
│ Client │                    │ Server │                    │ Database │
└───┬────┘                    └───┬────┘                    └────┬─────┘
    │                             │                              │
    │  1. Connect (TCP)           │                              │
    │────────────────────────────►│                              │
    │                             │                              │
    │  2. LOGIN|user|SERVER|pass  │                              │
    │────────────────────────────►│                              │
    │                             │                              │
    │                             │  3. Query: SELECT * FROM     │
    │                             │     users WHERE username=?   │
    │                             │─────────────────────────────►│
    │                             │                              │
    │                             │  4. Return user data         │
    │                             │◄─────────────────────────────│
    │                             │                              │
    │  5. LOGIN_OK|SERVER|user    │                              │
    │◄────────────────────────────│                              │
    │                             │                              │
    │  6. USERLIST|SERVER|user    │                              │
    │◄────────────────────────────│                              │
    │                             │                              │
    │                             │  7. Broadcast JOIN to all    │
    │                             │─────────────────────────────►│
    │                             │                              │
```

### 4.4 Sequence Diagram - Gửi tin nhắn

```
┌──────────┐              ┌────────┐              ┌──────────┐
│ Client A │              │ Server │              │ Client B │
└────┬─────┘              └───┬────┘              └────┬─────┘
     │                        │                        │
     │ PUBLIC|A|ALL|Hello!    │                        │
     │───────────────────────►│                        │
     │                        │                        │
     │                        │  Broadcast to all      │
     │                        │───────────────────────►│
     │                        │                        │
     │ PUBLIC|A|ALL|Hello!    │  PUBLIC|A|ALL|Hello!   │
     │◄───────────────────────│                        │
     │                        │                        │
     │                        │                        │
     │ PRIVATE|A|B|Hi B!      │                        │
     │───────────────────────►│                        │
     │                        │                        │
     │                        │  Forward to B only     │
     │                        │───────────────────────►│
     │                        │                        │
     │                        │  PRIVATE|A|B|Hi B!     │
     │                        │                        │
```

---

## 5. DATABASE DESIGN

### 5.1 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│    ┌─────────────────┐              ┌─────────────────┐         │
│    │     USERS       │              │    MESSAGES     │         │
│    ├─────────────────┤              ├─────────────────┤         │
│    │ PK id           │              │ PK id           │         │
│    │    username     │◄────────────►│ FK sender_id    │         │
│    │    password     │              │ FK receiver_id  │         │
│    │    email        │              │    content      │         │
│    │    created_at   │              │    msg_type     │         │
│    │    last_login   │              │    sent_at      │         │
│    └─────────────────┘              └─────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 SQL Schema

```sql
-- Bảng Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

-- Bảng Messages (Optional - lưu lịch sử chat)
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER,
    content TEXT NOT NULL,
    msg_type VARCHAR(20) DEFAULT 'PUBLIC',
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);

-- Index để tăng tốc query
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_receiver ON messages(receiver_id);
CREATE INDEX idx_users_username ON users(username);
```

---

## 6. DEPLOYMENT DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DEPLOYMENT DIAGRAM                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVER MACHINE                                  │
│                         (IP: 192.168.1.100)                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        <<device>>                                      │  │
│  │                     Windows/Linux PC                                   │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                    <<executionEnvironment>>                      │  │  │
│  │  │                        JVM / Python                              │  │  │
│  │  │  ┌─────────────────┐    ┌─────────────────┐                     │  │  │
│  │  │  │  ChatServer.jar │    │  chatbox.db     │                     │  │  │
│  │  │  │  (Port 5000)    │    │  (SQLite)       │                     │  │  │
│  │  │  └─────────────────┘    └─────────────────┘                     │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ TCP/IP (Port 5000)
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│   CLIENT PC #1    │    │   CLIENT PC #2    │    │   CLIENT PC #N    │
│ (192.168.1.101)   │    │ (192.168.1.102)   │    │ (192.168.1.xxx)   │
│  ┌─────────────┐  │    │  ┌─────────────┐  │    │  ┌─────────────┐  │
│  │ ChatClient  │  │    │  │ ChatClient  │  │    │  │ ChatClient  │  │
│  │    .jar     │  │    │  │    .jar     │  │    │  │    .jar     │  │
│  └─────────────┘  │    │  └─────────────┘  │    │  └─────────────┘  │
└───────────────────┘    └───────────────────┘    └───────────────────┘
```

---

## 7. FLOWCHART

### 7.1 Flowchart - Server Main Loop

```
                    ┌─────────────┐
                    │    START    │
                    └──────┬──────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Initialize Server  │
                │  (Create Socket)    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Listen on Port     │
                │      5000           │
                └──────────┬──────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Wait for Connection   │◄─────────────────┐
              └───────────┬────────────┘                  │
                          │                               │
                          ▼                               │
                   ┌─────────────┐                        │
                   │   Client    │                        │
                   │  Connected? │                        │
                   └──────┬──────┘                        │
                          │                               │
              ┌───────────┴───────────┐                   │
              │ YES                   │ NO                │
              ▼                       └───────────────────┘
    ┌─────────────────────┐
    │  Create New Thread  │
    │  (ClientHandler)    │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  Add to Client List │
    └──────────┬──────────┘
               │
               └──────────────────────────────────────────┘
```

### 7.2 Flowchart - Client Handler

```
                    ┌─────────────┐
                    │    START    │
                    └──────┬──────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Read Message from    │◄────────────────┐
              │       Client           │                 │
              └───────────┬────────────┘                 │
                          │                              │
                          ▼                              │
                   ┌─────────────┐                       │
                   │   Parse     │                       │
                   │  Message    │                       │
                   └──────┬──────┘                       │
                          │                              │
         ┌────────────────┼────────────────┐             │
         │                │                │             │
         ▼                ▼                ▼             │
    ┌─────────┐     ┌─────────┐     ┌─────────┐         │
    │  LOGIN  │     │ PUBLIC  │     │ PRIVATE │         │
    └────┬────┘     └────┬────┘     └────┬────┘         │
         │               │               │              │
         ▼               ▼               ▼              │
    ┌─────────┐     ┌─────────┐     ┌─────────┐         │
    │Validate │     │Broadcast│     │ Forward │         │
    │  User   │     │ to All  │     │to Target│         │
    └────┬────┘     └────┬────┘     └────┬────┘         │
         │               │               │              │
         └───────────────┴───────────────┘              │
                          │                              │
                          ▼                              │
                   ┌─────────────┐                       │
                   │ Connection  │───YES─────────────────┘
                   │   Active?   │
                   └──────┬──────┘
                          │ NO
                          ▼
                ┌─────────────────────┐
                │  Remove from List   │
                │  Broadcast LEAVE    │
                └──────────┬──────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │     END     │
                    └─────────────┘
```

---

## 8. TECHNOLOGY STACK

| Layer | Technology | Mô tả |
|-------|------------|-------|
| Language | Python 3.8+ | Ngôn ngữ lập trình chính |
| GUI | Tkinter | Giao diện người dùng (built-in) |
| Network | socket module | TCP Socket programming |
| Threading | threading module | Xử lý đa luồng |
| Database | sqlite3 | Lưu trữ dữ liệu (built-in) |
| Version Control | Git | Quản lý source code |

---

## 9. CẤU TRÚC THƯ MỤC DỰ ÁN

```
ChatBox/
├── server/
│   ├── server.py              # Main server
│   ├── client_handler.py      # Xử lý từng client
│   ├── database.py            # Quản lý SQLite
│   └── chatbox.db             # Database file
│
├── client/
│   ├── client.py              # Main client + socket
│   ├── gui.py                 # Giao diện Tkinter
│   └── login_gui.py           # Form đăng nhập
│
├── docs/
│   ├── SRS_ChatBox.md
│   ├── KienTrucHeThong.md
│   └── PhanChiaCongViec.md
│
├── requirements.txt           # Dependencies (nếu có)
└── README.md
```

---

*Tài liệu thiết kế kiến trúc - Dự án Chat Box*
