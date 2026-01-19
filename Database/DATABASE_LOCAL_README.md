# 🗄️ CHAT BOX DATABASE - LOCAL SQLite

## 📋 Tổng quan
Database SQLite đơn giản chỉ dùng trên local, không cần cài đặt gì thêm.

## 🚀 Sử dụng nhanh

### 1. Chạy demo và tạo dữ liệu mẫu:
```bash
python database.py
```

### 2. Quản lý database:
```bash
python manage_db.py
```

### 3. Sử dụng trong code:
```python
from database import ChatDatabase

# Khởi tạo
db = ChatDatabase()

# Đăng ký user
db.register_user("username", "password", "Tên hiển thị", "email@example.com")

# Đăng nhập
user = db.login_user("username", "password")

# Gửi tin nhắn public
db.send_public_message(user['id'], "Hello everyone!")

# Gửi tin nhắn private
db.send_private_message(user['id'], receiver_id, "Hi there!")

# Lấy tin nhắn
messages = db.get_public_messages(50)
```

## 📁 Files

| File | Mục đích |
|------|----------|
| `database.py` | Core database manager |
| `manage_db.py` | Tool quản lý database |
| `chatbox.db` | File database SQLite (tự tạo) |

## 🔧 Chức năng chính

### User Management:
- ✅ Đăng ký user mới
- ✅ Đăng nhập/đăng xuất
- ✅ Quản lý trạng thái online/offline
- ✅ Lấy danh sách users

### Message Management:
- ✅ Gửi tin nhắn public
- ✅ Gửi tin nhắn private
- ✅ Lấy lịch sử chat
- ✅ Timestamp cho tin nhắn

### Database Features:
- ✅ SQLite - không cần cài đặt
- ✅ Auto-create tables
- ✅ Password hashing (SHA256)
- ✅ Foreign key constraints
- ✅ Indexes cho performance

## 📊 Database Schema

### Bảng `users`:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,           -- SHA256 hash
    display_name TEXT NOT NULL,
    email TEXT,
    avatar TEXT DEFAULT 'default.png',
    status TEXT DEFAULT 'offline',    -- online/offline/away
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);
```

### Bảng `messages`:
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER,              -- NULL = public message
    content TEXT NOT NULL,
    msg_type TEXT DEFAULT 'PUBLIC',   -- PUBLIC/PRIVATE/SYSTEM
    is_read BOOLEAN DEFAULT 0,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);
```

## 🎮 Demo & Test

### Tài khoản mẫu (tự động tạo):
- **admin** / admin123 (Administrator)
- **user1** / 123456 (Người dùng 1)
- **user2** / 123456 (Người dùng 2)
- **demo** / demo (Demo User)

### Test các chức năng:
```bash
python manage_db.py
# Chọn các option để test:
# 1. Xem users
# 2. Xem tin nhắn
# 4. Test đăng nhập
# 6. Chat tương tác
```

## 🔒 Bảo mật

- ✅ Password được hash SHA256
- ✅ SQL injection protection (parameterized queries)
- ✅ Input validation
- ❌ Không có encryption cho tin nhắn (có thể thêm sau)

## 💾 Backup & Recovery

### Backup:
```bash
python manage_db.py
# Chọn: 7. Backup database
```

### Manual backup:
```bash
copy chatbox.db chatbox_backup.db
```

### Reset database:
```bash
python manage_db.py
# Chọn: 8. Reset database
```

## 🔧 Tích hợp vào ứng dụng

### Ví dụ Chat Client:
```python
from database import ChatDatabase

class ChatClient:
    def __init__(self):
        self.db = ChatDatabase()
        self.current_user = None
    
    def login(self, username, password):
        self.current_user = self.db.login_user(username, password)
        return self.current_user is not None
    
    def send_message(self, content):
        if self.current_user:
            return self.db.send_public_message(
                self.current_user['id'], content
            )
        return False
    
    def get_messages(self):
        return self.db.get_public_messages(50)
    
    def get_online_users(self):
        return self.db.get_online_users()
    
    def logout(self):
        if self.current_user:
            self.db.logout_user(self.current_user['id'])
            self.current_user = None

# Sử dụng
client = ChatClient()
if client.login("admin", "admin123"):
    client.send_message("Hello World!")
    messages = client.get_messages()
    client.logout()
```

## 📈 Performance

### Tối ưu hóa có sẵn:
- Index trên username, sender_id, sent_at
- LIMIT cho queries lớn
- Connection management

### Giới hạn:
- SQLite: ~1000 concurrent reads, 1 concurrent write
- File size: Không giới hạn thực tế
- Phù hợp: 1-10 users đồng thời

## 🐛 Troubleshooting

### Database locked:
```python
# Đảm bảo đóng connection
conn = db.get_connection()
# ... làm việc với database
conn.close()  # Quan trọng!
```

### Corrupt database:
```bash
sqlite3 chatbox.db "PRAGMA integrity_check;"
```

### Reset nếu cần:
```bash
python manage_db.py
# Chọn: 8. Reset database
```

## 🎯 Ưu điểm

✅ **Đơn giản**: Không cần cài đặt server  
✅ **Nhanh**: SQLite rất nhanh cho local  
✅ **Portable**: Chỉ 1 file database  
✅ **Reliable**: SQLite rất ổn định  
✅ **Zero-config**: Chạy ngay không cần setup  

## ❌ Nhược điểm

❌ **Single machine**: Chỉ dùng trên 1 máy  
❌ **Limited concurrent writes**: 1 write tại 1 thời điểm  
❌ **No network**: Không thể share qua mạng  

## 🚀 Mở rộng sau này

Nếu cần nhiều máy sử dụng, có thể:
1. Chuyển sang MySQL/PostgreSQL
2. Thêm REST API server
3. Sử dụng file sharing (NFS/SMB)
4. Cloud database (Firebase, Supabase)

---

**💡 Tip**: Database này hoàn hảo cho development, testing, và ứng dụng single-user!