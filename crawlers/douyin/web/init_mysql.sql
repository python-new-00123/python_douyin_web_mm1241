-- MySQL 数据库初始化脚本
-- 用于创建 cookies 表

CREATE DATABASE IF NOT EXISTS douyin_cookies CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE douyin_cookies;

CREATE TABLE IF NOT EXISTS cookies (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    service VARCHAR(50) NOT NULL COMMENT '服务名称（如：douyin, tiktok）',
    cookie TEXT NOT NULL COMMENT 'Cookie值',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    is_active TINYINT DEFAULT 1 COMMENT '是否激活（1=激活，0=禁用）',
    ip_address VARCHAR(45) DEFAULT NULL COMMENT '使用此Cookie的机器外网IP',
    INDEX idx_service (service),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Cookies存储表';

-- 插入示例数据（可选）
-- INSERT INTO cookies (service, cookie, is_active) VALUES 
-- ('douyin', 'your_cookie_here', 1);
