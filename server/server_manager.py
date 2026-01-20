#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server Manager - Quản lý và monitor Chat Server
Cung cấp giao diện để quản lý server
"""

import threading
import time
import sys
import os
from datetime import datetime

# Import server
from server import ChatServer

class ServerManager:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.is_monitoring = False
        
    def start_server(self, host='localhost', port=5000):
        """Khởi động server trong thread riêng"""
        if self.server and self.server.is_running:
            print("❌ Server đã đang chạy!")
            return False
        
        try:
            self.server = ChatServer(host, port)
            self.server_thread = threading.Thread(target=self.server.start)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            # Đợi server khởi động
            time.sleep(1)
            
            if self.server.is_running:
                print("✅ Server đã khởi động thành công!")
                return True
            else:
                print("❌ Không thể khởi động server!")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khởi động server: {e}")
            return False
    
    def stop_server(self):
        """Dừng server"""
        if not self.server or not self.server.is_running:
            print("❌ Server không đang chạy!")
            return False
        
        try:
            self.server.stop()
            print("✅ Server đã dừng!")
            return True
        except Exception as e:
            print(f"❌ Lỗi dừng server: {e}")
            return False
    
    def get_server_status(self):
        """Lấy trạng thái server"""
        if not self.server:
            return {
                'status': 'Not initialized',
                'running': False,
                'clients': 0,
                'authenticated': 0,
                'online_users': []
            }
        
        stats = self.server.get_stats()
        return {
            'status': 'Running' if self.server.is_running else 'Stopped',
            'running': self.server.is_running,
            'host': self.server.host,
            'port': self.server.port,
            'clients': stats['total_clients'],
            'authenticated': stats['authenticated_clients'],
            'online_users': stats['online_users']
        }
    
    def monitor_server(self, interval=5):
        """Monitor server theo thời gian thực"""
        self.is_monitoring = True
        print(f"📊 Bắt đầu monitor server (cập nhật mỗi {interval}s)")
        print("Nhấn Ctrl+C để dừng monitor\n")
        
        try:
            while self.is_monitoring:
                status = self.get_server_status()
                
                # Clear screen (Windows/Linux compatible)
                os.system('cls' if os.name == 'nt' else 'clear')
                
                print("🖥️  CHAT SERVER MONITOR")
                print("=" * 50)
                print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"🔄 Trạng thái: {status['status']}")
                
                if status['running']:
                    print(f"🌐 Địa chỉ: {status['host']}:{status['port']}")
                    print(f"👥 Tổng clients: {status['clients']}")
                    print(f"✅ Đã xác thực: {status['authenticated']}")
                    print(f"🟢 Users online: {len(status['online_users'])}")
                    
                    if status['online_users']:
                        print("📋 Danh sách online:")
                        for user in status['online_users']:
                            print(f"  - {user}")
                    else:
                        print("📋 Không có user nào online")
                else:
                    print("❌ Server không chạy")
                
                print("\n" + "=" * 50)
                print("Nhấn Ctrl+C để dừng monitor")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.is_monitoring = False
            print("\n📊 Dừng monitor")
    
    def send_server_message(self, message):
        """Gửi tin nhắn từ server đến tất cả client"""
        if not self.server or not self.server.is_running:
            print("❌ Server không chạy!")
            return False
        
        try:
            server_msg = f"SYSTEM|SERVER|ALL|{message}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.server.broadcast_message(server_msg)
            print(f"📢 Đã gửi tin nhắn server: {message}")
            return True
        except Exception as e:
            print(f"❌ Lỗi gửi tin nhắn: {e}")
            return False
    
    def kick_user(self, username):
        """Kick user khỏi server"""
        if not self.server or not self.server.is_running:
            print("❌ Server không chạy!")
            return False
        
        try:
            for client in self.server.clients:
                if client.username == username and client.is_authenticated:
                    client.send_message(f"KICK|SERVER|{username}|You have been kicked from server|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    client.disconnect()
                    print(f"👢 Đã kick user: {username}")
                    return True
            
            print(f"❌ Không tìm thấy user: {username}")
            return False
            
        except Exception as e:
            print(f"❌ Lỗi kick user: {e}")
            return False

def interactive_menu():
    """Menu tương tác cho Server Manager"""
    manager = ServerManager()
    
    while True:
        print("\n🖥️  CHAT SERVER MANAGER")
        print("=" * 30)
        print("1. Khởi động server")
        print("2. Dừng server")
        print("3. Xem trạng thái server")
        print("4. Monitor server real-time")
        print("5. Gửi tin nhắn server")
        print("6. Kick user")
        print("7. Xem danh sách online")
        print("0. Thoát")
        
        choice = input("\nChọn chức năng (0-7): ").strip()
        
        try:
            if choice == "1":
                host = input("Nhập IP (Enter = localhost): ").strip() or 'localhost'
                port_input = input("Nhập port (Enter = 5000): ").strip()
                port = int(port_input) if port_input.isdigit() else 5000
                manager.start_server(host, port)
                
            elif choice == "2":
                manager.stop_server()
                
            elif choice == "3":
                status = manager.get_server_status()
                print("\n📊 TRẠNG THÁI SERVER:")
                print(f"  - Status: {status['status']}")
                if status['running']:
                    print(f"  - Address: {status['host']}:{status['port']}")
                    print(f"  - Clients: {status['clients']}")
                    print(f"  - Authenticated: {status['authenticated']}")
                    print(f"  - Online users: {', '.join(status['online_users']) if status['online_users'] else 'None'}")
                
            elif choice == "4":
                if manager.server and manager.server.is_running:
                    interval = input("Interval (giây, Enter = 5): ").strip()
                    interval = int(interval) if interval.isdigit() else 5
                    manager.monitor_server(interval)
                else:
                    print("❌ Server chưa chạy!")
                
            elif choice == "5":
                if manager.server and manager.server.is_running:
                    message = input("Nhập tin nhắn server: ").strip()
                    if message:
                        manager.send_server_message(message)
                else:
                    print("❌ Server chưa chạy!")
                
            elif choice == "6":
                if manager.server and manager.server.is_running:
                    username = input("Nhập username cần kick: ").strip()
                    if username:
                        manager.kick_user(username)
                else:
                    print("❌ Server chưa chạy!")
                
            elif choice == "7":
                status = manager.get_server_status()
                if status['online_users']:
                    print(f"\n👥 Users online ({len(status['online_users'])}):")
                    for i, user in enumerate(status['online_users'], 1):
                        print(f"  {i}. {user}")
                else:
                    print("\n👥 Không có user nào online")
                
            elif choice == "0":
                if manager.server and manager.server.is_running:
                    confirm = input("Server đang chạy. Bạn có muốn dừng? (y/n): ").lower()
                    if confirm == 'y':
                        manager.stop_server()
                        print("👋 Tạm biệt!")
                        break
                else:
                    print("👋 Tạm biệt!")
                    break
                    
            else:
                print("❌ Lựa chọn không hợp lệ!")
                
        except KeyboardInterrupt:
            print("\n⚠️  Nhận tín hiệu dừng")
            if manager.server and manager.server.is_running:
                manager.stop_server()
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        if choice not in ["4"]:  # Không pause sau monitor
            input("\nNhấn Enter để tiếp tục...")

def main():
    """Hàm main"""
    print("🚀 CHAT BOX SERVER MANAGER")
    print("Quản lý và monitor Chat Server")
    print("=" * 40)
    
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()