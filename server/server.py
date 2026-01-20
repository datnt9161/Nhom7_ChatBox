#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat Box Server - Main Server Application
Xử lý kết nối từ nhiều client đồng thời
"""

import socket
import threading
import sys
import os
from datetime import datetime

# Thêm thư mục Database vào path để import
database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database'))
if database_path not in sys.path:
    sys.path.insert(0, database_path)

from database import ChatDatabase

from client_handler import ClientHandler

class ChatServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []  # Danh sách ClientHandler
        self.is_running = False
        self.db = ChatDatabase(os.path.join(database_path, 'chatbox.db'))
        
        print(f"🚀 Chat Server khởi tạo tại {host}:{port}")
    
    def start(self):
        """Khởi động server"""
        try:
            # Tạo server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)  # Tối đa 10 kết nối chờ
            
            self.is_running = True
            print(f"✅ Server đang lắng nghe tại {self.host}:{self.port}")
            print("📡 Đang chờ client kết nối...")
            
            # Vòng lặp chính - chấp nhận kết nối
            while self.is_running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"🔗 Client mới kết nối từ {client_address}")
                    
                    # Tạo ClientHandler cho client mới
                    client_handler = ClientHandler(client_socket, client_address, self)
                    self.clients.append(client_handler)
                    
                    # Khởi động thread xử lý client
                    client_thread = threading.Thread(target=client_handler.run)
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.is_running:
                        print(f"❌ Lỗi accept connection: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ Lỗi khởi động server: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Dừng server"""
        print("\n🛑 Đang dừng server...")
        self.is_running = False
        
        # Đóng tất cả client connections
        for client in self.clients[:]:
            client.disconnect()
        
        # Đóng server socket
        if self.server_socket:
            self.server_socket.close()
        
        print("✅ Server đã dừng")
    
    def remove_client(self, client_handler):
        """Xóa client khỏi danh sách"""
        if client_handler in self.clients:
            self.clients.remove(client_handler)
            print(f"📤 Đã xóa client {client_handler.address}")
    
    def broadcast_message(self, message, sender_client=None):
        """Gửi tin nhắn đến tất cả client (trừ sender)"""
        disconnected_clients = []
        
        for client in self.clients:
            if client != sender_client and client.is_authenticated:
                try:
                    client.send_message(message)
                except:
                    disconnected_clients.append(client)
        
        # Xóa các client đã disconnect
        for client in disconnected_clients:
            self.remove_client(client)
    
    def send_private_message(self, message, target_username, sender_client):
        """Gửi tin nhắn private đến user cụ thể"""
        for client in self.clients:
            if client.username == target_username and client.is_authenticated:
                try:
                    client.send_message(message)
                    return True
                except:
                    self.remove_client(client)
                    return False
        return False
    
    def get_online_users(self):
        """Lấy danh sách user đang online"""
        online_users = []
        for client in self.clients:
            if client.is_authenticated and client.username:
                online_users.append(client.username)
        return online_users
    
    def broadcast_user_list(self):
        """Gửi danh sách user online đến tất cả client"""
        users = self.get_online_users()
        user_list_msg = f"USERLIST|SERVER|ALL|{','.join(users)}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.broadcast_message(user_list_msg)
    
    def broadcast_user_joined(self, username):
        """Thông báo user mới join"""
        join_msg = f"JOIN|{username}|ALL|đã tham gia chat|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.broadcast_message(join_msg)
        self.broadcast_user_list()
    
    def broadcast_user_left(self, username):
        """Thông báo user rời khỏi chat"""
        leave_msg = f"LEAVE|{username}|ALL|đã rời khỏi chat|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.broadcast_message(leave_msg)
        self.broadcast_user_list()
    
    def send_notification(self, message, target_user=None):
        """Gửi notification đến user hoặc tất cả users"""
        notification_msg = f"NOTIFICATION|SERVER|{'ALL' if not target_user else target_user}|{message}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        if target_user:
            self.send_private_message(notification_msg, target_user, None)
        else:
            self.broadcast_message(notification_msg)
    
    def get_stats(self):
        """Lấy thống kê server"""
        return {
            'total_clients': len(self.clients),
            'authenticated_clients': len([c for c in self.clients if c.is_authenticated]),
            'online_users': self.get_online_users(),
            'server_running': self.is_running
        }

def main():
    """Hàm main"""
    print("🌐 CHAT BOX SERVER")
    print("=" * 30)
    
    # Cấu hình server
    host = input("Nhập IP server (Enter = localhost): ").strip() or 'localhost'
    port_input = input("Nhập port (Enter = 5000): ").strip()
    port = int(port_input) if port_input.isdigit() else 5000
    
    # Tạo và khởi động server
    server = ChatServer(host, port)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n⚠️  Nhận tín hiệu dừng từ người dùng")
    except Exception as e:
        print(f"❌ Lỗi server: {e}")
    finally:
        server.stop()

if __name__ == "__main__":
    main()