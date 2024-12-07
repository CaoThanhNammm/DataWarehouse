create database if not exists datawarehouse;
use datawarehouse;

ALTER DATABASE datawarehouse
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

DROP TABLE IF EXISTS product_dim;
CREATE TABLE IF NOT EXISTS product_dim (
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
      FOREIGN KEY (date_sk) REFERENCES date_dim(date_sk)  -- Tạo liên kết với bảng date_dim
);


-- tạo bảng date_dim
DROP TABLE IF EXISTS date_dim;
CREATE TABLE IF NOT EXISTS date_dim (
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

CREATE TABLE IF NOT EXISTS monthdim (
                            monthSk int(11) NOT NULL,
                            calendarYearMonth varchar(255) DEFAULT NULL,
                            dateSkEnd int(11) DEFAULT NULL,
                            dateSkStart int(11) DEFAULT NULL,
                            monthSince2005 int(11) DEFAULT NULL
)
ALTER TABLE `monthdim`
    ADD PRIMARY KEY (`monthSk`) USING BTREE;
COMMIT;
DROP TABLE IF EXISTS month_dim;
-- Load date_dim từ csv vào datawarehouse
LOAD DATA INFILE 'D:\\date_dim.csv'
INTO TABLE date_dim
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 0 ROWS;
-- Load month_dim từ csv vào datawarehouse
LOAD DATA INFILE 'D:\\month_dim.csv'
INTO TABLE date_dim
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 0 ROWS;