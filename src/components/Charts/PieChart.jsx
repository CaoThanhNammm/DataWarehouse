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
  const [priceRange, setPriceRange] = useState([])
  useEffect(() => {
    fetchPriceRange()
  }, [])

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

  return (
    <div className="w-[100%]">
      {/* <h2>Biểu đồ giá sản phẩm</h2> */}
      <ResponsiveContainer width="100%" height={600}>
        <PieChart>
          <Pie
            data={priceRange}
            dataKey="count"
            nameKey="priceRange"
            cx="50%"
            cy="50%"
            outerRadius={150}
            label
            isAnimationActive={false}
          >
            {priceRange.map((entry, index) => (
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
