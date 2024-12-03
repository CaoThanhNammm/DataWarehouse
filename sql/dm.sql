-- create database if not exists datamart;
use datamart;

ALTER DATABASE datamart
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;


-- tạo bảng date
CREATE TABLE IF NOT EXISTS date (
  date_sk INT PRIMARY KEY,
  full_date DATE NOT NULL,
  day_since_2005 INT NOT NULL,
  month_since_2005 INT NOT NULL,
  day_of_week VARCHAR(10) NOT NULL,
  calendar_month VARCHAR(10) NOT NULL,
  calendar_year INT NOT NULL,
  calendar_year_month VARCHAR(10) NOT NULL, 
  day_of_month INT NOT NULL,
  day_of_year INT NOT NULL,
  week_of_year_sunday INT NOT NULL,
  year_week_sunday VARCHAR(10) NOT NULL,
  week_sunday_start DATE NOT NULL,
  week_of_year_monday INT NOT NULL,
  year_week_monday VARCHAR(10) NOT NULL,
  week_monday_start DATE NOT NULL,
  holiday VARCHAR(15) NOT NULL,
  day_type VARCHAR(10) NOT NULL
);

DROP TABLE IF EXISTS product;
CREATE TABLE IF NOT EXISTS product (
  product_sk INT AUTO_INCREMENT PRIMARY KEY,
  id VARCHAR(255) NULL DEFAULT NULL,
  name VARCHAR(255) NULL DEFAULT NULL,
  price VARCHAR(255) NULL DEFAULT NULL,
  priceSale VARCHAR(255) NULL DEFAULT NULL,
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
  FOREIGN KEY (date_sk) REFERENCES date(date_sk)  -- Tạo liên kết với bảng date_dim
);

