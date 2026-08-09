CREATE DATABASE IF NOT EXISTS iot_device
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE iot_device;

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