import express from "express"
import mysql from "mysql2"
import bodyParser from "body-parser"
import cors from "cors"

const app = express()
const port = 5000

// Middleware
app.use(cors())
app.use(bodyParser.json())

// Kết nối với MySQL
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "datamart",
})

db.connect((err) => {
  if (err) {
    console.error("Kết nối MySQL thất bại:", err)
    return
  }
  console.log("Đã kết nối với MySQL")
})

// API: Lấy danh sách tất cả người dùng
app.get("/users", (req, res) => {
  const query = "SELECT * FROM users"
  db.query(query, (err, results) => {
    if (err) {
      res.status(500).json({ error: "Lỗi truy vấn MySQL" })
    } else {
      res.json(results)
    }
  })
})

// API: Thêm một người dùng mới
app.post("/users", (req, res) => {
  const { name, email } = req.body
  const query = "INSERT INTO users (name, email) VALUES (?, ?)"
  db.query(query, [name, email], (err, results) => {
    if (err) {
      res.status(500).json({ error: "Lỗi thêm dữ liệu" })
    } else {
      res.json({ message: "Thêm thành công", id: results.insertId })
    }
  })
})
const formatDate = (dateString) => {
  const date = new Date(dateString)

  const day = String(date.getDate()).padStart(2, "0")
  const month = String(date.getMonth() + 1).padStart(2, "0") // tháng bắt đầu từ 0
  const year = date.getFullYear()
  return `${day}/${month}/${year}`
}
app.get("/products", (req, res) => {
  function formatCurrency(value) {
    // Ép kiểu về số và đảm bảo giá trị đầu vào hợp lệ
    if (typeof value !== "number") {
      value = parseFloat(value)
    }
    if (isNaN(value)) {
      return "Invalid number"
    }

    // Định dạng số với dấu '.' phân cách hàng nghìn
    return value.toLocaleString("vi-VN", { minimumFractionDigits: 0 })
  }
  const query = "SELECT * FROM product WHERE isDelete = 0"

  db.query(query, (err, results) => {
    if (err) {
      res.status(500).json({ error: "Lỗi truy vấn MySQL" })
    } else {
      // Chuyển đổi giá trị price từ chuỗi có dấu chấm và ký tự ₫ thành số
      results.forEach((product) => {
        if (product.priceSale) {
          product.priceSale = formatCurrency(product.priceSale)
        }
        if (product.color) {
          product.color = product.color.replace(/^:/, "").trim()
        }
        if (product.created_at && product.date_insert && product.expired_date) {
          product.created_at = formatDate(product.created_at)
          product.date_insert = formatDate(product.date_insert)
          product.expired_date = formatDate(product.expired_date)
        }
      })

      res.json(results)
    }
  })
})

app.get("/products/names", (req, res) => {
  const query = "SELECT DISTINCT name FROM product WHERE isDelete = 0" // Lấy tất cả tên sản phẩm
  db.query(query, (err, results) => {
    if (err) {
      return res.status(500).json({ error: "Lỗi truy vấn MySQL" })
    }
    res.json(results) // Trả về danh sách tên sản phẩm
  })
})
//Lấy sản phẩm theo tên
app.get("/products/highest-price-by-name/:name", (req, res) => {
  const { name } = req.params

  const query = `
        SELECT * FROM product p1
        WHERE p1.price = (
            SELECT MAX(p2.price)
            FROM product p2
            WHERE p2.name = p1.name AND p2.name = ?
        ) AND p1.isDelete = 0
    `

  db.query(query, [name], (err, results) => {
    if (err) {
      return res.status(500).json({ error: "Lỗi truy vấn MySQL" })
    }
    res.json(results)
  })
})
app.get("/products/:name", (req, res) => {
  const { name } = req.params
  const query = "SELECT * FROM product WHERE name = ? AND isDelete = 0" // Truy vấn sản phẩm theo tên

  db.query(query, [name], (err, results) => {
    if (err) {
      console.error("Lỗi truy vấn MySQL:", err)
      return res.status(500).json({ error: "Lỗi truy vấn MySQL" })
    }

    // Nếu không tìm thấy sản phẩm, trả về thông báo không tìm thấy
    if (results.length === 0) {
      return res.status(404).json({ error: "Sản phẩm không tìm thấy" })
    }

    // Xử lý dữ liệu
    const output = results.reduce((acc, product) => {
      // Chuyển đổi giá trị priceSale và gán vào màu sắc
      const cleanedPriceSale = parseInt(
        product.price.replace(/\./g, "").replace(" ₫", "")
      )

      // Xử lý ngày insert
      const dateInsert = new Date(product.date_insert)
        .toISOString()
        .split("T")[0] // Định dạng ngày YYYY-MM-DD

      // Tạo đối tượng theo từng ngày
      if (!acc[dateInsert]) {
        acc[dateInsert] = { date_insert: dateInsert } // Nếu chưa có ngày, thêm vào
      }

      // Thêm giá trị priceSale vào đối tượng với key là màu sắc
      acc[dateInsert][product.color] = cleanedPriceSale

      return acc
    }, {})

    // Trả về kết quả dưới dạng mảng
    res.json(Object.values(output))
  })
})

app.get("/api/stats/total", (req, res) => {
  const query = "SELECT COUNT(*) AS total FROM product" // Tổng số TV
  db.query(query, (err, result) => {
    if (err) {
      res.status(500).send("Error fetching total count")
    } else {
      res.json(result[0])
    }
  })
})
app.get("/api/products/highest-price", (req, res) => {
  const query = "SELECT MAX(priceSale) AS maxPriceSale FROM Product"

  db.query(query, (err, result) => {
    if (err) throw err
    result.map((product) => {
      if (product.price) {
        return product.price
      }
    })
    res.json(result)
  })
})
app.get("/api/products/lowest-price", (req, res) => {
  const query =
    "SELECT min(priceSale) as minPrice FROM product WHERE priceSale <> 0 and isDelete = 0"

  db.query(query, (err, result) => {
    if (err) throw err
    result.map((product) => {
      if (product.price) {
        // Loại bỏ dấu chấm và ký tự ₫, sau đó chuyển thành số
        const cleanedPrice = product.price.replace(/\./g, "").replace(" ₫", "")
        product.price = parseFloat(cleanedPrice) // Chuyển chuỗi thành số
        let formattedPrice = new Intl.NumberFormat("vi-VN", {
          style: "currency",
          currency: "VND",
        }).format(product.price)
        formattedPrice = formattedPrice.replace("₫", "VND")
        product.price = formattedPrice
        return product
      }
    })
    res.json(result)
  })
})
app.get("/api/products/price-range", (req, res) => {
  const query = `
         SELECT 
            CASE
                WHEN priceSale < 5000000 THEN 'Dưới 5 triệu'
                WHEN priceSale BETWEEN 5000000 AND 10000000 THEN 'Từ 5-10 triệu'
                ELSE 'Trên 10 triệu'
            END AS priceRange, 
            COUNT(*) AS count 
        FROM product 
        GROUP BY priceRange
        ORDER BY count DESC` // Sắp xếp theo số lượng phân khúc giá giảm dần
  db.query(query, (err, result) => {
    if (err) {
      res.status(500).send("Error fetching price range stats")
    } else {
      res.json(result)
    }
  })
})
app.get("/average-price", (req, res) => {
  const query = "SELECT AVG(priceSale) AS average_price FROM product"

  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching data:", err)
      return res.status(500).json({ error: "Internal Server Error" })
    }

    // Làm tròn giá trung bình đến 2 chữ số thập phân
    const averagePrice = parseFloat(results[0].average_price).toFixed(2)

    res.status(200).json({
      average_price: parseFloat(averagePrice), // Đảm bảo kết quả là số (không phải chuỗi)
    })
  })
})
app.get("/total-products", (req, res) => {
  const query = "SELECT COUNT(*) AS total FROM product WHERE isDelete = 0"

  db.query(query, (err, results) => {
    if (err) {
      console.error("Lỗi khi truy vấn MySQL:", err)
      return res.status(500).json({ error: "Lỗi máy chủ" })
    }

    res.json({ total: results[0].total })
  })
})
app.get("/available-products", (req, res) => {
  const query =
    "SELECT COUNT(*) AS total_in_stock FROM product WHERE status = 'Còn hàng' AND isDelete = 0"

  db.query(query, (err, results) => {
    if (err) {
      console.error("Lỗi khi truy vấn MySQL:", err)
      return res.status(500).json({ error: "Lỗi máy chủ" })
    }

    res.json({ total_in_stock: results[0].total_in_stock })
  })
})
app.get("/out-of-stock-products", (req, res) => {
  const query =
    "SELECT COUNT(*) AS total_out_of_stock FROM product WHERE status = 'Hết hàng' and isDelete = 0"

  db.query(query, (err, results) => {
    if (err) {
      console.error("Lỗi khi truy vấn MySQL:", err)
      return res.status(500).json({ error: "Lỗi máy chủ" })
    }

    res.json({ total_out_of_stock: results[0].total_out_of_stock })
  })
})
app.listen(port, () => {
  console.log(`Server đang chạy tại http://localhost:${port}`)
})
