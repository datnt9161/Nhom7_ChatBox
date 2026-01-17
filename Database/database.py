#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Box Database Manager - Multi-machine Support
Hỗ trợ MySQL để nhiều máy có thể kết nối đồng thời
"""

import mysql.connector
from mysql.connector import Error
import hashlib
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ChatBoxDatabase:
    def __init__(self, config_file="db_config.json"):
        self.config = self.load_config(config_file)
        self.connection = None
    
    def load_config(self, config_file):
        """Load database configuration"""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Default config
            default_config = {
                "host": "localhost",
                "port": 3306,
                "database": "chatbox",
                "username": "chatbox_user",
                "password": "chatbox123",
                "charset": "utf8mb4"
            }
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def connect(self):
        """Kết nối đến MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['username'],
                password=self.config['password'],
                charset=self.config['charset'],
                autocommit=True
            )
            return True
        except Error as e:
            print(f"❌ Lỗi kết nối database: {e}")
            return False
    
    def disconnect(self):
        """Ngắt kết nối"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def hash_password(self, password: str) -> str:
        """Mã hóa mật khẩu"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_tables(self):
        """Tạo các bảng cần thiết"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # Bảng users
            cursor.execute('''
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
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')
            
            # Bảng messages
            cursor.execute('''
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
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            ''')
            
            print("✅ Tạo bảng thành công!")
            return True
            
        except Error as e:
            print(f"❌ Lỗi tạo bảng: {e}")
            return False
        finally:
            cursor.close()
            self.disconnect()
    
    # ==================== USER MANAGEMENT ====================
    
    def register_user(self, username: str, password: str, display_name: str, email: str = None) -> bool:
        """Đăng ký user mới"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, password, display_name, email)
                VALUES (%s, %s, %s, %s)
            ''', (username, hashed_password, display_name, email))
            
            print(f"✅ Đăng ký user '{username}' thành công!")
            return True
            
        except Error as e:
            if "Duplicate entry" in str(e):
                print(f"❌ Username '{username}' đã tồn tại!")
            else:
                print(f"❌ Lỗi đăng ký: {e}")
            return False
        finally:
            cursor.close()
            self.disconnect()
    
    def login_user(self, username: str, password: str) -> Optional[Dict]:
        """Đăng nhập user"""
        if not self.connect():
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, display_name, avatar, email
                FROM users 
                WHERE username = %s AND password = %s AND is_active = TRUE
            ''', (username, hashed_password))
            
            user = cursor.fetchone()
            
            if user:
                # Cập nhật trạng thái online và last_login
                cursor.execute('''
                    UPDATE users 
                    SET status = 'online', last_login = CURRENT_TIMESTAMP 
                    WHERE id = %s
                ''', (user['id'],))
                
                print(f"✅ Đăng nhập thành công: {user['display_name']}")
                return user
            else:
                print("❌ Sai username hoặc password!")
                return None
                
        except Error as e:
            print(f"❌ Lỗi đăng nhập: {e}")
            return None
        finally:
            cursor.close()
            self.disconnect()
    
    def logout_user(self, user_id: int) -> bool:
        """Đăng xuất user"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE users SET status = 'offline' WHERE id = %s
            ''', (user_id,))
            return True
            
        except Error as e:
            print(f"❌ Lỗi đăng xuất: {e}")
            return False
        finally:
            cursor.close()
            self.disconnect()
    
    def get_online_users(self) -> List[Dict]:
        """Lấy danh sách user online"""
        if not self.connect():
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT id, username, display_name, avatar
                FROM users 
                WHERE status = 'online' AND is_active = TRUE
                ORDER BY display_name
            ''')
            
            return cursor.fetchall()
            
        except Error as e:
            print(f"❌ Lỗi lấy danh sách user: {e}")
            return []
        finally:
            cursor.close()
            self.disconnect()
    
    # ==================== MESSAGE MANAGEMENT ====================
    
    def send_public_message(self, sender_id: int, content: str) -> bool:
        """Gửi tin nhắn public"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO messages (sender_id, content, msg_type)
                VALUES (%s, %s, 'PUBLIC')
            ''', (sender_id, content))
            
            return True
            
        except Error as e:
            print(f"❌ Lỗi gửi tin nhắn: {e}")
            return False
        finally:
            cursor.close()
            self.disconnect()
    
    def send_private_message(self, sender_id: int, receiver_id: int, content: str) -> bool:
        """Gửi tin nhắn private"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO messages (sender_id, receiver_id, content, msg_type)
                VALUES (%s, %s, %s, 'PRIVATE')
            ''', (sender_id, receiver_id, content))
            
            return True
            
        except Error as e:
            print(f"❌ Lỗi gửi tin nhắn private: {e}")
            return False
        finally:
            cursor.close()
            self.disconnect()
    
    def get_public_messages(self, limit: int = 50) -> List[Dict]:
        """Lấy tin nhắn public gần nhất"""
        if not self.connect():
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT m.id, m.content, m.sent_at, 
                       u.username, u.display_name, u.avatar
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.msg_type IN ('PUBLIC', 'SYSTEM')
                ORDER BY m.sent_at DESC
                LIMIT %s
            ''', (limit,))
            
            messages = cursor.fetchall()
            return list(reversed(messages))  # Đảo ngược để hiển thị từ cũ đến mới
            
        except Error as e:
            print(f"❌ Lỗi lấy tin nhắn: {e}")
            return []
        finally:
            cursor.close()
            self.disconnect()
    
    def get_private_messages(self, user1_id: int, user2_id: int, limit: int = 100) -> List[Dict]:
        """Lấy tin nhắn private giữa 2 user"""
        if not self.connect():
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT m.id, m.content, m.sent_at, m.sender_id, m.receiver_id,
                       u.username, u.display_name
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.msg_type = 'PRIVATE' 
                  AND ((m.sender_id = %s AND m.receiver_id = %s) 
                       OR (m.sender_id = %s AND m.receiver_id = %s))
                ORDER BY m.sent_at ASC
                LIMIT %s
            ''', (user1_id, user2_id, user2_id, user1_id, limit))
            
            return cursor.fetchall()
            
        except Error as e:
            print(f"❌ Lỗi lấy tin nhắn private: {e}")
            return []
        finally:
            cursor.close()
            self.disconnect()
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def get_stats(self) -> Dict:
        """Lấy thống kê database"""
        if not self.connect():
            return {}
        
        try:
            cursor = self.connection.cursor()
            
            # Đếm users
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'online'")
            online_users = cursor.fetchone()[0]
            
            # Đếm messages
            cursor.execute("SELECT COUNT(*) FROM messages")
            total_messages = cursor.fetchone()[0]
            
            return {
                'total_users': total_users,
                'online_users': online_users,
                'total_messages': total_messages
            }
            
        except Error as e:
            print(f"❌ Lỗi lấy thống kê: {e}")
            return {}
        finally:
            cursor.close()
            self.disconnect()
    
    def test_connection(self) -> bool:
        """Test kết nối database"""
        if self.connect():
            print("✅ Kết nối database thành công!")
            self.disconnect()
            return True
        else:
            print("❌ Không thể kết nối database!")
            return False

# ==================== DEMO FUNCTIONS ====================

def demo_database():
    """Demo các chức năng database"""
    print("🚀 DEMO CHAT BOX DATABASE")
    print("=" * 40)
    
    db = ChatBoxDatabase()
    
    # Test kết nối
    if not db.test_connection():
        print("❌ Không thể kết nối database! Kiểm tra cấu hình.")
        return
    
    # Tạo bảng
    if not db.create_tables():
        print("❌ Không thể tạo bảng!")
        return
    
    # Đăng ký user demo
    print("\n📝 Đăng ký users demo...")
    db.register_user("admin", "admin123", "Administrator", "admin@chatbox.com")
    db.register_user("user1", "123456", "Người dùng 1", "user1@email.com")
    db.register_user("user2", "123456", "Người dùng 2", "user2@email.com")
    
    # Đăng nhập
    print("\n🔐 Test đăng nhập...")
    user = db.login_user("admin", "admin123")
    if user:
        # Gửi tin nhắn
        print("\n💬 Gửi tin nhắn demo...")
        db.send_public_message(user['id'], "Chào mừng đến với Chat Box!")
        db.send_public_message(user['id'], "Hệ thống đã sẵn sàng hoạt động.")
        
        # Lấy tin nhắn
        messages = db.get_public_messages(10)
        print(f"\n📨 Có {len(messages)} tin nhắn:")
        for msg in messages:
            print(f"  [{msg['sent_at']}] {msg['display_name']}: {msg['content']}")
    
    # Thống kê
    stats = db.get_stats()
    print(f"\n📊 Thống kê: {stats}")
    
    print("\n✅ Demo hoàn thành!")

if __name__ == "__main__":
    demo_database()