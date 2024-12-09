create database if not exists datawarehouse;
use datawarehouse;

ALTER DATABASE datawarehouse
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

DROP TABLE IF EXISTS productDim;
CREATE TABLE IF NOT EXISTS productDim (
  product_sk INT AUTO_INCREMENT PRIMARY KEY,
  id VARCHAR(255) NULL DEFAULT NULL,
  name VARCHAR(255) NULL DEFAULT NULL,
  price decimal(15,2) NULL DEFAULT NULL,
  priceSale decimal(15,2) NULL DEFAULT NULL,
  brand VARCHAR(255) NULL DEFAULT NULL,
  color VARCHAR(255) NULL DEFAULT NULL,
  size VARCHAR(255) NULL DEFAULT NULL,
  status VARCHAR(255) NULL DEFAULT NULL,
  description_part1 VARCHAR(255) NULL DEFAULT NULL,
  description_part2 VARCHAR(255) NULL DEFAULT NULL,
  description_part3 VARCHAR(255) NULL DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  isDelete BOOLEAN DEFAULT FALSE,  -- Cột kiểm tra trạng thái xóa
  date_delete DATE,                -- Ngày xóa
  date_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Ngày chèn
  expired_date DATE DEFAULT '9999-12-31',  -- Ngày hết hạn mặc định
  date_sk INT,                     -- Thêm cột date_sk để lưu khóa từ bảng date_dim
      FOREIGN KEY (date_sk) REFERENCES datedim(date_sk)  -- Tạo liên kết với bảng date_dim
);

