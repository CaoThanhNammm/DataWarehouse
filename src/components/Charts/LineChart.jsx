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
  const [priceRange, setPriceRange] = useState([])

  const fetchPriceRange = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/api/products/price-range"
      )
      const priceRangeData = response?.data
      setPriceRange(priceRangeData)
    } catch (error) {
      console.log(error)
    }
  }
  useEffect(() => {
    fetchPriceRange()
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
        <LineChart data={priceRange} margin={{ left: 30 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="priceRange" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="count"
            name="count"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default LineChartComponent
