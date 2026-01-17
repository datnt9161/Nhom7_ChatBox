# ChatBox Client - Giao diện người dùng hiện đại

## Tổng quan

ChatBox Client là ứng dụng chat desktop với giao diện đẹp và hiện đại, được xây dựng bằng Python và Tkinter. Ứng dụng hỗ trợ chat thời gian thực với nhiều tính năng nâng cao.

## Tính năng chính

### 🎨 Giao diện hiện đại
- **Thiết kế Material Design**: Sử dụng màu sắc và typography hiện đại
- **Responsive Layout**: Giao diện tự động điều chỉnh theo kích thước cửa sổ
- **Dark Theme**: Giao diện tối dễ nhìn, giảm mỏi mắt
- **Smooth Animations**: Hiệu ứng chuyển động mượt mà
- **Custom Components**: Các thành phần UI được thiết kế riêng

### 💬 Tính năng Chat
- **Chat công khai**: Gửi tin nhắn đến tất cả người dùng online
- **Chat riêng tư**: Gửi tin nhắn riêng cho người dùng cụ thể
- **Emoji Picker**: Chọn emoji để thêm vào tin nhắn
- **File Attachment**: Đính kèm file (đang phát triển)
- **Message History**: Lưu trữ lịch sử tin nhắn
- **Typing Indicator**: Hiển thị khi người khác đang gõ (đang phát triển)

### 👥 Quản lý người dùng
- **Danh sách Online**: Hiển thị người dùng đang online
- **User Search**: Tìm kiếm người dùng nhanh chóng
- **Unread Messages**: Đếm tin nhắn chưa đọc
- **User Status**: Hiển thị trạng thái online/offline

### 🔐 Bảo mật
- **Mã hóa mật khẩu**: Sử dụng SHA256 hash
- **Xác thực người dùng**: Đăng nhập/đăng ký an toàn
- **Session Management**: Quản lý phiên đăng nhập

### 🔔 Thông báo
- **Toast Notifications**: Thông báo popup đẹp mắt
- **System Messages**: Tin nhắn hệ thống
- **Sound Notifications**: Âm thanh thông báo (đang phát triển)

## Cấu trúc file

```
client/
├── main.py                 # Ứng dụng client cơ bản
├── enhanced_client.py      # Ứng dụng client nâng cao (khuyên dùng)
├── styles.py              # Định nghĩa styles và themes
├── components.py          # Các component UI tái sử dụng
└── README.md             # Tài liệu này
```

## Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Tkinter (có sẵn trong Python)
- Hệ điều hành: Windows, macOS, Linux

### Chạy ứng dụng

1. **Client cơ bản**:
```bash
cd client
python main.py
```

2. **Client nâng cao** (khuyên dùng):
```bash
cd client
python enhanced_client.py
```

### Kết nối đến server

1. Khởi động server trước (xem hướng dẫn trong thư mục `server/`)
2. Mở client
3. Nhập thông tin đăng nhập
4. Cấu hình server (nếu cần):
   - IP: 127.0.0.1 (localhost)
   - Port: 5000 (mặc định)

## Hướng dẫn sử dụng

### Đăng ký tài khoản mới
1. Click nút "📝 Tạo tài khoản"
2. Nhập tên đăng nhập (ít nhất 3 ký tự)
3. Nhập mật khẩu (ít nhất 6 ký tự)
4. Click "Tạo tài khoản"

### Đăng nhập
1. Nhập tên đăng nhập và mật khẩu
2. Click "🔐 Đăng nhập"
3. Chờ kết nối đến server

### Chat công khai
1. Chọn "🌐 Công khai" trong phần loại tin nhắn
2. Nhập tin nhắn vào ô input
3. Nhấn Enter hoặc click "📤" để gửi

### Chat riêng tư
1. Click vào tên người dùng trong danh sách
2. Loại tin nhắn sẽ tự động chuyển sang "🔒 Riêng tư"
3. Nhập và gửi tin nhắn như bình thường

### Sử dụng emoji
1. Click nút "😊" bên cạnh ô nhập tin
2. Chọn emoji từ bảng popup
3. Emoji sẽ được thêm vào tin nhắn

## Tùy chỉnh giao diện

### Thay đổi màu sắc
Chỉnh sửa file `styles.py`:

```python
COLORS = {
    'primary': '#3498db',      # Màu chính
    'secondary': '#2c3e50',    # Màu phụ
    'success': '#27ae60',      # Màu thành công
    'danger': '#e74c3c',       # Màu nguy hiểm
    # ... thêm màu khác
}
```

### Thay đổi font chữ
```python
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'body': ('Segoe UI', 11),
    # ... thêm font khác
}
```

## Tính năng nâng cao

### Component tái sử dụng
- `ModernScrollableFrame`: Khung cuộn hiện đại
- `ChatMessage`: Component tin nhắn
- `UserListItem`: Item trong danh sách người dùng
- `NotificationToast`: Thông báo popup
- `LoadingSpinner`: Spinner loading
- `StatusBar`: Thanh trạng thái

### Animation và hiệu ứng
- Hover effects trên buttons và user items
- Fade in/out animations
- Bounce effects
- Smooth transitions

## Troubleshooting

### Lỗi kết nối
- Kiểm tra server đã chạy chưa
- Kiểm tra IP và Port có đúng không
- Kiểm tra firewall có chặn không

### Lỗi giao diện
- Đảm bảo Python có Tkinter
- Thử chạy với Python 3.8+
- Kiểm tra độ phân giải màn hình

### Lỗi font
- Trên Linux: cài đặt font Segoe UI hoặc thay bằng font khác
- Trên macOS: font sẽ tự động fallback

## Phát triển thêm

### Tính năng có thể thêm
- [ ] Voice messages
- [ ] Video calls
- [ ] File sharing
- [ ] Message encryption
- [ ] Group chats
- [ ] Message reactions
- [ ] Custom themes
- [ ] Plugin system

### Cải thiện hiệu năng
- [ ] Message pagination
- [ ] Lazy loading users
- [ ] Image compression
- [ ] Caching system

## Đóng góp

Nếu bạn muốn đóng góp vào dự án:

1. Fork repository
2. Tạo branch mới cho tính năng
3. Commit changes
4. Push và tạo Pull Request

## License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

---

**Tác giả**: Nhóm phát triển ChatBox  
**Phiên bản**: 1.0.0  
**Ngày cập nhật**: 2024