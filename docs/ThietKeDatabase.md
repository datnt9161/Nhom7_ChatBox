# THIẾT KẾ DATABASE - CHAT BOX APPLICATION

---

## 1. TỔNG QUAN

### 1.1 Hệ quản trị CSDL
- **Database**: SQLite 3
- **Lý do chọn**: 
  - Nhẹ, không cần cài đặt server riêng
  - Tích hợp sẵn trong Python (sqlite3 module)
  - Phù hợp cho ứng dụng desktop
  - File-based, dễ backup và di chuyển

### 1.2 File Database
- **Tên file**: `chatbox.db`
- **Vị trí**: `server/chatbox.db`

---

## 2. SƠ ĐỒ QUAN HỆ (ERD)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     ENTITY RELATIONSHIP DIAGRAM                          │
└─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────┐                    ┌─────────────────────┐
    │       USERS         │                    │      MESSAGES       │
    ├─────────────────────┤                    ├─────────────────────┤
    │ PK  id              │                    │ PK  id              │
    │     username        │───────┐            │ FK  sender_id       │
    │     password        │       │            │ FK  receiver_id     │
    │     display_name    │       └───────────►│     content         │
    │     email           │                    │     msg_type        │
    │     avatar          │◄───────────────────│     is_read         │
    │     status          │                    │     sent_at         │
    │     created_at      │                    │     updated_at      │
    │     last_login      │                    └─────────────────────┘
    │     is_active       │
    └─────────────────────┘
              │
              │ 1:N
              ▼
    ┌─────────────────────┐
    │    CHAT_ROOMS       │
    ├─────────────────────┤
    │ PK  id              │
    │     room_name       │
    │     room_type       │
    │ FK  created_by      │
    │     created_at      │
    └─────────────────────┘
              │
              │ N:M
              ▼
    ┌─────────────────────┐
    │   ROOM_MEMBERS      │
    ├─────────────────────┤
    │ PK  id              │
    │ FK  room_id         │
    │ FK  user_id         │
    │     joined_at       │
    │     role            │
    └─────────────────────┘
```

---

## 3. CHI TIẾT CÁC BẢNG

### 3.1 Bảng USERS (Người dùng)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID tự tăng |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Tên đăng nhập |
| password | VARCHAR(255) | NOT NULL | Mật khẩu (đã hash SHA256) |
| display_name | VARCHAR(100) | | Tên hiển thị |
| email | VARCHAR(100) | UNIQUE | Email |
| avatar | VARCHAR(255) | | Đường dẫn ảnh đại diện |
| status | VARCHAR(20) | DEFAULT 'offline' | online/offline/away |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Ngày tạo |
| last_login | DATETIME | | Lần đăng nhập cuối |
| is_active | BOOLEAN | DEFAULT 1 | Tài khoản còn hoạt động |


**SQL tạo bảng:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    avatar VARCHAR(255) DEFAULT 'default.png',
    status VARCHAR(20) DEFAULT 'offline',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Index để tăng tốc tìm kiếm
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_status ON users(status);
```

---

### 3.2 Bảng MESSAGES (Tin nhắn)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID tự tăng |
| sender_id | INTEGER | FOREIGN KEY, NOT NULL | ID người gửi |
| receiver_id | INTEGER | FOREIGN KEY | ID người nhận (NULL = public) |
| content | TEXT | NOT NULL | Nội dung tin nhắn |
| msg_type | VARCHAR(20) | DEFAULT 'PUBLIC' | PUBLIC/PRIVATE/SYSTEM |
| is_read | BOOLEAN | DEFAULT 0 | Đã đọc chưa |
| sent_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Thời gian gửi |
| updated_at | DATETIME | | Thời gian sửa |

**SQL tạo bảng:**
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER,
    content TEXT NOT NULL,
    msg_type VARCHAR(20) DEFAULT 'PUBLIC',
    is_read BOOLEAN DEFAULT 0,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Index để tăng tốc query tin nhắn
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_receiver ON messages(receiver_id);
CREATE INDEX idx_messages_sent_at ON messages(sent_at);
CREATE INDEX idx_messages_type ON messages(msg_type);
```

---

### 3.3 Bảng CHAT_ROOMS (Phòng chat - Optional)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID tự tăng |
| room_name | VARCHAR(100) | NOT NULL | Tên phòng |
| room_type | VARCHAR(20) | DEFAULT 'public' | public/private/group |
| created_by | INTEGER | FOREIGN KEY | Người tạo phòng |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Ngày tạo |

**SQL tạo bảng:**
```sql
CREATE TABLE chat_rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name VARCHAR(100) NOT NULL,
    room_type VARCHAR(20) DEFAULT 'public',
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);
```

---

### 3.4 Bảng ROOM_MEMBERS (Thành viên phòng - Optional)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID tự tăng |
| room_id | INTEGER | FOREIGN KEY, NOT NULL | ID phòng |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | ID user |
| joined_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Ngày tham gia |
| role | VARCHAR(20) | DEFAULT 'member' | admin/member |

**SQL tạo bảng:**
```sql
CREATE TABLE room_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) DEFAULT 'member',
    FOREIGN KEY (room_id) REFERENCES chat_rooms(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(room_id, user_id)
);
```

---

## 4. CÁC TRUY VẤN THƯỜNG DÙNG


### 4.1 Đăng ký user mới
```sql
INSERT INTO users (username, password, display_name, email) 
VALUES ('user1', 'hashed_password', 'User One', 'user1@email.com');
```

### 4.2 Đăng nhập (kiểm tra credentials)
```sql
SELECT id, username, display_name, avatar 
FROM users 
WHERE username = ? AND password = ? AND is_active = 1;
```

### 4.3 Cập nhật trạng thái online
```sql
UPDATE users 
SET status = 'online', last_login = CURRENT_TIMESTAMP 
WHERE id = ?;
```

### 4.4 Lấy danh sách user online
```sql
SELECT id, username, display_name, avatar 
FROM users 
WHERE status = 'online' AND is_active = 1;
```

### 4.5 Lưu tin nhắn public
```sql
INSERT INTO messages (sender_id, content, msg_type) 
VALUES (?, ?, 'PUBLIC');
```

### 4.6 Lưu tin nhắn private
```sql
INSERT INTO messages (sender_id, receiver_id, content, msg_type) 
VALUES (?, ?, ?, 'PRIVATE');
```

### 4.7 Lấy lịch sử chat public (50 tin gần nhất)
```sql
SELECT m.id, m.content, m.sent_at, u.username, u.display_name, u.avatar
FROM messages m
JOIN users u ON m.sender_id = u.id
WHERE m.msg_type = 'PUBLIC'
ORDER BY m.sent_at DESC
LIMIT 50;
```

### 4.8 Lấy lịch sử chat private giữa 2 user
```sql
SELECT m.id, m.content, m.sent_at, m.sender_id, m.receiver_id,
       u.username as sender_name
FROM messages m
JOIN users u ON m.sender_id = u.id
WHERE m.msg_type = 'PRIVATE' 
  AND ((m.sender_id = ? AND m.receiver_id = ?) 
       OR (m.sender_id = ? AND m.receiver_id = ?))
ORDER BY m.sent_at ASC;
```

### 4.9 Đánh dấu tin nhắn đã đọc
```sql
UPDATE messages 
SET is_read = 1 
WHERE receiver_id = ? AND sender_id = ? AND is_read = 0;
```

### 4.10 Đếm tin nhắn chưa đọc
```sql
SELECT sender_id, COUNT(*) as unread_count
FROM messages
WHERE receiver_id = ? AND is_read = 0
GROUP BY sender_id;
```

---

## 5. DATA DICTIONARY

### 5.1 Giải thích các trường

| Trường | Ý nghĩa | Giá trị mẫu |
|--------|---------|-------------|
| username | Tên đăng nhập duy nhất | "john_doe" |
| password | Mật khẩu đã mã hóa SHA256 | "a665a45920422f9d..." |
| display_name | Tên hiển thị trong chat | "John Doe" |
| status | Trạng thái hoạt động | "online", "offline", "away" |
| msg_type | Loại tin nhắn | "PUBLIC", "PRIVATE", "SYSTEM" |
| is_read | Trạng thái đọc tin | 0 (chưa đọc), 1 (đã đọc) |
| role | Vai trò trong phòng | "admin", "member" |

### 5.2 Quy tắc nghiệp vụ

1. **Username**: 3-50 ký tự, chỉ chứa chữ, số và underscore
2. **Password**: Tối thiểu 6 ký tự, được hash SHA256 trước khi lưu
3. **Message**: Tối đa 5000 ký tự
4. **Tin nhắn PUBLIC**: receiver_id = NULL
5. **Tin nhắn PRIVATE**: receiver_id = ID người nhận

---

## 6. BACKUP & RECOVERY

### 6.1 Backup database
```bash
# Copy file database
cp chatbox.db chatbox_backup_$(date +%Y%m%d).db

# Hoặc dùng sqlite3
sqlite3 chatbox.db ".backup 'chatbox_backup.db'"
```

### 6.2 Restore database
```bash
cp chatbox_backup.db chatbox.db
```

---

## 7. SCRIPT KHỞI TẠO DATABASE

```python
import sqlite3
import hashlib

def init_database(db_path="chatbox.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tạo bảng users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            display_name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            avatar VARCHAR(255) DEFAULT 'default.png',
            status VARCHAR(20) DEFAULT 'offline',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tạo bảng messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER,
            content TEXT NOT NULL,
            msg_type VARCHAR(20) DEFAULT 'PUBLIC',
            is_read BOOLEAN DEFAULT 0,
            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    ''')
    
    # Tạo indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_receiver ON messages(receiver_id)')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
```

---

*Tài liệu thiết kế Database - Dự án Chat Box*
