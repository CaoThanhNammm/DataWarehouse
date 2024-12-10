DELIMITER $$

CREATE PROCEDURE LoadDataFromStagingToDW()
BEGIN
START TRANSACTION;



-- Tạo bảng tạm lưu product (check trùng)
CREATE TEMPORARY TABLE temp_product AS
SELECT *,
       TRIM(REPLACE(color, ':', '')) AS processed_color,
       CAST(
               IFNULL(
                       NULLIF(
                               REPLACE(REPLACE(REPLACE(price, '₫', ''), '.', ''), ' ', ''),
                               ''
                       ),
                       '0'
               ) AS DECIMAL(15,2)
       ) AS processed_price,
       CAST(
               IFNULL(
                       NULLIF(
                               REPLACE(REPLACE(REPLACE(priceSale, '₫', ''), '.', ''), ' ', ''),
                               ''
                       ),
                       '0'
               ) AS DECIMAL(15,2)
       ) AS processed_priceSale
FROM staging.bikes;

ALTER TABLE temp_product
    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- Chèn các sản phẩm mới vào productdim nếu chưa có (xử lý null -> N/A)
INSERT INTO datawarehouse.productdim (
    id, name, price, priceSale, brand, color, size, status,
    description_part1, description_part2, description_part3,
    created_at, isDelete, date_insert, expired_date, date_sk
)
SELECT
    COALESCE(tp.id, 'N/A'),
    COALESCE(tp.name, 'N/A'),
    COALESCE(tp.processed_price, 0),  -- Dùng giá trị đã xử lý
    COALESCE(tp.processed_priceSale, 0),  -- Dùng giá trị đã xử lý
    COALESCE(tp.brand, 'N/A'),
    COALESCE(tp.processed_color, 'N/A'), -- Sử dụng giá trị đã xử lý
    COALESCE(tp.size, 'N/A'),
    COALESCE(tp.status, 'N/A'),
    COALESCE(tp.description_part1, 'N/A'),
    COALESCE(tp.description_part2, 'N/A'),
    COALESCE(tp.description_part3, 'N/A'),
    CURRENT_TIMESTAMP,
    FALSE,
    CURRENT_TIMESTAMP,
    '9999-12-31',
    dd.dateSk  -- Lấy date_sk từ bảng date
FROM temp_product tp
         JOIN control.datedim dd ON dd.fullDate = CURRENT_DATE
WHERE NOT EXISTS (
    SELECT 1
    FROM datawarehouse.productdim pd
    WHERE
        pd.name = tp.name
      AND pd.id = tp.id
      AND pd.color = tp.processed_color
      AND pd.size = tp.size
      AND pd.isDelete = FALSE
      AND pd.expired_date = '9999-12-31'
);

-- Tạo bảng tạm để lưu các sản phẩm cần cập nhật
CREATE TEMPORARY TABLE temp_update_products AS
SELECT
    tp.*,
    ROW_NUMBER() OVER (PARTITION BY tp.name, tp.id, tp.color, tp.size ORDER BY tp.timeStartInsert DESC) AS row_num
FROM staging.bikes tp
WHERE EXISTS (
    SELECT 1
    FROM datawarehouse.productdim pd2
    WHERE
        pd2.id = tp.id
      AND pd2.name = tp.name
      AND pd2.color = tp.color
      AND pd2.size = tp.size
      AND pd2.isDelete = FALSE
      AND pd2.expired_date = '9999-12-31'
      AND (
        CAST(
                IFNULL(
                        NULLIF(
                                REPLACE(REPLACE(REPLACE(tp.price, '₫', ''), '.', ''), ' ', ''),
                                ''
                        ),
                        '0'
                ) AS DECIMAL(15,2)
        ) <> pd2.price OR
        CAST(
                IFNULL(
                        NULLIF(
                                REPLACE(REPLACE(REPLACE(tp.priceSale, '₫', ''), '.', ''), ' ', ''),
                                ''
                        ),
                        '0'
                ) AS DECIMAL(15,2)
        ) <> pd2.priceSale OR
        pd2.description_part1 <> tp.description_part1 OR
        pd2.description_part2 <> tp.description_part2 OR
        pd2.description_part3 <> tp.description_part3 OR
        pd2.status <> tp.status
        )
);

-- Bảng tạm chứa các ID sản phẩm cũ cần cập nhật
CREATE TEMPORARY TABLE temp_ids AS
SELECT pd2.product_sk
FROM datawarehouse.productdim pd2
         JOIN temp_update_products tup
              ON tup.id = pd2.id
                  AND tup.name = pd2.name
                  AND tup.color = pd2.color
                  AND tup.size = pd2.size
WHERE pd2.isDelete = FALSE
  AND pd2.expired_date = '9999-12-31';

-- Cập nhật trạng thái "đã xóa" đối với các sản phẩm cũ
UPDATE datawarehouse.productdim pd
SET
    pd.isDelete = TRUE,
    pd.expired_date = CURRENT_DATE,
    pd.date_delete = CURRENT_DATE
WHERE pd.product_sk IN (SELECT product_sk FROM temp_ids);

-- Chèn các sản phẩm mới vào productdim
INSERT INTO datawarehouse.productdim   (
    id, name, price, priceSale, brand, color, size, status,
    description_part1, description_part2, description_part3,
    created_at, isDelete, date_insert, expired_date, date_sk
)
SELECT
    tp.id,
    tp.name,
    tp.price,
    tp.priceSale,
    tp.brand,
    tp.color,
    tp.size,
    tp.status,
    tp.description_part1,
    tp.description_part2,
    tp.description_part3,
    CURRENT_TIMESTAMP,
    FALSE,
    CURRENT_TIMESTAMP,
    '9999-12-31',
    dd.dateSk  -- Lấy date_sk từ bảng date
FROM temp_update_products tp
         JOIN control.datedim dd ON dd.fullDate = CURRENT_DATE
WHERE tp.row_num = 1;  -- Chỉ lấy bản ghi mới nhất

COMMIT;
END$$

DELIMITER ;