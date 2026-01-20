#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Handler - Xử lý gửi/nhận file trong Chat Box
"""

import os
import base64
import hashlib
from datetime import datetime

class FileHandler:
    def __init__(self, upload_dir="uploads"):
        self.upload_dir = upload_dir
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {'.txt', '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.zip'}
        
        # Tạo thư mục upload nếu chưa có
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
    
    def is_allowed_file(self, filename):
        """Kiểm tra file có được phép upload không"""
        if not filename:
            return False
        
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions
    
    def get_file_hash(self, file_data):
        """Tạo hash cho file để kiểm tra tính toàn vẹn"""
        return hashlib.md5(file_data).hexdigest()
    
    def save_file(self, filename, file_data, sender_username):
        """Lưu file vào server"""
        try:
            if not self.is_allowed_file(filename):
                return False, "File type not allowed"
            
            if len(file_data) > self.max_file_size:
                return False, f"File too large (max {self.max_file_size // (1024*1024)}MB)"
            
            # Tạo tên file unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{sender_username}_{timestamp}_{filename}"
            file_path = os.path.join(self.upload_dir, safe_filename)
            
            # Lưu file
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            # Tạo file info
            file_info = {
                'original_name': filename,
                'saved_name': safe_filename,
                'file_path': file_path,
                'size': len(file_data),
                'hash': self.get_file_hash(file_data),
                'sender': sender_username,
                'uploaded_at': datetime.now().isoformat()
            }
            
            return True, file_info
            
        except Exception as e:
            return False, f"Error saving file: {str(e)}"
    
    def get_file(self, file_path):
        """Lấy file từ server"""
        try:
            if not os.path.exists(file_path):
                return False, "File not found"
            
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            return True, file_data
            
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    def delete_file(self, file_path):
        """Xóa file khỏi server"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True, "File deleted"
            else:
                return False, "File not found"
                
        except Exception as e:
            return False, f"Error deleting file: {str(e)}"
    
    def encode_file_for_transfer(self, file_data):
        """Encode file data để gửi qua socket"""
        return base64.b64encode(file_data).decode('utf-8')
    
    def decode_file_from_transfer(self, encoded_data):
        """Decode file data nhận từ socket"""
        try:
            return base64.b64decode(encoded_data.encode('utf-8'))
        except Exception as e:
            raise ValueError(f"Invalid file data: {str(e)}")
    
    def get_file_info(self, file_path):
        """Lấy thông tin file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'path': file_path
            }
            
        except Exception as e:
            return None
    
    def list_files(self, username=None):
        """Liệt kê files đã upload"""
        try:
            files = []
            for filename in os.listdir(self.upload_dir):
                if username and not filename.startswith(f"{username}_"):
                    continue
                
                file_path = os.path.join(self.upload_dir, filename)
                file_info = self.get_file_info(file_path)
                if file_info:
                    files.append(file_info)
            
            return files
            
        except Exception as e:
            return []

def test_file_handler():
    """Test FileHandler"""
    print("🧪 Test FileHandler")
    
    handler = FileHandler("test_uploads")
    
    # Test 1: Save file
    test_data = b"Hello, this is test file content!"
    success, result = handler.save_file("test.txt", test_data, "testuser")
    
    if success:
        print("✅ Save file thành công")
        print(f"   File info: {result}")
        
        # Test 2: Get file
        success2, file_data = handler.get_file(result['file_path'])
        if success2 and file_data == test_data:
            print("✅ Get file thành công")
        else:
            print("❌ Get file thất bại")
        
        # Test 3: Delete file
        success3, msg = handler.delete_file(result['file_path'])
        if success3:
            print("✅ Delete file thành công")
        else:
            print("❌ Delete file thất bại")
    else:
        print(f"❌ Save file thất bại: {result}")
    
    # Cleanup
    try:
        os.rmdir("test_uploads")
    except:
        pass

if __name__ == "__main__":
    test_file_handler()