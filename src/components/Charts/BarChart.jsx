/* eslint-disable react/prop-types */
import axios from "axios"
import { useEffect, useState } from "react"
import {
  ResponsiveContainer,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
} from "recharts"

// eslint-disable-next-line react/prop-types
const BarChartComponent = ({ highestPrice, lowestPrice }) => {
  const [averagePrice, setAveragePrice] = useState(0)
  const calculateAveragePrice = (products) => {
    if (products.length === 0) {
      setAveragePrice(0)
      return
    }
    console.log(products)
    const total = products.reduce((sum, product) => sum + product.price, 0)
    const average = total / products.length
    console.log(average)
    setAveragePrice(average)
  }
  useEffect(() => {
    const fetchDataProducts = async () => {
      try {
        const reponse = await axios.get("http://localhost:5000/products")
        const productData = reponse?.data
        calculateAveragePrice(productData)
      } catch (error) {
        console.log(error)
      }
    }
    fetchDataProducts()
  }, [])
  // eslint-disable-next-line react/prop-types
  const cleanedPriceHighest = highestPrice?.replace(/[.,VND]/g, "")
  const highestPriceInt = parseInt(cleanedPriceHighest, 10)
  // eslint-disable-next-line react/prop-types
  const cleanedPriceLowest = lowestPrice?.replace(/[.,VND]/g, "")
  const lowestPriceInt = parseInt(cleanedPriceLowest, 10)

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={[
          { name: "Giá Thấp Nhất", value: lowestPriceInt },
          { name: "Giá Trung Bình ", value: averagePrice },
          { name: "Giá Cao Nhất", value: highestPriceInt },
        ]}
        margin={{ left: 30 }}
      >
        <CartesianGrid />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Bar dataKey="value" name="Giá" fill="#2563eb" />
      </BarChart>
    </ResponsiveContainer>
  )
}
// eslint-disable-next-line react/prop-types
const CustomTooltip = ({ active, payload, label }) => {
  // eslint-disable-next-line react/prop-types
  if (active && payload && payload?.length) {
    return (
      <div className="p-4 bg-slate-900 flex flex-col gap-4 rounded-md text-white">
        <p className="text-medium text-lg">{label}</p>
        <p className="text-sm font-bold text-blue-400">
          Giá:{" "}
          <span className="ml-2">
            {payload[0]?.value?.toLocaleString("vi-VN")} VND
          </span>
        </p>
      </div>
    )
  }
}

export default BarChartComponent
