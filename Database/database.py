#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Box Database - SQLite Local
Database đơn giản chỉ dùng trên local
"""

import sqlite3
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Optional

class ChatDatabase:
    def __init__(self, db_path="chatbox.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Tạo kết nối đến database"""
        return sqlite3.connect(self.db_path)
    
    def hash_password(self, password: str) -> str:
        """Mã hóa mật khẩu bằng SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def init_database(self):
        """Khởi tạo database và tạo bảng"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Tạo bảng users
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    email TEXT,
                    avatar TEXT DEFAULT 'default.png',
                    status TEXT DEFAULT 'offline',
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
                    msg_type TEXT DEFAULT 'PUBLIC',
                    is_read BOOLEAN DEFAULT 0,
                    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users(id),
                    FOREIGN KEY (receiver_id) REFERENCES users(id)
                )
            ''')
            
            # Tạo index
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_sent_at ON messages(sent_at)')
            
            conn.commit()
            
        except Exception as e:
            print(f"Lỗi khởi tạo database: {e}")
        finally:
            conn.close()
    
    # ==================== USER MANAGEMENT ====================
    
    def register_user(self, username: str, password: str, display_name: str, email: str = None) -> bool:
        """Đăng ký user mới"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            hashed_password = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password, display_name, email)
                VALUES (?, ?, ?, ?)
            ''', (username, hashed_password, display_name, email))
            
            conn.commit()
            print(f"✅ Đăng ký user '{username}' thành công!")
            return True
            
        except sqlite3.IntegrityError:
            print(f"❌ Username '{username}' đã tồn tại!")
            return False
        except Exception as e:
            print(f"❌ Lỗi đăng ký: {e}")
            return False
        finally:
            conn.close()
    
    def login_user(self, username: str, password: str) -> Optional[Dict]:
        """Đăng nhập user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            hashed_password = self.hash_password(password)
            cursor.execute('''
                SELECT id, username, display_name, avatar, email
                FROM users 
                WHERE username = ? AND password = ? AND is_active = 1
            ''', (username, hashed_password))
            
            user = cursor.fetchone()
            
            if user:
                user_dict = {
                    'id': user[0],
                    'username': user[1],
                    'display_name': user[2],
                    'avatar': user[3],
                    'email': user[4]
                }
                
                # Cập nhật trạng thái online
                cursor.execute('''
                    UPDATE users 
                    SET status = 'online', last_login = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (user[0],))
                conn.commit()
                
                print(f"✅ Đăng nhập thành công: {user_dict['display_name']}")
                return user_dict
            else:
                print("❌ Sai username hoặc password!")
                return None
                
        except Exception as e:
            print(f"❌ Lỗi đăng nhập: {e}")
            return None
        finally:
            conn.close()
    
    def logout_user(self, user_id: int) -> bool:
        """Đăng xuất user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET status = 'offline' WHERE id = ?
            ''', (user_id,))
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Lỗi đăng xuất: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_users(self) -> List[Dict]:
        """Lấy tất cả users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, username, display_name, email, status, created_at, is_active
                FROM users 
                ORDER BY created_at DESC
            ''')
            
            users = cursor.fetchall()
            return [
                {
                    'id': user[0],
                    'username': user[1],
                    'display_name': user[2],
                    'email': user[3],
                    'status': user[4],
                    'created_at': user[5],
                    'is_active': bool(user[6])
                }
                for user in users
            ]
            
        except Exception as e:
            print(f"❌ Lỗi lấy danh sách user: {e}")
            return []
        finally:
            conn.close()
    
    def get_online_users(self) -> List[Dict]:
        """Lấy danh sách user online"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, username, display_name, avatar
                FROM users 
                WHERE status = 'online' AND is_active = 1
                ORDER BY display_name
            ''')
            
            users = cursor.fetchall()
            return [
                {
                    'id': user[0],
                    'username': user[1],
                    'display_name': user[2],
                    'avatar': user[3]
                }
                for user in users
            ]
            
        except Exception as e:
            print(f"❌ Lỗi lấy danh sách user online: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== MESSAGE MANAGEMENT ====================
    
    def send_public_message(self, sender_id: int, content: str) -> bool:
        """Gửi tin nhắn public"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO messages (sender_id, content, msg_type)
                VALUES (?, ?, 'PUBLIC')
            ''', (sender_id, content))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Lỗi gửi tin nhắn: {e}")
            return False
        finally:
            conn.close()
    
    def send_private_message(self, sender_id: int, receiver_id: int, content: str) -> bool:
        """Gửi tin nhắn private"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO messages (sender_id, receiver_id, content, msg_type)
                VALUES (?, ?, ?, 'PRIVATE')
            ''', (sender_id, receiver_id, content))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Lỗi gửi tin nhắn private: {e}")
            return False
        finally:
            conn.close()
    
    def get_public_messages(self, limit: int = 50) -> List[Dict]:
        """Lấy tin nhắn public gần nhất"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT m.id, m.content, m.sent_at, u.username, u.display_name, u.avatar
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.msg_type IN ('PUBLIC', 'SYSTEM')
                ORDER BY m.sent_at DESC
                LIMIT ?
            ''', (limit,))
            
            messages = cursor.fetchall()
            
            # Đảo ngược để hiển thị từ cũ đến mới
            return [
                {
                    'id': msg[0],
                    'content': msg[1],
                    'sent_at': msg[2],
                    'username': msg[3],
                    'display_name': msg[4],
                    'avatar': msg[5]
                }
                for msg in reversed(messages)
            ]
            
        except Exception as e:
            print(f"❌ Lỗi lấy tin nhắn: {e}")
            return []
        finally:
            conn.close()
    
    def get_private_messages(self, user1_id: int, user2_id: int, limit: int = 100) -> List[Dict]:
        """Lấy tin nhắn private giữa 2 user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT m.id, m.content, m.sent_at, m.sender_id, m.receiver_id,
                       u.username, u.display_name
                FROM messages m
                JOIN users u ON m.sender_id = u.id
                WHERE m.msg_type = 'PRIVATE' 
                  AND ((m.sender_id = ? AND m.receiver_id = ?) 
                       OR (m.sender_id = ? AND m.receiver_id = ?))
                ORDER BY m.sent_at ASC
                LIMIT ?
            ''', (user1_id, user2_id, user2_id, user1_id, limit))
            
            messages = cursor.fetchall()
            return [
                {
                    'id': msg[0],
                    'content': msg[1],
                    'sent_at': msg[2],
                    'sender_id': msg[3],
                    'receiver_id': msg[4],
                    'username': msg[5],
                    'display_name': msg[6]
                }
                for msg in messages
            ]
            
        except Exception as e:
            print(f"❌ Lỗi lấy tin nhắn private: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def get_stats(self) -> Dict:
        """Lấy thống kê database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Đếm users
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'online'")
            online_users = cursor.fetchone()[0]
            
            # Đếm messages
            cursor.execute("SELECT COUNT(*) FROM messages")
            total_messages = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM messages WHERE msg_type = 'PUBLIC'")
            public_messages = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM messages WHERE msg_type = 'PRIVATE'")
            private_messages = cursor.fetchone()[0]
            
            return {
                'total_users': total_users,
                'online_users': online_users,
                'total_messages': total_messages,
                'public_messages': public_messages,
                'private_messages': private_messages
            }
            
        except Exception as e:
            print(f"❌ Lỗi lấy thống kê: {e}")
            return {}
        finally:
            conn.close()
    
    def create_sample_data(self):
        """Tạo dữ liệu mẫu"""
        print("📝 Tạo dữ liệu mẫu...")
        
        # Tạo users mẫu
        sample_users = [
            ('admin', 'admin123', 'Administrator', 'admin@chatbox.com'),
            ('user1', '123456', 'Người dùng 1', 'user1@email.com'),
            ('user2', '123456', 'Người dùng 2', 'user2@email.com'),
            ('demo', 'demo', 'Demo User', 'demo@chatbox.com')
        ]
        
        for username, password, display_name, email in sample_users:
            self.register_user(username, password, display_name, email)
        
        # Đăng nhập admin và gửi tin nhắn chào mừng
        admin = self.login_user('admin', 'admin123')
        if admin:
            self.send_public_message(admin['id'], 'Chào mừng đến với Chat Box!')
            self.send_public_message(admin['id'], 'Hệ thống đã sẵn sàng hoạt động.')
        
        print("✅ Tạo dữ liệu mẫu thành công!")

# ==================== DEMO FUNCTIONS ====================

def demo_database():
    """Demo các chức năng database"""
    print("🚀 DEMO CHAT BOX DATABASE (SQLite Local)")
    print("=" * 50)
    
    # Khởi tạo database
    db = ChatDatabase()
    
    # Tạo dữ liệu mẫu
    db.create_sample_data()
    
    # Hiển thị thống kê
    stats = db.get_stats()
    print(f"\n📊 Thống kê database:")
    print(f"  - Tổng users: {stats['total_users']}")
    print(f"  - Users online: {stats['online_users']}")
    print(f"  - Tổng tin nhắn: {stats['total_messages']}")
    print(f"  - Tin nhắn public: {stats['public_messages']}")
    print(f"  - Tin nhắn private: {stats['private_messages']}")
    
    # Hiển thị users
    users = db.get_all_users()
    print(f"\n👥 Danh sách users ({len(users)}):")
    for user in users:
        status_icon = "🟢" if user['status'] == 'online' else "⚫"
        print(f"  {status_icon} {user['display_name']} ({user['username']})")
    
    # Hiển thị tin nhắn
    messages = db.get_public_messages(10)
    print(f"\n💬 Tin nhắn gần nhất ({len(messages)}):")
    for msg in messages:
        timestamp = datetime.fromisoformat(msg['sent_at']).strftime("%H:%M:%S")
        print(f"  [{timestamp}] {msg['display_name']}: {msg['content']}")
    
    print(f"\n✅ Demo hoàn thành!")
    print(f"📁 Database file: {db.db_path}")
    print(f"📝 Tài khoản test:")
    print(f"  - admin/admin123")
    print(f"  - user1/123456")
    print(f"  - user2/123456")
    print(f"  - demo/demo")

if __name__ == "__main__":
    demo_database()