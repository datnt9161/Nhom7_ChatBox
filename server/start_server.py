#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start ChatBox Server - Khởi động server đơn giản
"""

from server import ChatServer

def main():
    """Khởi động server với cài đặt mặc định"""
    print("🚀 Khởi động ChatBox Server...")
    print("=" * 40)
    
    # Tạo và khởi động server
    server = ChatServer(host='localhost', port=5000)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng server...")
        server.stop()
        print("👋 Server đã dừng!")
    except Exception as e:
        print(f"❌ Lỗi server: {str(e)}")

if __name__ == "__main__":
    main()