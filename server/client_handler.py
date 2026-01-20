#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Handler - Xử lý kết nối từ từng client
Mỗi client sẽ có 1 thread riêng để xử lý
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

class ClientHandler:
    def __init__(self, client_socket, client_address, server):
        self.client_socket = client_socket
        self.address = client_address
        self.server = server
        self.username = None
        self.user_id = None
        self.is_authenticated = False
        self.is_running = True
        
        # Database connection
        self.db = ChatDatabase(os.path.join(database_path, 'chatbox.db'))
        
        print(f"👤 ClientHandler tạo cho {client_address}")
    
    def run(self):
        """Vòng lặp chính xử lý tin nhắn từ client"""
        try:
            while self.is_running:
                try:
                    # Nhận tin nhắn từ client - tăng buffer size cho file upload
                    message = self.client_socket.recv(1024 * 1024).decode('utf-8')  # 1MB buffer
                    
                    if not message:
                        break
                    
                    print(f"📨 Nhận từ {self.address}: {len(message)} bytes")
                    self.handle_message(message)
                    
                except socket.timeout:
                    continue
                except socket.error:
                    break
                except Exception as e:
                    print(f"❌ Lỗi xử lý tin nhắn từ {self.address}: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ Lỗi trong ClientHandler.run(): {e}")
        finally:
            self.disconnect()
    
    def handle_message(self, message):
        """Xử lý tin nhắn từ client theo protocol"""
        try:
            print(f"🔍 DEBUG: Raw message length: {len(message)}")
            print(f"🔍 DEBUG: Message start: {message[:100]}...")
            
            # Parse message: TYPE|SENDER|RECEIVER|CONTENT|TIMESTAMP
            parts = message.split('|', 4)
            if len(parts) < 4:
                print(f"❌ DEBUG: Invalid parts count: {len(parts)}")
                self.send_error("Invalid message format")
                return
            
            msg_type = parts[0]
            sender = parts[1]
            receiver = parts[2]
            content = parts[3]
            timestamp = parts[4] if len(parts) > 4 else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"🔍 DEBUG: Parsed - Type: {msg_type}, Sender: {sender}, Receiver: {receiver}")
            print(f"🔍 DEBUG: Content length: {len(content)}")
            
            # Xử lý theo loại tin nhắn
            if msg_type == "LOGIN":
                self.handle_login(sender, content)
            elif msg_type == "REGISTER":
                self.handle_register(sender, content)
            elif msg_type == "PUBLIC":
                self.handle_public_message(sender, content, timestamp)
            elif msg_type == "PRIVATE":
                self.handle_private_message(sender, receiver, content, timestamp)
            elif msg_type == "GET_USERS":
                self.handle_get_users_request(sender, timestamp)
            elif msg_type == "STATS":
                self.handle_stats_request(sender, timestamp)
            elif msg_type == "PING":
                self.send_message("PONG|SERVER|CLIENT|OK|" + timestamp)
            elif msg_type == "FILE_UPLOAD":
                self.handle_file_upload(sender, receiver, content, timestamp)
            elif msg_type == "FILE_DOWNLOAD":
                self.handle_file_download(sender, content, timestamp)
            elif msg_type == "FILE_LIST":
                self.handle_file_list_request(sender, timestamp)
            elif msg_type == "FILE_SHARE":
                self.handle_file_share(sender, receiver, content, timestamp)
            else:
                self.send_error(f"Unknown message type: {msg_type}")
                
        except Exception as e:
            print(f"❌ Lỗi handle_message: {e}")
            print(f"❌ Message causing error: {message[:200]}...")
            self.send_error("Server error processing message")
    
    def handle_login(self, username, password):
        """Xử lý đăng nhập"""
        try:
            user = self.db.login_user(username, password)
            
            if user:
                self.username = username
                self.user_id = user['id']
                self.is_authenticated = True
                
                # Gửi thông báo đăng nhập thành công
                login_response = f"LOGIN_OK|SERVER|{username}|Welcome {user['display_name']}!|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.send_message(login_response)
                
                # Delay một chút trước khi broadcast để client kịp setup listener
                import time
                time.sleep(0.2)  # Tăng delay lên 200ms
                
                # Thông báo user join và cập nhật user list
                self.server.broadcast_user_joined(username)
                
                # Gửi thêm một lần USERLIST riêng cho client mới login
                time.sleep(0.1)
                users = self.server.get_online_users()
                user_list_msg = f"USERLIST|SERVER|{username}|{','.join(users)}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.send_message(user_list_msg)
                print(f"📤 Gửi USERLIST riêng cho {username}: {users}")  # Debug
                
                print(f"✅ User {username} đã đăng nhập từ {self.address}")
                
            else:
                # Gửi thông báo đăng nhập thất bại
                login_response = f"LOGIN_FAIL|SERVER|{username}|Invalid username or password|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.send_message(login_response)
                
                print(f"❌ Đăng nhập thất bại cho {username} từ {self.address}")
                
        except Exception as e:
            print(f"❌ Lỗi handle_login: {e}")
            self.send_error("Login error")
    
    def handle_register(self, username, password):
        """Xử lý đăng ký"""
        try:
            # Tách password và display_name nếu có
            parts = password.split('|', 1)
            actual_password = parts[0]
            display_name = parts[1] if len(parts) > 1 else username
            
            success = self.db.register_user(username, actual_password, display_name)
            
            if success:
                register_response = f"REGISTER_OK|SERVER|{username}|Registration successful!|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.send_message(register_response)
                print(f"✅ User {username} đã đăng ký từ {self.address}")
            else:
                register_response = f"REGISTER_FAIL|SERVER|{username}|Username already exists!|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.send_message(register_response)
                print(f"❌ Đăng ký thất bại cho {username} từ {self.address}")
                
        except Exception as e:
            print(f"❌ Lỗi handle_register: {e}")
            self.send_error("Registration error")
    
    def handle_public_message(self, sender, content, timestamp):
        """Xử lý tin nhắn public"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            # Lưu tin nhắn vào database
            if self.user_id:
                self.db.send_public_message(self.user_id, content)
            
            # Broadcast tin nhắn đến tất cả client
            public_msg = f"PUBLIC|{sender}|ALL|{content}|{timestamp}"
            self.server.broadcast_message(public_msg, self)
            
            print(f"📢 Public message từ {sender}: {content}")
            
        except Exception as e:
            print(f"❌ Lỗi handle_public_message: {e}")
            self.send_error("Error sending public message")
    
    def handle_private_message(self, sender, receiver, content, timestamp):
        """Xử lý tin nhắn private"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            # Tìm receiver_id từ username
            receiver_user = None
            for client in self.server.clients:
                if client.username == receiver and client.is_authenticated:
                    receiver_user = client
                    break
            
            if receiver_user:
                # Lưu tin nhắn vào database
                if self.user_id and receiver_user.user_id:
                    self.db.send_private_message(self.user_id, receiver_user.user_id, content)
                
                # Gửi tin nhắn đến receiver
                private_msg = f"PRIVATE|{sender}|{receiver}|{content}|{timestamp}"
                success = self.server.send_private_message(private_msg, receiver, self)
                
                if success:
                    # Gửi confirmation cho sender
                    confirm_msg = f"PRIVATE_SENT|SERVER|{sender}|Message sent to {receiver}|{timestamp}"
                    self.send_message(confirm_msg)
                    print(f"🔒 Private message từ {sender} đến {receiver}: {content}")
                else:
                    self.send_error(f"User {receiver} not found or offline")
            else:
                self.send_error(f"User {receiver} not found or offline")
                
        except Exception as e:
            print(f"❌ Lỗi handle_private_message: {e}")
            self.send_error("Error sending private message")
    
    def handle_get_users_request(self, sender, timestamp):
        """Xử lý yêu cầu lấy danh sách user online"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            # Lấy danh sách user online
            users = self.server.get_online_users()
            user_list_msg = f"USERLIST|SERVER|{sender}|{','.join(users)}|{timestamp}"
            self.send_message(user_list_msg)
            
            print(f"📤 Gửi USERLIST cho {sender}: {users}")
            
        except Exception as e:
            print(f"❌ Lỗi handle_get_users_request: {e}")
            self.send_error("Error getting user list")
    
    def handle_stats_request(self, sender, timestamp):
        """Xử lý yêu cầu thống kê server"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            stats = self.server.get_stats()
            db_stats = self.db.get_stats()
            
            stats_info = f"{stats['total_clients']},{stats['authenticated_clients']},{db_stats.get('total_messages', 0)},{db_stats.get('total_users', 0)}"
            stats_msg = f"STATS|SERVER|{sender}|{stats_info}|{timestamp}"
            self.send_message(stats_msg)
            
            print(f"📊 Gửi thống kê cho {sender}")
            
        except Exception as e:
            print(f"❌ Lỗi handle_stats_request: {e}")
            self.send_error("Error getting stats")
    
    def handle_file_upload(self, sender, receiver, content, timestamp):
        """Xử lý upload file"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            # Parse file data: filename#filesize#base64_data (sử dụng # thay vì |)
            parts = content.split('#', 2)
            if len(parts) != 3:
                print(f"❌ DEBUG: Invalid file format. Parts: {len(parts)}")
                print(f"❌ DEBUG: Content preview: {content[:200]}...")
                self.send_error("Invalid file format")
                return
            
            filename, filesize, file_data = parts
            
            print(f"🔍 DEBUG: Parsed file - Name: {filename}, Size: {filesize}")
            print(f"🔍 DEBUG: Base64 data length: {len(file_data)}")
            
            # Tạo thư mục files nếu chưa có
            import os
            files_dir = os.path.join(os.path.dirname(__file__), '..', 'files')
            os.makedirs(files_dir, exist_ok=True)
            
            # Decode và lưu file
            import base64
            file_path = os.path.join(files_dir, f"{self.username}_{filename}")
            
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(file_data))
            
            print(f"✅ DEBUG: File saved to: {file_path}")
            
            # Thông báo upload thành công
            success_msg = f"FILE_UPLOAD_OK|SERVER|{sender}|{filename} uploaded successfully|{timestamp}"
            self.send_message(success_msg)
            
            # Broadcast thông báo có file mới
            if receiver == "ALL":
                broadcast_msg = f"FILE_SHARED|{sender}|ALL|{sender} shared file: {filename}|{timestamp}"
                self.server.broadcast_message(broadcast_msg, self)
            else:
                # Gửi private file notification
                private_msg = f"FILE_SHARED|{sender}|{receiver}|{sender} sent you a file: {filename}|{timestamp}"
                self.server.send_private_message(private_msg, receiver, self)
            
            print(f"📁 File uploaded: {filename} by {sender}")
            
        except Exception as e:
            print(f"❌ Lỗi handle_file_upload: {e}")
            import traceback
            traceback.print_exc()
            self.send_error("Error uploading file")
    
    def handle_file_download(self, sender, filename, timestamp):
        """Xử lý download file"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            import os
            import base64
            
            files_dir = os.path.join(os.path.dirname(__file__), '..', 'files')
            file_path = os.path.join(files_dir, filename)
            
            if not os.path.exists(file_path):
                self.send_error(f"File {filename} not found")
                return
            
            # Đọc và encode file
            with open(file_path, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')
            
            file_size = os.path.getsize(file_path)
            
            # Gửi file data về client - Format: TYPE|SENDER|RECEIVER|CONTENT|TIMESTAMP
            # Content sẽ là: filename#filesize#base64_data (sử dụng # thay vì |)
            file_content = f"{filename}#{file_size}#{file_data}"
            download_msg = f"FILE_DOWNLOAD_OK|SERVER|{sender}|{file_content}|{timestamp}"
            self.send_message(download_msg)
            
            print(f"📥 File downloaded: {filename} by {sender}")
            
        except Exception as e:
            print(f"❌ Lỗi handle_file_download: {e}")
            self.send_error("Error downloading file")
    
    def handle_file_list_request(self, sender, timestamp):
        """Xử lý yêu cầu danh sách file"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            import os
            
            files_dir = os.path.join(os.path.dirname(__file__), '..', 'files')
            
            if not os.path.exists(files_dir):
                file_list = ""
            else:
                files = []
                for filename in os.listdir(files_dir):
                    file_path = os.path.join(files_dir, filename)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        # Format: filename:size:uploader
                        if '_' in filename:
                            uploader, original_name = filename.split('_', 1)
                            files.append(f"{original_name}:{file_size}:{uploader}")
                        else:
                            files.append(f"{filename}:{file_size}:unknown")
                
                file_list = ",".join(files)
            
            # Gửi danh sách file
            list_msg = f"FILE_LIST_OK|SERVER|{sender}|{file_list}|{timestamp}"
            self.send_message(list_msg)
            
            print(f"📋 File list sent to {sender}: {len(files) if 'files' in locals() else 0} files")
            
        except Exception as e:
            print(f"❌ Lỗi handle_file_list_request: {e}")
            self.send_error("Error getting file list")
    
    def handle_file_share(self, sender, receiver, content, timestamp):
        """Xử lý chia sẻ file với hỗ trợ text và binary"""
        if not self.is_authenticated:
            self.send_error("Not authenticated")
            return
        
        try:
            # Parse content: filename:type:file_content
            parts = content.split(':', 2)
            if len(parts) != 3:
                self.send_error("Invalid file share format")
                return
            
            filename, file_type, file_content = parts
            
            print(f"🔍 DEBUG: File share - Name: {filename}, Type: {file_type}, Content length: {len(file_content)}")
            
            # Lưu file vào thư mục files
            import os
            import base64
            files_dir = os.path.join(os.path.dirname(__file__), '..', 'files')
            os.makedirs(files_dir, exist_ok=True)
            
            file_path = os.path.join(files_dir, f"{self.username}_{filename}")
            
            if file_type == "text":
                # Lưu file text
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
            elif file_type == "binary":
                # Decode Base64 và lưu file binary
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(file_content))
            else:
                self.send_error(f"Unsupported file type: {file_type}")
                return
            
            print(f"✅ DEBUG: File saved to: {file_path}")
            
            # Thông báo thành công
            success_msg = f"FILE_SHARE_OK|SERVER|{sender}|File {filename} uploaded successfully|{timestamp}"
            self.send_message(success_msg)
            
            # Broadcast thông báo có file mới
            if receiver == "ALL":
                broadcast_msg = f"FILE_SHARED|{sender}|ALL|{sender} shared file: {filename}|{timestamp}"
                self.server.broadcast_message(broadcast_msg, self)
            else:
                # Gửi private file notification
                private_msg = f"FILE_SHARED|{sender}|{receiver}|{sender} sent you a file: {filename}|{timestamp}"
                self.server.send_private_message(private_msg, receiver, self)
            
            print(f"📁 File shared: {filename} ({file_type}) by {sender}")
            
        except Exception as e:
            print(f"❌ Lỗi handle_file_share: {e}")
            import traceback
            traceback.print_exc()
            self.send_error("Error sharing file")
    
    def send_message(self, message):
        """Gửi tin nhắn đến client"""
        try:
            self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"❌ Lỗi gửi tin nhắn đến {self.address}: {e}")
            raise
    
    def send_error(self, error_message):
        """Gửi thông báo lỗi đến client"""
        try:
            error_msg = f"ERROR|SERVER|CLIENT|{error_message}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.send_message(error_msg)
        except:
            pass
    
    def disconnect(self):
        """Ngắt kết nối client"""
        try:
            self.is_running = False
            
            # Đăng xuất user nếu đã đăng nhập
            if self.is_authenticated and self.username:
                if self.user_id:
                    self.db.logout_user(self.user_id)
                self.server.broadcast_user_left(self.username)
                print(f"👋 User {self.username} đã đăng xuất")
            
            # Đóng socket
            if self.client_socket:
                self.client_socket.close()
            
            # Xóa khỏi danh sách client
            self.server.remove_client(self)
            
            print(f"🔌 Đã ngắt kết nối {self.address}")
            
        except Exception as e:
            print(f"❌ Lỗi disconnect: {e}")

def test_client_handler():
    """Test function cho ClientHandler"""
    print("🧪 Test ClientHandler")
    # Có thể thêm unit tests ở đây
    pass

if __name__ == "__main__":
    test_client_handler()