# TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)
# ỨNG DỤNG CHAT BOX - MÔN LẬP TRÌNH MẠNG

---

## 1. GIỚI THIỆU

### 1.1 Mục đích
Tài liệu này mô tả đặc tả yêu cầu phần mềm cho ứng dụng Chat Box, một ứng dụng nhắn tin thời gian thực sử dụng kiến thức lập trình mạng (Socket Programming).

### 1.2 Phạm vi
- Tên sản phẩm: ChatBox Application
- Ứng dụng cho phép nhiều người dùng chat với nhau trong thời gian thực
- Sử dụng mô hình Client-Server
- Giao thức: TCP/IP Socket

### 1.3 Đối tượng sử dụng
- Sinh viên, người dùng cần trao đổi thông tin qua mạng LAN/Internet

---

## 2. MÔ TẢ TỔNG QUAN

### 2.1 Góc nhìn sản phẩm
```
┌─────────────┐     TCP/IP      ┌─────────────┐
│   Client 1  │◄───────────────►│             │
└─────────────┘                 │             │
                                │   SERVER    │
┌─────────────┐     TCP/IP      │             │
│   Client 2  │◄───────────────►│             │
└─────────────┘                 └─────────────┘
```

### 2.2 Chức năng chính
| STT | Chức năng | Mô tả |
|-----|-----------|-------|
| 1 | Đăng ký/Đăng nhập | Người dùng tạo tài khoản và đăng nhập |
| 2 | Chat công khai | Gửi tin nhắn đến tất cả người dùng online |
| 3 | Chat riêng tư | Gửi tin nhắn riêng cho một người dùng cụ thể |
| 4 | Danh sách online | Hiển thị danh sách người dùng đang online |
| 5 | Gửi file | Gửi file cho người dùng khác |
| 6 | Thông báo | Thông báo khi có người vào/rời phòng chat |

### 2.3 Công nghệ sử dụng
- Ngôn ngữ: Python 3.8+
- Giao thức: TCP Socket
- GUI: Tkinter (có sẵn trong Python)
- Database: SQLite (có sẵn trong Python)
- Thư viện: socket, threading, sqlite3, tkinter

---

## 3. YÊU CẦU CHỨC NĂNG

### 3.1 Module Server

#### 3.1.1 Khởi tạo Server
- **Input**: Port number
- **Process**: Tạo ServerSocket, lắng nghe kết nối
- **Output**: Server sẵn sàng nhận kết nối

#### 3.1.2 Quản lý kết nối
- Chấp nhận kết nối từ Client
- Tạo Thread riêng cho mỗi Client
- Quản lý danh sách Client đang kết nối

#### 3.1.3 Xử lý tin nhắn
- Nhận tin nhắn từ Client
- Phân loại tin nhắn (public/private)
- Chuyển tiếp tin nhắn đến đích

#### 3.1.4 Quản lý User
- Xác thực đăng nhập
- Lưu trữ thông tin user
- Cập nhật trạng thái online/offline

### 3.2 Module Client

#### 3.2.1 Kết nối Server
- **Input**: IP Server, Port
- **Process**: Tạo Socket kết nối đến Server
- **Output**: Kết nối thành công/thất bại

#### 3.2.2 Giao diện người dùng
- Form đăng nhập/đăng ký
- Cửa sổ chat chính
- Danh sách người dùng online
- Khu vực nhập tin nhắn

#### 3.2.3 Gửi/Nhận tin nhắn
- Gửi tin nhắn đến Server
- Nhận và hiển thị tin nhắn từ Server
- Hỗ trợ emoji cơ bản

---

## 4. YÊU CẦU PHI CHỨC NĂNG

### 4.1 Hiệu năng
- Server hỗ trợ tối thiểu 10 Client đồng thời
- Độ trễ tin nhắn < 1 giây trong mạng LAN

### 4.2 Bảo mật
- Mật khẩu được mã hóa khi lưu trữ
- Xác thực người dùng trước khi chat

### 4.3 Khả năng sử dụng
- Giao diện thân thiện, dễ sử dụng
- Hỗ trợ tiếng Việt

### 4.4 Độ tin cậy
- Xử lý ngắt kết nối đột ngột
- Thông báo lỗi rõ ràng

---

## 5. THIẾT KẾ HỆ THỐNG

### 5.1 Kiến trúc hệ thống
```
┌────────────────────────────────────────────────────────┐
│                      CLIENT                            │
├────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │     GUI      │  │ Message      │  │   Socket     │ │
│  │   Layer      │  │ Handler      │  │   Handler    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────────────────────────────────────────┘
                          │
                          │ TCP/IP
                          ▼
┌────────────────────────────────────────────────────────┐
│                      SERVER                            │
├────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Socket     │  │   Client     │  │   Database   │ │
│  │   Listener   │  │   Manager    │  │   Handler    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────────────────────────────────────────┘
```

### 5.2 Giao thức tin nhắn
```
Format: [TYPE]|[SENDER]|[RECEIVER]|[CONTENT]|[TIMESTAMP]

Ví dụ:
- PUBLIC|user1|ALL|Hello everyone|2024-01-15 10:30:00
- PRIVATE|user1|user2|Hi there|2024-01-15 10:31:00
- LOGIN|user1|SERVER|password123|2024-01-15 10:29:00
- USERLIST|SERVER|user1|user2,user3,user4|2024-01-15 10:30:00
```

### 5.3 Sơ đồ Use Case
```
                    ┌─────────────────┐
                    │    Người dùng   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Đăng ký/     │  │   Chat công     │  │   Chat riêng    │
│  Đăng nhập    │  │   khai          │  │   tư            │
└───────────────┘  └─────────────────┘  └─────────────────┘
        │                    │                    │
        │                    ▼                    │
        │          ┌─────────────────┐            │
        └─────────►│  Xem danh sách  │◄───────────┘
                   │  online         │
                   └─────────────────┘
```

---

## 6. DATABASE SCHEMA

### 6.1 Bảng Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);
```

### 6.2 Bảng Messages (Optional - lưu lịch sử)
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    content TEXT,
    message_type VARCHAR(20),
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);
```

---

## 7. GIAO DIỆN NGƯỜI DÙNG (MOCKUP)

### 7.1 Màn hình đăng nhập
```
┌─────────────────────────────────────┐
│           CHAT BOX LOGIN            │
├─────────────────────────────────────┤
│                                     │
│   Username: [________________]      │
│                                     │
│   Password: [________________]      │
│                                     │
│   [  Đăng nhập  ]  [  Đăng ký  ]   │
│                                     │
│   Server IP: [________________]     │
│   Port:      [________________]     │
│                                     │
└─────────────────────────────────────┘
```

### 7.2 Màn hình chat chính
```
┌─────────────────────────────────────────────────────────┐
│  CHAT BOX - Welcome, User1                    [X]       │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────────────────────────────┐ │
│ │ ONLINE (3)  │ │ [Public Chat]                       │ │
│ ├─────────────┤ ├─────────────────────────────────────┤ │
│ │ ● User2     │ │ User2: Chào mọi người!              │ │
│ │ ● User3     │ │ User3: Hi!                          │ │
│ │ ● User4     │ │ You: Hello everyone                 │ │
│ │             │ │                                     │ │
│ │             │ │                                     │ │
│ │             │ │                                     │ │
│ └─────────────┘ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ [Nhập tin nhắn...]                        [Gửi]    │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 8. KẾ HOẠCH KIỂM THỬ

### 8.1 Test Cases

| ID | Mô tả | Input | Expected Output |
|----|-------|-------|-----------------|
| TC01 | Đăng ký thành công | username, password hợp lệ | Tạo tài khoản thành công |
| TC02 | Đăng nhập thành công | credentials đúng | Vào màn hình chat |
| TC03 | Gửi tin public | Tin nhắn | Tất cả user nhận được |
| TC04 | Gửi tin private | Tin nhắn + user đích | Chỉ user đích nhận |
| TC05 | Ngắt kết nối | Đóng client | Server cập nhật list |

---

## 9. TIMELINE DỰ KIẾN

| Tuần | Công việc |
|------|-----------|
| 1 | Thiết kế, setup project, tạo Server cơ bản |
| 2 | Hoàn thiện Server, bắt đầu Client |
| 3 | Hoàn thiện Client, tích hợp |
| 4 | Testing, fix bug, hoàn thiện báo cáo |

---

## 10. TÀI LIỆU THAM KHẢO

1. Java Socket Programming - Oracle Documentation
2. TCP/IP Protocol - RFC 793
3. Multi-threaded Server Design Patterns
4. GUI Programming with JavaFX/Tkinter

---

*Tài liệu được tạo cho bài tập cuối kỳ môn Lập trình mạng*
