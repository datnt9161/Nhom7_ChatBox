#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Database cho Chat Box - Multi-machine Support
Hướng dẫn setup MySQL để nhiều máy có thể chat cùng lúc
"""

import json
import subprocess
import socket
import os
from database import ChatBoxDatabase

def get_local_ip():
    """Lấy IP của máy hiện tại"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def create_server_config(server_ip="localhost"):
    """Tạo config cho máy server"""
    config = {
        "host": server_ip,
        "port": 3306,
        "database": "chatbox",
        "username": "chatbox_user",
        "password": "chatbox123",
        "charset": "utf8mb4"
    }
    
    with open("db_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Tạo config server: db_config.json")
    return config

def create_client_config(server_ip):
    """Tạo config cho máy client"""
    config = {
        "host": server_ip,
        "port": 3306,
        "database": "chatbox",
        "username": "chatbox_user",
        "password": "chatbox123",
        "charset": "utf8mb4"
    }
    
    filename = f"client_config_{server_ip.replace('.', '_')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Tạo config client: {filename}")
    return filename

def create_docker_setup():
    """Tạo Docker setup cho MySQL"""
    
    # Docker Compose file
    docker_compose = """version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: chatbox_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: chatbox
      MYSQL_USER: chatbox_user
      MYSQL_PASSWORD: chatbox123
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    command: --default-authentication-plugin=mysql_native_password

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: chatbox_phpmyadmin
    restart: always
    ports:
      - "8080:80"
    environment:
      PMA_HOST: mysql
      PMA_USER: root
      PMA_PASSWORD: root123
    depends_on:
      - mysql

volumes:
  mysql_data:
"""
    
    # SQL init file
    init_sql = """-- Khởi tạo database Chat Box
CREATE DATABASE IF NOT EXISTS chatbox CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tạo user cho ứng dụng
CREATE USER IF NOT EXISTS 'chatbox_user'@'%' IDENTIFIED BY 'chatbox123';
GRANT ALL PRIVILEGES ON chatbox.* TO 'chatbox_user'@'%';
FLUSH PRIVILEGES;

USE chatbox;

-- Tạo bảng users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    avatar VARCHAR(255) DEFAULT 'default.png',
    status ENUM('online', 'offline', 'away') DEFAULT 'offline',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tạo bảng messages
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NULL,
    content TEXT NOT NULL,
    msg_type ENUM('PUBLIC', 'PRIVATE', 'SYSTEM') DEFAULT 'PUBLIC',
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_sender (sender_id),
    INDEX idx_receiver (receiver_id),
    INDEX idx_sent_at (sent_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tạo user admin mặc định
INSERT IGNORE INTO users (username, password, display_name, email) 
VALUES ('admin', SHA2('admin123', 256), 'Administrator', 'admin@chatbox.com');

-- Tin nhắn chào mừng
INSERT IGNORE INTO messages (sender_id, content, msg_type) 
VALUES (1, 'Chào mừng đến với Chat Box! Hệ thống đã sẵn sàng.', 'SYSTEM');
"""
    
    with open("docker-compose.yml", "w", encoding="utf-8") as f:
        f.write(docker_compose)
    
    with open("init.sql", "w", encoding="utf-8") as f:
        f.write(init_sql)
    
    print("✅ Tạo Docker setup: docker-compose.yml, init.sql")

def setup_server():
    """Setup máy làm database server"""
    print("🖥️  SETUP DATABASE SERVER")
    print("=" * 40)
    
    local_ip = get_local_ip()
    print(f"📍 IP máy này: {local_ip}")
    
    print("\n🐳 SETUP VỚI DOCKER (Khuyến nghị)")
    print("1. Tạo Docker setup")
    print("2. Khởi động MySQL container")
    print("3. Tạo config files")
    
    # Tạo Docker setup
    create_docker_setup()
    
    # Tạo config
    create_server_config(local_ip)
    
    print(f"\n🚀 CHẠY CÁC LỆNH SAU:")
    print("1. docker-compose up -d")
    print("2. python database.py  # Test database")
    
    # Hỏi có muốn tự động chạy không
    auto_run = input("\nBạn có muốn tự động chạy Docker? (y/n): ").lower()
    if auto_run == 'y':
        try:
            print("🚀 Đang khởi động MySQL...")
            subprocess.run(['docker-compose', 'up', '-d'], check=True)
            print("✅ MySQL đã khởi động!")
            
            # Đợi MySQL khởi động
            print("⏳ Đợi MySQL khởi động hoàn toàn (30s)...")
            import time
            time.sleep(30)
            
            # Test database
            print("🔍 Test database...")
            db = ChatBoxDatabase()
            if db.test_connection():
                db.create_tables()
                print("✅ Database sẵn sàng!")
            
        except subprocess.CalledProcessError:
            print("❌ Lỗi khởi động Docker. Chạy thủ công: docker-compose up -d")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    # Tạo config cho client
    client_file = create_client_config(local_ip)
    
    print(f"\n✅ SETUP SERVER HOÀN THÀNH!")
    print(f"📍 Server IP: {local_ip}")
    print(f"🔗 MySQL: {local_ip}:3306")
    print(f"🌐 phpMyAdmin: http://{local_ip}:8080")
    print(f"📁 File cho client: {client_file}")
    print(f"\n📋 HƯỚNG DẪN CHO MÁY KHÁC:")
    print(f"1. Copy file {client_file} sang máy khác")
    print(f"2. Đổi tên thành db_config.json")
    print(f"3. Chạy python database.py để test")

def setup_client():
    """Setup máy client"""
    print("💻 SETUP CLIENT")
    print("=" * 40)
    
    server_ip = input("Nhập IP của database server: ").strip()
    if not server_ip:
        print("❌ IP không được để trống!")
        return
    
    # Test kết nối
    print(f"🔍 Test kết nối đến {server_ip}:3306...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((server_ip, 3306))
        sock.close()
        
        if result == 0:
            print("✅ Kết nối thành công!")
        else:
            print("❌ Không thể kết nối!")
            print("🔧 Kiểm tra:")
            print("- Server đã khởi động MySQL chưa?")
            print("- Firewall có chặn port 3306?")
            print("- IP có đúng không?")
            return
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return
    
    # Tạo config
    config = {
        "host": server_ip,
        "port": 3306,
        "database": "chatbox",
        "username": "chatbox_user",
        "password": "chatbox123",
        "charset": "utf8mb4"
    }
    
    with open("db_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # Test database
    print("🔍 Test database...")
    db = ChatBoxDatabase()
    if db.test_connection():
        print("✅ Setup client thành công!")
        
        # Hiển thị thống kê
        stats = db.get_stats()
        print(f"📊 Thống kê database: {stats}")
    else:
        print("❌ Không thể kết nối database!")

def show_usage_guide():
    """Hướng dẫn sử dụng"""
    print("📖 HƯỚNG DẪN SỬ DỤNG")
    print("=" * 40)
    
    print("""
🏗️  KIẾN TRÚC HỆ THỐNG:

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Máy A      │    │  Máy B      │    │  Máy C      │
│  (Client)   │    │  (Client)   │    │  (Client)   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
              ┌───────────┴────────────┐
              │    Database Server     │
              │    MySQL + Docker      │
              └────────────────────────┘

🔧 CÁC BƯỚC THỰC HIỆN:

1. SETUP SERVER (1 máy):
   - Chọn 1 máy có IP cố định làm server
   - Chạy: python setup_database.py → chọn 1
   - Khởi động MySQL với Docker
   - Lấy file config cho client

2. SETUP CLIENT (các máy khác):
   - Copy file config từ server
   - Chạy: python setup_database.py → chọn 2
   - Test kết nối

3. SỬ DỤNG TRONG CODE:
   from database import ChatBoxDatabase
   
   db = ChatBoxDatabase()
   
   # Đăng ký user
   db.register_user("username", "password", "Tên hiển thị")
   
   # Đăng nhập
   user = db.login_user("username", "password")
   
   # Gửi tin nhắn public
   db.send_public_message(user['id'], "Hello everyone!")
   
   # Lấy tin nhắn
   messages = db.get_public_messages(50)

⚠️  LƯU Ý:
- Server cần có IP cố định
- Mở firewall port 3306
- Tất cả máy phải cùng mạng LAN hoặc có kết nối internet
- Backup database định kỳ

🔐 BẢO MẬT:
- Đổi password mặc định trong production
- Sử dụng SSL/TLS nếu qua internet
- Giới hạn IP được phép kết nối
""")

def main():
    """Menu chính"""
    print("🌐 CHAT BOX DATABASE SETUP")
    print("Hỗ trợ nhiều máy chat cùng lúc")
    print("=" * 50)
    
    print("📋 CHỌN CHỨC NĂNG:")
    print("1. Setup máy làm Database Server")
    print("2. Setup máy Client")
    print("3. Hướng dẫn sử dụng")
    print("4. Test database hiện tại")
    print("0. Thoát")
    
    choice = input("\nChọn (0-4): ").strip()
    
    if choice == "1":
        setup_server()
    elif choice == "2":
        setup_client()
    elif choice == "3":
        show_usage_guide()
    elif choice == "4":
        print("🔍 Test database...")
        db = ChatBoxDatabase()
        if db.test_connection():
            stats = db.get_stats()
            print(f"📊 Thống kê: {stats}")
            
            # Hiển thị user online
            users = db.get_online_users()
            print(f"👥 Users online: {len(users)}")
            for user in users:
                print(f"  - {user['display_name']} ({user['username']})")
        else:
            print("❌ Không thể kết nối database!")
    elif choice == "0":
        print("👋 Tạm biệt!")
    else:
        print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()