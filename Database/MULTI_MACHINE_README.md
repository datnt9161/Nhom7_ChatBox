# 🌐 CHAT BOX - MULTI-MACHINE SUPPORT

## 🎯 Tính năng chính
✅ **Nhiều máy có thể chat cùng lúc**  
✅ **Database MySQL chia sẻ**  
✅ **Real-time messaging**  
✅ **User management**  
✅ **Private & Public chat**  

---

## 🚀 SETUP NHANH (3 BƯỚC)

### Bước 1: Setup Database Server (1 máy)
```bash
# Cài Docker (nếu chưa có)
# Windows/Mac: Tải Docker Desktop
# Linux: sudo apt install docker.io docker-compose

# Chạy setup
python setup_database.py
# Chọn: 1. Setup máy làm Database Server
# Chọn: y (tự động khởi động Docker)
```

### Bước 2: Setup Client (các máy khác)
```bash
# Copy 3 files này sang máy khác:
# - database.py
# - setup_database.py  
# - client_config_XXX.json (từ máy server)

# Đổi tên file config
mv client_config_XXX.json db_config.json

# Test kết nối
python setup_database.py
# Chọn: 4. Test database hiện tại
```

### Bước 3: Sử dụng
```python
from database import ChatBoxDatabase

db = ChatBoxDatabase()

# Đăng ký user
db.register_user("username", "password", "Tên hiển thị")

# Đăng nhập
user = db.login_user("username", "password")

# Gửi tin nhắn
db.send_public_message(user['id'], "Hello everyone!")

# Lấy tin nhắn
messages = db.get_public_messages(50)
```

---

## 📁 CÁC FILE QUAN TRỌNG

| File | Mục đích | Khi nào dùng |
|------|----------|--------------|
| `database.py` | Core database manager | Tích hợp vào app |
| `setup_database.py` | Setup server/client | Lần đầu cài đặt |
| `chat_demo.py` | Test & demo | Kiểm tra hoạt động |
| `db_config.json` | Cấu hình database | Tự động tạo |

---

## 🔧 KIẾN TRÚC HỆ THỐNG

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Máy A     │    │   Máy B     │    │   Máy C     │
│ (Chat App)  │    │ (Chat App)  │    │ (Chat App)  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
              ┌───────────┴────────────┐
              │   Database Server      │
              │   MySQL + Docker       │
              │   IP: 192.168.1.100    │
              │   Port: 3306           │
              └────────────────────────┘
```

---

## 🎮 TEST & DEMO

### Test tự động (mô phỏng nhiều user):
```bash
python chat_demo.py
# Chọn: 1. Mô phỏng nhiều user chat
```

### Monitor real-time:
```bash
python chat_demo.py
# Chọn: 2. Monitor chat real-time
```

### Chat tương tác:
```bash
python chat_demo.py
# Chọn: 3. Chat tương tác
```

---

## 🔍 TROUBLESHOOTING

### Không kết nối được database:
```bash
# Kiểm tra MySQL có chạy
docker ps

# Kiểm tra port
netstat -an | grep 3306

# Test từ client
telnet SERVER_IP 3306
```

### Lỗi quyền truy cập:
```bash
# Vào phpMyAdmin: http://SERVER_IP:8080
# User: root, Pass: root123
# Kiểm tra user 'chatbox_user' có quyền chưa
```

### Firewall chặn:
```bash
# Windows: Mở Windows Firewall → Allow port 3306
# Linux: sudo ufw allow 3306
```

---

## 📊 THÔNG TIN KỸ THUẬT

### Database Schema:
- **users**: id, username, password, display_name, status, ...
- **messages**: id, sender_id, receiver_id, content, msg_type, ...

### API Functions:
- `register_user()` - Đăng ký user mới
- `login_user()` - Đăng nhập
- `send_public_message()` - Gửi tin nhắn public
- `send_private_message()` - Gửi tin nhắn private
- `get_public_messages()` - Lấy tin nhắn public
- `get_online_users()` - Lấy danh sách user online

### Config Format:
```json
{
  "host": "192.168.1.100",
  "port": 3306,
  "database": "chatbox",
  "username": "chatbox_user",
  "password": "chatbox123",
  "charset": "utf8mb4"
}
```

---

## 🔒 BẢO MẬT

### Production Setup:
1. **Đổi password mặc định**:
   ```sql
   ALTER USER 'chatbox_user'@'%' IDENTIFIED BY 'password_mạnh_mới';
   ```

2. **Giới hạn IP truy cập**:
   ```sql
   CREATE USER 'chatbox_user'@'192.168.1.%' IDENTIFIED BY 'password';
   ```

3. **Sử dụng SSL** (nâng cao):
   - Cấu hình SSL cho MySQL
   - Update connection string với SSL params

---

## 🎯 TÍCH HỢP VÀO ỨNG DỤNG

### Trong Chat Client:
```python
from database import ChatBoxDatabase

class ChatClient:
    def __init__(self):
        self.db = ChatBoxDatabase()
        self.current_user = None
    
    def login(self, username, password):
        self.current_user = self.db.login_user(username, password)
        return self.current_user is not None
    
    def send_message(self, content):
        if self.current_user:
            return self.db.send_public_message(
                self.current_user['id'], content
            )
    
    def get_messages(self):
        return self.db.get_public_messages(50)
    
    def get_online_users(self):
        return self.db.get_online_users()
```

### Trong Chat Server:
```python
# Server chỉ cần forward messages giữa clients
# Database handle tất cả logic lưu trữ
```

---

## 📈 PERFORMANCE

### Tối ưu hóa:
- **Connection pooling**: Sử dụng connection pool
- **Indexing**: Đã tạo index cho các truy vấn thường dùng
- **Caching**: Cache danh sách user online
- **Pagination**: Giới hạn số tin nhắn trả về

### Giới hạn:
- **Concurrent users**: ~100 users đồng thời (tùy server)
- **Message size**: Tối đa ~65KB per message
- **Database size**: Không giới hạn (MySQL)

---

## 🚀 NEXT STEPS

1. **Tích hợp vào GUI**: Tkinter, PyQt, hoặc web interface
2. **Real-time updates**: WebSocket hoặc polling
3. **File sharing**: Upload/download files
4. **Emoji support**: Unicode emoji
5. **Message encryption**: End-to-end encryption
6. **Push notifications**: Desktop notifications
7. **Mobile app**: React Native hoặc Flutter

---

## 📞 HỖ TRỢ

### Commands hữu ích:
```bash
# Xem log MySQL
docker logs chatbox_mysql

# Backup database
docker exec chatbox_mysql mysqldump -u root -proot123 chatbox > backup.sql

# Restore database
docker exec -i chatbox_mysql mysql -u root -proot123 chatbox < backup.sql

# Restart MySQL
docker-compose restart mysql
```

### Kiểm tra status:
```bash
python setup_database.py  # Chọn 4
python chat_demo.py       # Chọn 5
```

**🎉 Chúc bạn thành công với Chat Box multi-machine!**