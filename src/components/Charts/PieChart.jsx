import { useEffect, useState } from "react"
import axios from "axios"
import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts"

const PieChartComponent = () => {
  const [groupedPrice, setGroupedPrice] = useState([])
  useEffect(() => {
    // Ví dụ về cách lấy dữ liệu từ API
    axios
      .get("http://localhost:5000/products") // Giả sử API trả về danh sách sản phẩm
      .then((response) => {
        // Giả sử bạn có data để phân loại sản phẩm theo các giá

        categorizePriceRange(response?.data)
      })
      .catch((error) => console.error("Error fetching data:", error))
  }, [])
  const categorizePriceRange = (products) => {
    const grouped = [
      {
        name: "Giá dưới 2 triệu",
        count: products.filter((product) => product.price < 2000000).length,
      },
      {
        name: "Giá từ 2 triệu đến 5 triệu",
        count: products.filter(
          (product) => product.price >= 2000000 && product.price <= 5000000
        ).length,
      },
      {
        name: "Giá trên 5 triệu",
        count: products.filter((product) => product.price > 5000000).length,
      },
    ]
    console.log(grouped)
    setGroupedPrice(grouped) // Cập nhật mảng các nhóm sản phẩm
  }

  return (
    <div className="w-[100%]">
      {/* <h2>Biểu đồ giá sản phẩm</h2> */}
      <ResponsiveContainer width="100%" height={600}>
        <PieChart>
          <Pie
            data={groupedPrice}
            dataKey="count"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={150}
            label
            isAnimationActive={false}
          >
            {groupedPrice.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  index === 0 ? "#f16f47" : index === 1 ? "#009487" : "#e64486"
                }
              />
            ))}
          </Pie>
          <Legend />
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

export default PieChartComponent
