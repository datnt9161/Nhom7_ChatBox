# Chat Box - Java Application

Ứng dụng chat real-time hỗ trợ nhiều phòng chat (rooms) được implement hoàn toàn bằng **Java với Spring Boot**.

## ✅ Features

- ✅ **100% Java** - Backend và frontend đều serve từ Java
- ✅ Real-time messaging qua WebSocket (STOMP)
- ✅ Multi-room support
- ✅ Web client interface
- ✅ Spring Boot - Framework Java hiện đại
- ✅ Built-in web server - Không cần Apache hay PHP

## 📋 Requirements

- **Java 17** hoặc cao hơn
- **Maven 3.6+**

## 🚀 Quick Start

### Cách 1: Dùng script (Dễ nhất)

```cmd
cd chat-app-java
run.bat
```

### Cách 2: Chạy thủ công

```cmd
cd chat-app-java
mvn clean package
java -jar target/chat-app-1.0.0.jar
```

### Cách 3: Chạy với Maven

```cmd
cd chat-app-java
mvn spring-boot:run
```

## 🌐 Sử dụng

1. Chạy server (một trong các cách trên)
2. Mở browser: `http://localhost:8080`
3. Nhập username và room name
4. Bắt đầu chat!

## 📁 Cấu trúc Project

```
multiroom-chat/
├── chat-app-java/              # Ứng dụng Java chính (Spring Boot)
│   ├── pom.xml                 # Maven config
│   ├── run.bat                 # Script chạy
│   ├── README.md               # Hướng dẫn chi tiết
│   └── src/main/
│       ├── java/               # Java source code
│       └── resources/
│           ├── application.properties
│           └── static/         # Frontend (HTML/CSS/JS)
├── README.md                   # File này
└── docs/                       # Tài liệu
```

## 🔧 Configuration

File `chat-app-java/src/main/resources/application.properties`:
- `server.port=8080` - Port server (có thể thay đổi)

## ✅ Ưu điểm

- ✅ **Không cần PHP** - Tất cả đều Java
- ✅ **Không cần Apache** - Spring Boot có built-in server
- ✅ **Chỉ 1 server** - Không cần chạy nhiều server
- ✅ **Dễ deploy** - Chỉ cần 1 file JAR
- ✅ **Hiệu suất tốt** - Java performance

## 📝 Lưu ý

- Client vẫn dùng HTML/JavaScript (vì browser chỉ hiểu HTML/JS)
- Nhưng tất cả được serve từ Java server
- Không cần PHP hay Apache nữa!

## 📚 Documentation

- Chi tiết: Xem `chat-app-java/README.md`
- Architecture: Xem `docs/architecture.md`
- Protocol: Xem `docs/protocol.md`

## 🎯 Development

### Build JAR file

```cmd
cd chat-app-java
mvn clean package
```

File JAR sẽ được tạo tại: `target/chat-app-1.0.0.jar`

### Run tests

```cmd
cd chat-app-java
mvn test
```

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Java 17+ đã được cài đặt
2. Maven đã được cài đặt
3. Port 8080 không bị chiếm bởi ứng dụng khác

---

**Chúc bạn sử dụng vui vẻ!** 🎉
