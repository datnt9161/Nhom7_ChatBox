#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Demo - Test nhiều máy chat cùng lúc
Mô phỏng nhiều user chat đồng thời
"""

import threading
import time
import random
from database import ChatBoxDatabase

class ChatUser:
    def __init__(self, username, password, display_name):
        self.username = username
        self.password = password
        self.display_name = display_name
        self.user_id = None
        self.db = ChatBoxDatabase()
        self.is_online = False
    
    def login(self):
        """Đăng nhập user"""
        user = self.db.login_user(self.username, self.password)
        if user:
            self.user_id = user['id']
            self.is_online = True
            print(f"✅ {self.display_name} đã đăng nhập")
            return True
        else:
            print(f"❌ {self.display_name} đăng nhập thất bại")
            return False
    
    def logout(self):
        """Đăng xuất user"""
        if self.user_id:
            self.db.logout_user(self.user_id)
            self.is_online = False
            print(f"👋 {self.display_name} đã đăng xuất")
    
    def send_message(self, content):
        """Gửi tin nhắn public"""
        if self.is_online and self.user_id:
            success = self.db.send_public_message(self.user_id, content)
            if success:
                print(f"💬 {self.display_name}: {content}")
            return success
        return False
    
    def send_private_message(self, receiver_id, content):
        """Gửi tin nhắn private"""
        if self.is_online and self.user_id:
            success = self.db.send_private_message(self.user_id, receiver_id, content)
            if success:
                print(f"🔒 {self.display_name} → User {receiver_id}: {content}")
            return success
        return False
    
    def auto_chat(self, duration=60):
        """Tự động chat trong thời gian nhất định"""
        messages = [
            "Chào mọi người!",
            "Hôm nay thế nào?",
            "Ai đang online không?",
            "Chat box này hay quá!",
            "Mình mới tham gia nih",
            "Có ai muốn chat private không?",
            "Hệ thống chạy mượt quá!",
            "Cảm ơn admin đã tạo chat box này",
            "Mọi người ở đâu vậy?",
            "Tính năng này rất hữu ích!"
        ]
        
        start_time = time.time()
        while time.time() - start_time < duration and self.is_online:
            # Random gửi tin nhắn
            if random.random() < 0.3:  # 30% chance gửi tin
                message = random.choice(messages)
                self.send_message(message)
            
            # Nghỉ random 2-8 giây
            time.sleep(random.uniform(2, 8))

def create_demo_users():
    """Tạo users demo"""
    print("👥 Tạo users demo...")
    
    db = ChatBoxDatabase()
    
    demo_users = [
        ("alice", "123456", "Alice Nguyễn"),
        ("bob", "123456", "Bob Trần"),
        ("charlie", "123456", "Charlie Lê"),
        ("diana", "123456", "Diana Phạm"),
        ("eve", "123456", "Eve Hoàng")
    ]
    
    for username, password, display_name in demo_users:
        db.register_user(username, password, display_name)
    
    print(f"✅ Tạo {len(demo_users)} users demo")

def simulate_multi_user_chat():
    """Mô phỏng nhiều user chat cùng lúc"""
    print("🚀 MÔ PHỎNG MULTI-USER CHAT")
    print("=" * 40)
    
    # Tạo users demo
    create_demo_users()
    
    # Tạo các ChatUser objects
    users = [
        ChatUser("alice", "123456", "Alice Nguyễn"),
        ChatUser("bob", "123456", "Bob Trần"),
        ChatUser("charlie", "123456", "Charlie Lê"),
        ChatUser("diana", "123456", "Diana Phạm")
    ]
    
    # Đăng nhập tất cả users
    print("\n🔐 Đăng nhập users...")
    for user in users:
        if not user.login():
            users.remove(user)
    
    print(f"\n💬 Bắt đầu chat với {len(users)} users...")
    
    # Tạo threads cho mỗi user
    threads = []
    for user in users:
        thread = threading.Thread(target=user.auto_chat, args=(30,))  # Chat 30 giây
        threads.append(thread)
        thread.start()
    
    # Đợi tất cả threads hoàn thành
    for thread in threads:
        thread.join()
    
    # Đăng xuất tất cả users
    print("\n👋 Đăng xuất users...")
    for user in users:
        user.logout()
    
    print("\n✅ Demo hoàn thành!")

def monitor_chat():
    """Monitor chat real-time"""
    print("📺 MONITOR CHAT REAL-TIME")
    print("=" * 40)
    print("Nhấn Ctrl+C để dừng\n")
    
    db = ChatBoxDatabase()
    last_message_id = 0
    
    try:
        while True:
            # Lấy tin nhắn mới
            messages = db.get_public_messages(10)
            
            for msg in messages:
                if msg['id'] > last_message_id:
                    timestamp = msg['sent_at'].strftime("%H:%M:%S")
                    print(f"[{timestamp}] {msg['display_name']}: {msg['content']}")
                    last_message_id = msg['id']
            
            # Hiển thị users online
            users = db.get_online_users()
            if users:
                user_names = [u['display_name'] for u in users]
                print(f"🟢 Online ({len(users)}): {', '.join(user_names)}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n👋 Dừng monitor")

def interactive_chat():
    """Chat tương tác"""
    print("💬 CHAT TƯƠNG TÁC")
    print("=" * 40)
    
    # Đăng nhập
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    db = ChatBoxDatabase()
    user = db.login_user(username, password)
    
    if not user:
        print("❌ Đăng nhập thất bại!")
        return
    
    print(f"✅ Chào {user['display_name']}!")
    print("Gõ tin nhắn và nhấn Enter. Gõ 'quit' để thoát.\n")
    
    try:
        while True:
            # Hiển thị tin nhắn mới
            messages = db.get_public_messages(5)
            for msg in messages[-3:]:  # Hiển thị 3 tin gần nhất
                timestamp = msg['sent_at'].strftime("%H:%M:%S")
                if msg['username'] != username:  # Không hiển thị tin nhắn của chính mình
                    print(f"[{timestamp}] {msg['display_name']}: {msg['content']}")
            
            # Nhập tin nhắn
            message = input(f"{user['display_name']}: ").strip()
            
            if message.lower() == 'quit':
                break
            
            if message:
                db.send_public_message(user['id'], message)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    
    # Đăng xuất
    db.logout_user(user['id'])
    print(f"\n👋 Tạm biệt {user['display_name']}!")

def main():
    """Menu chính"""
    print("🎮 CHAT BOX DEMO")
    print("Test nhiều máy chat cùng lúc")
    print("=" * 40)
    
    print("📋 CHỌN CHỨC NĂNG:")
    print("1. Mô phỏng nhiều user chat (Auto)")
    print("2. Monitor chat real-time")
    print("3. Chat tương tác")
    print("4. Tạo users demo")
    print("5. Xem thống kê")
    print("0. Thoát")
    
    choice = input("\nChọn (0-5): ").strip()
    
    if choice == "1":
        simulate_multi_user_chat()
    elif choice == "2":
        monitor_chat()
    elif choice == "3":
        interactive_chat()
    elif choice == "4":
        create_demo_users()
    elif choice == "5":
        db = ChatBoxDatabase()
        if db.test_connection():
            stats = db.get_stats()
            print(f"\n📊 Thống kê database:")
            print(f"  - Tổng users: {stats.get('total_users', 0)}")
            print(f"  - Users online: {stats.get('online_users', 0)}")
            print(f"  - Tổng tin nhắn: {stats.get('total_messages', 0)}")
            
            # Hiển thị users online
            users = db.get_online_users()
            if users:
                print(f"\n👥 Users đang online:")
                for user in users:
                    print(f"  - {user['display_name']} ({user['username']})")
            
            # Hiển thị tin nhắn gần nhất
            messages = db.get_public_messages(5)
            if messages:
                print(f"\n💬 Tin nhắn gần nhất:")
                for msg in messages:
                    timestamp = msg['sent_at'].strftime("%H:%M:%S")
                    print(f"  [{timestamp}] {msg['display_name']}: {msg['content']}")
        else:
            print("❌ Không thể kết nối database!")
    elif choice == "0":
        print("👋 Tạm biệt!")
    else:
        print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()