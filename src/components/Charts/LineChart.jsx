import axios from "axios"
import { useEffect, useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"

const LineChartComponent = () => {
  const [groupedPrice, setGroupedPrice] = useState([])

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
  useEffect(() => {
    const fetchDataProducts = async () => {
      try {
        const reponse = await axios.get("http://localhost:5000/products")
        const productData = reponse?.data
        categorizePriceRange(productData)
      } catch (error) {
        console.log(error)
      }
    }
    fetchDataProducts()
  }, [])
  //   <div>
  //   <h2>Biểu đồ đường (Line Chart)</h2>
  //   <ResponsiveContainer width="100%" height={400}>
  //     <LineChart data={products}>
  //       <CartesianGrid strokeDasharray="3 3" />
  //       <XAxis dataKey="name" />
  //       <YAxis />
  //       <Tooltip />
  //       <Legend />
  //       <Line
  //         type="monotone"
  //         dataKey="price"
  //         stroke="#8884d8"
  //         activeDot={{ r: 8 }}
  //       />
  //     </LineChart>
  //   </ResponsiveContainer>
  // </div>
  return (
    <div className="w-[800px]">
      <h2>Biểu đồ đường (Line Chart)</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={groupedPrice} margin={{ left: 30 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip label="Giá" />
          <Legend />
          <Line
            type="monotone"
            dataKey="count"
            name="Giá"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default LineChartComponent
