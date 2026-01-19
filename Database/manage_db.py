#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager - Quản lý database SQLite đơn giản
"""

from database import ChatDatabase
from datetime import datetime
import os

def view_users():
    """Xem danh sách users"""
    db = ChatDatabase()
    users = db.get_all_users()
    
    print("👥 DANH SÁCH USERS")
    print("=" * 60)
    print(f"{'ID':<4} {'Username':<15} {'Display Name':<20} {'Status':<10} {'Email'}")
    print("-" * 60)
    
    for user in users:
        status_icon = "🟢" if user['status'] == 'online' else "⚫"
        print(f"{user['id']:<4} {user['username']:<15} {user['display_name']:<20} "
              f"{status_icon}{user['status']:<9} {user['email'] or 'N/A'}")
    
    print(f"\nTổng: {len(users)} users")

def view_messages():
    """Xem tin nhắn gần nhất"""
    db = ChatDatabase()
    
    limit = input("Số tin nhắn muốn xem (mặc định 20): ").strip()
    limit = int(limit) if limit.isdigit() else 20
    
    messages = db.get_public_messages(limit)
    
    print(f"\n💬 TIN NHẮN PUBLIC ({limit} gần nhất)")
    print("=" * 60)
    
    for msg in messages:
        timestamp = datetime.fromisoformat(msg['sent_at']).strftime("%d/%m %H:%M:%S")
        print(f"[{timestamp}] {msg['display_name']}: {msg['content']}")
    
    print(f"\nTổng: {len(messages)} tin nhắn")

def create_user():
    """Tạo user mới"""
    db = ChatDatabase()
    
    print("📝 TẠO USER MỚI")
    print("=" * 30)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username không được để trống!")
        return
    
    password = input("Password: ").strip()
    if not password:
        print("❌ Password không được để trống!")
        return
    
    display_name = input("Tên hiển thị: ").strip()
    if not display_name:
        display_name = username
    
    email = input("Email (tùy chọn): ").strip()
    if not email:
        email = None
    
    if db.register_user(username, password, display_name, email):
        print("✅ Tạo user thành công!")
    else:
        print("❌ Tạo user thất bại!")

def test_login():
    """Test đăng nhập"""
    db = ChatDatabase()
    
    print("🔐 TEST ĐĂNG NHẬP")
    print("=" * 30)
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    user = db.login_user(username, password)
    if user:
        print(f"✅ Đăng nhập thành công!")
        print(f"  - ID: {user['id']}")
        print(f"  - Username: {user['username']}")
        print(f"  - Tên hiển thị: {user['display_name']}")
        print(f"  - Email: {user['email'] or 'N/A'}")
        
        # Test gửi tin nhắn
        test_msg = input("\nNhập tin nhắn test (Enter để bỏ qua): ").strip()
        if test_msg:
            if db.send_public_message(user['id'], test_msg):
                print("✅ Gửi tin nhắn thành công!")
            else:
                print("❌ Gửi tin nhắn thất bại!")
        
        # Đăng xuất
        db.logout_user(user['id'])
        print("👋 Đã đăng xuất")
    else:
        print("❌ Đăng nhập thất bại!")

def show_stats():
    """Hiển thị thống kê"""
    db = ChatDatabase()
    stats = db.get_stats()
    
    print("📊 THỐNG KÊ DATABASE")
    print("=" * 30)
    print(f"📁 File database: {db.db_path}")
    print(f"👥 Tổng users: {stats['total_users']}")
    print(f"🟢 Users online: {stats['online_users']}")
    print(f"💬 Tổng tin nhắn: {stats['total_messages']}")
    print(f"📢 Tin nhắn public: {stats['public_messages']}")
    print(f"🔒 Tin nhắn private: {stats['private_messages']}")
    
    # Hiển thị kích thước file
    if os.path.exists(db.db_path):
        size = os.path.getsize(db.db_path)
        size_mb = size / (1024 * 1024)
        print(f"💾 Kích thước file: {size_mb:.2f} MB")

def reset_database():
    """Reset database"""
    db = ChatDatabase()
    
    confirm = input("⚠️  Bạn có chắc muốn xóa tất cả dữ liệu? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if os.path.exists(db.db_path):
            os.remove(db.db_path)
            print("🗑️  Đã xóa database cũ")
        
        # Tạo lại database mới
        new_db = ChatDatabase()
        new_db.create_sample_data()
        print("✅ Đã tạo lại database với dữ liệu mẫu")
    else:
        print("❌ Hủy bỏ reset database")

def backup_database():
    """Backup database"""
    db = ChatDatabase()
    
    if not os.path.exists(db.db_path):
        print("❌ Database không tồn tại!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"chatbox_backup_{timestamp}.db"
    
    try:
        import shutil
        shutil.copy2(db.db_path, backup_name)
        print(f"✅ Backup thành công: {backup_name}")
    except Exception as e:
        print(f"❌ Lỗi backup: {e}")

def interactive_chat():
    """Chat tương tác đơn giản"""
    db = ChatDatabase()
    
    print("💬 CHAT TƯƠNG TÁC")
    print("=" * 30)
    
    # Đăng nhập
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    user = db.login_user(username, password)
    if not user:
        print("❌ Đăng nhập thất bại!")
        return
    
    print(f"✅ Chào {user['display_name']}!")
    print("Gõ tin nhắn và nhấn Enter. Gõ 'quit' để thoát.\n")
    
    try:
        while True:
            # Hiển thị tin nhắn mới
            messages = db.get_public_messages(3)
            for msg in messages[-2:]:  # Hiển thị 2 tin gần nhất
                if msg['username'] != username:  # Không hiển thị tin của chính mình
                    timestamp = datetime.fromisoformat(msg['sent_at']).strftime("%H:%M")
                    print(f"[{timestamp}] {msg['display_name']}: {msg['content']}")
            
            # Nhập tin nhắn
            message = input(f"{user['display_name']}: ").strip()
            
            if message.lower() == 'quit':
                break
            
            if message:
                if db.send_public_message(user['id'], message):
                    print("✅ Đã gửi")
                else:
                    print("❌ Gửi thất bại")
            
    except KeyboardInterrupt:
        pass
    
    # Đăng xuất
    db.logout_user(user['id'])
    print(f"\n👋 Tạm biệt {user['display_name']}!")

def main():
    """Menu chính"""
    while True:
        print("\n🗄️  CHAT BOX DATABASE MANAGER")
        print("=" * 40)
        print("1. Xem danh sách users")
        print("2. Xem tin nhắn gần nhất")
        print("3. Tạo user mới")
        print("4. Test đăng nhập")
        print("5. Xem thống kê")
        print("6. Chat tương tác")
        print("7. Backup database")
        print("8. Reset database")
        print("9. Tạo dữ liệu mẫu")
        print("0. Thoát")
        
        choice = input("\nChọn chức năng (0-9): ").strip()
        
        try:
            if choice == "1":
                view_users()
            elif choice == "2":
                view_messages()
            elif choice == "3":
                create_user()
            elif choice == "4":
                test_login()
            elif choice == "5":
                show_stats()
            elif choice == "6":
                interactive_chat()
            elif choice == "7":
                backup_database()
            elif choice == "8":
                reset_database()
            elif choice == "9":
                db = ChatDatabase()
                db.create_sample_data()
            elif choice == "0":
                print("👋 Tạm biệt!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()