# IoT Device Management API

使用 **Python + FastAPI + MySQL** 建立的 IoT 設備基本資料管理 API。  
這是一個小型示範專案，目標是完成一個結構清楚、可測試、可擴充的設備資料管理後端服務。

---

## 專案簡介

本專案提供一組 RESTful API，用於管理 IoT 設備的基本資料，例如：

- 設備編號
- 設備名稱
- 設備類型
- 安裝位置
- 設備狀態
- IP 位址
- 建立時間
- 更新時間

並支援：

- CRUD 操作
- 條件查詢
- 分頁查詢
- 關鍵字搜尋
- GROUP BY 統計
- HAVING COUNT 過濾
- Swagger API 文件

---

## 功能

- [x] 新增設備
- [x] 查詢設備列表
- [x] 查詢單一設備
- [x] 更新設備
- [x] 刪除設備
- [x] 依設備狀態查詢
- [x] 依設備位置查詢
- [x] 依設備類型查詢
- [x] 關鍵字搜尋
- [x] 分頁查詢
- [x] 設備統計 API
- [x] Swagger UI
- [x] 基本錯誤處理

---

## 技術

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- MySQL 8.x
- PyMySQL
- Uvicorn

---

## 系統架構

```text
Client / Swagger UI
        ↓
FastAPI Router
        ↓
Device Service
        ↓
Device Repository
        ↓
SQLAlchemy / MySQL
        ↓
devices table
```

本專案採用簡單分層架構：

- `Router`：處理 HTTP 請求與回應。
- `Service`：處理商業邏輯與資料驗證。
- `Repository`：處理資料庫存取。
- `Model`：對應資料庫資料表。
- `Schema`：定義 API 輸入與輸出格式。

---

## 資料表設計

資料表名稱：

```text
devices
```

SQL 建立語法：

```sql
CREATE TABLE IF NOT EXISTS devices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_code VARCHAR(50) NOT NULL UNIQUE,
    device_name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50),
    location VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'offline',
    ip_address VARCHAR(45),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_devices_status ON devices(status);
CREATE INDEX idx_devices_location ON devices(location);
CREATE INDEX idx_devices_device_type ON devices(device_type);
```

欄位說明：

| 欄位 | 型別 | 說明 |
|---|---|---|
| id | INT | 主鍵，自動遞增 |
| device_code | VARCHAR(50) | 設備編號，唯一 |
| device_name | VARCHAR(100) | 設備名稱 |
| device_type | VARCHAR(50) | 設備類型 |
| location | VARCHAR(100) | 設備位置 |
| status | VARCHAR(20) | 設備狀態 |
| ip_address | VARCHAR(45) | 設備 IP，支援 IPv4 / IPv6 |
| created_at | DATETIME | 建立時間 |
| updated_at | DATETIME | 更新時間 |

目前支援的 status：

```text
online
offline
maintenance
```

---

## 專案結構

```text
iot-device-api/
├── app/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── devices.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── device.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── device_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── device.py
│   └── services/
│       ├── __init__.py
│       └── device_service.py
├── scripts/
│   └── init.sql
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 快速開始

### 環境需求

請先安裝：

- Python 3.11+
- MySQL 8.x

---

### 1. 下載專案

```bash
git clone https://github.com/your-username/iot-device-api.git
cd iot-device-api
```

請將 `your-username` 改成你的 GitHub 帳號。

---

### 2. 建立虛擬環境

```bash
python -m venv .venv
```

啟動虛擬環境。

Linux / macOS：

```bash
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

---

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

---

### 4. 設定環境變數

複製 `.env.example`：

Linux / macOS：

```bash
cp .env.example .env
```

修改 `.env`：

```env
APP_NAME=IoT Device Management API
DEBUG=true

DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/iot_device?charset=utf8mb4
```

請將：

```text
your_password
```

改成你自己的 MySQL 密碼。

---

### 5. 初始化資料庫

方式一：手動建立資料庫。

```sql
CREATE DATABASE iot_device;
```

方式二：執行初始化腳本。

```bash
mysql -u root -p < scripts/init.sql
```

---

### 6. 啟動服務

```bash
uvicorn app.main:app --reload
```

預設服務位址：

```text
http://127.0.0.1:8000
```

Swagger UI：

```text
http://127.0.0.1:8000/docs
```

Redoc：

```text
http://127.0.0.1:8000/redoc
```

健康檢查：

```text
http://127.0.0.1:8000/health
```

---


## API 說明

### 基本資訊

Base URL：

```text
http://127.0.0.1:8000
```

---

## Health Check

### 健康檢查

```http
GET /health
```

範例：

```bash
curl http://127.0.0.1:8000/health
```

回應：

```json
{
  "status": "ok"
}
```

---

## Devices API

### 1. 新增設備

```http
POST /devices
```

Request Body：

```json
{
  "device_code": "DEV-001",
  "device_name": "溫濕度感測器",
  "device_type": "sensor",
  "location": "Taipei",
  "status": "online",
  "ip_address": "192.168.1.10"
}
```

curl 範例：

```bash
curl -X POST http://127.0.0.1:8000/devices \
  -H "Content-Type: application/json" \
  -d '{
    "device_code": "DEV-001",
    "device_name": "溫濕度感測器",
    "device_type": "sensor",
    "location": "Taipei",
    "status": "online",
    "ip_address": "192.168.1.10"
  }'
```

成功回應：

```json
{
  "id": 1,
  "device_code": "DEV-001",
  "device_name": "溫濕度感測器",
  "device_type": "sensor",
  "location": "Taipei",
  "status": "online",
  "ip_address": "192.168.1.10",
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-01T10:00:00"
}
```

錯誤：

- `409 Conflict`：device_code 已存在。
- `422 Unprocessable Entity`：輸入資料不合法。

---

### 2. 查詢設備列表

```http
GET /devices
```

支援 Query Parameters：

| 參數 | 型別 | 說明 |
|---|---:|---|
| status | string | 依狀態過濾 |
| location | string | 依位置過濾 |
| device_type | string | 依設備類型過濾 |
| keyword | string | 搜尋 device_code 或 device_name |
| page | int | 頁碼 |
| page_size | int | 每頁筆數 |

範例：

```bash
curl "http://127.0.0.1:8000/devices"
```

依狀態查詢：

```bash
curl "http://127.0.0.1:8000/devices?status=online"
```

依位置查詢：

```bash
curl "http://127.0.0.1:8000/devices?location=Taipei"
```

依設備類型查詢：

```bash
curl "http://127.0.0.1:8000/devices?device_type=sensor"
```

關鍵字搜尋：

```bash
curl "http://127.0.0.1:8000/devices?keyword=DEV"
```

分頁查詢：

```bash
curl "http://127.0.0.1:8000/devices?page=1&page_size=20"
```

組合查詢：

```bash
curl "http://127.0.0.1:8000/devices?status=online&location=Taipei&page=1&page_size=10"
```

回應範例：

```json
{
  "total": 1,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": 1,
      "device_code": "DEV-001",
      "device_name": "溫濕度感測器",
      "device_type": "sensor",
      "location": "Taipei",
      "status": "online",
      "ip_address": "192.168.1.10",
      "created_at": "2026-01-01T10:00:00",
      "updated_at": "2026-01-01T10:00:00"
    }
  ]
}
```

---

### 3. 查詢單一設備

```http
GET /devices/{device_id}
```

範例：

```bash
curl http://127.0.0.1:8000/devices/1
```

成功回應：

```json
{
  "id": 1,
  "device_code": "DEV-001",
  "device_name": "溫濕度感測器",
  "device_type": "sensor",
  "location": "Taipei",
  "status": "online",
  "ip_address": "192.168.1.10",
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-01T10:00:00"
}
```

錯誤：

- `404 Not Found`：找不到設備。

---

### 4. 更新設備

```http
PUT /devices/{device_id}
```

Request Body：

```json
{
  "device_name": "溫濕度感測器 A",
  "location": "Taichung",
  "status": "maintenance",
  "ip_address": "192.168.1.20"
}
```

curl 範例：

```bash
curl -X PUT http://127.0.0.1:8000/devices/1 \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "溫濕度感測器 A",
    "location": "Taichung",
    "status": "maintenance",
    "ip_address": "192.168.1.20"
  }'
```

成功回應：

```json
{
  "id": 1,
  "device_code": "DEV-001",
  "device_name": "溫濕度感測器 A",
  "device_type": "sensor",
  "location": "Taichung",
  "status": "maintenance",
  "ip_address": "192.168.1.20",
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-01T12:00:00"
}
```

注意：

- `device_code` 不可更新。
- 若沒有提供任何更新欄位，會回傳 `400 Bad Request`。

---

### 5. 刪除設備

```http
DELETE /devices/{device_id}
```

範例：

```bash
curl -X DELETE http://127.0.0.1:8000/devices/1
```

成功時回傳：

```text
204 No Content
```

錯誤：

- `404 Not Found`：找不到設備。

---

## Statistics API

### 設備統計

```http
GET /devices/statistics
```

Query Parameters：

| 參數 | 必填 | 型別 | 說明 |
|---|---:|---|---|
| group_by | 是 | string | 分組欄位 |
| min_count | 否 | int | 最小數量，對應 HAVING COUNT(*) >= min_count |

`group_by` 支援：

```text
status
location
device_type
```

---

### 依狀態統計

```bash
curl "http://127.0.0.1:8000/devices/statistics?group_by=status"
```

回應範例：

```json
{
  "group_by": "status",
  "items": [
    {
      "label": "online",
      "count": 5
    },
    {
      "label": "offline",
      "count": 3
    }
  ]
}
```

對應 SQL 概念：

```sql
SELECT status, COUNT(*) AS count
FROM devices
GROUP BY status;
```

---

### 依位置統計

```bash
curl "http://127.0.0.1:8000/devices/statistics?group_by=location"
```

回應範例：

```json
{
  "group_by": "location",
  "items": [
    {
      "label": "Taipei",
      "count": 4
    },
    {
      "label": "Taichung",
      "count": 2
    }
  ]
}
```

對應 SQL 概念：

```sql
SELECT location, COUNT(*) AS count
FROM devices
GROUP BY location;
```

---

### 依設備類型統計

```bash
curl "http://127.0.0.1:8000/devices/statistics?group_by=device_type"
```

回應範例：

```json
{
  "group_by": "device_type",
  "items": [
    {
      "label": "sensor",
      "count": 6
    },
    {
      "label": "gateway",
      "count": 2
    }
  ]
}
```

對應 SQL 概念：

```sql
SELECT device_type, COUNT(*) AS count
FROM devices
GROUP BY device_type;
```

---

### 使用 HAVING COUNT

```bash
curl "http://127.0.0.1:8000/devices/statistics?group_by=status&min_count=2"
```

對應 SQL 概念：

```sql
SELECT status, COUNT(*) AS count
FROM devices
GROUP BY status
HAVING COUNT(*) >= 2;
```

---

## 錯誤處理

| HTTP Status | 情境 |
|---|---|
| 400 | 查詢參數或輸入資料不合法 |
| 404 | 找不到設備 |
| 409 | device_code 已存在 |
| 422 | FastAPI 輸入驗證失敗 |
| 500 | 伺服器內部錯誤 |

錯誤回應範例：

```json
{
  "detail": "Device id 999 not found"
}
```

---

## License
Copyright © 2026 hanwu910514.

詳情請參閱[Apache License 2.0](LICENSE)檔案
