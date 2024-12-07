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

const BarChartComponent = ({ highestPrice, lowestPrice }) => {
  const [averagePrice, setAveragePrice] = useState(0)

  const getAveragePrice = async () => {
    try {
      const response = await axios.get("http://localhost:5000/average-price")
      console.log(response?.data)
      setAveragePrice(response?.data?.average_price)
    } catch (error) {
      console.log(error)
    }
  }
  useEffect(() => {
    getAveragePrice()
  }, [])

  // eslint-disable-next-line react/prop-types

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={[
          { name: "Giá Thấp Nhất", value: lowestPrice },
          { name: "Giá Trung Bình ", value: averagePrice },
          { name: "Giá Cao Nhất", value: highestPrice },
        ]}
        margin={{ left: 30 }}
      >
        <CartesianGrid />
        <XAxis dataKey="name" />
        <YAxis dataKey="value" />
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
          Giá: <span className="ml-2">{payload[0].value} triệu VND</span>
        </p>
      </div>
    )
  }
}

export default BarChartComponent