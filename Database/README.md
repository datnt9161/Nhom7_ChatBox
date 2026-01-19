# 🗄️ DATABASE MODULE

## 📋 Mô tả
Module quản lý database SQLite cho Chat Box Application.

## 📁 Files trong thư mục này

| File | Mục đích |
|------|----------|
| `database.py` | Core database manager - Chức năng chính |
| `manage_db.py` | Database management tool - Quản lý database |
| `chatbox.db` | SQLite database file - File dữ liệu |
| `DATABASE_LOCAL_README.md` | Hướng dẫn chi tiết |

## 🚀 Sử dụng nhanh

### 1. Tạo database và dữ liệu mẫu:
```bash
cd Database
python database.py
```

### 2. Quản lý database:
```bash
cd Database
python manage_db.py
```

### 3. Sử dụng trong code:
```python
import sys
sys.path.append('Database')
from database import ChatDatabase

# Khởi tạo
db = ChatDatabase()

# Đăng nhập
user = db.login_user("admin", "admin123")

# Gửi tin nhắn
db.send_public_message(user['id'], "Hello!")
```

## 👥 Tài khoản test có sẵn
- **admin** / admin123 (Administrator)
- **user1** / 123456 (Người dùng 1)
- **user2** / 123456 (Người dùng 2)
- **demo** / demo (Demo User)

## 🔧 Tính năng chính
- ✅ User registration/login
- ✅ Public & Private messaging
- ✅ Online/Offline status
- ✅ Message history
- ✅ Database backup/restore
- ✅ Interactive chat

## 📖 Hướng dẫn chi tiết
Xem file `DATABASE_LOCAL_README.md` để biết thêm chi tiết.

---
**💡 Lưu ý**: Database này chỉ dùng trên local, không hỗ trợ multi-machine.