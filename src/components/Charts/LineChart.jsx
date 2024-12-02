import React from "react"
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
const salesData = [
  {
    name: "Jan",
    revenue: 4000,
    profit: 2400,
  },
  {
    name: "Feb",
    revenue: 3000,
    profit: 1398,
  },
  {
    name: "Mar",
    revenue: 9800,
    profit: 2000,
  },
  {
    name: "Apr",
    revenue: 3908,
    profit: 2780,
  },
  {
    name: "May",
    revenue: 4800,
    profit: 1890,
  },
  {
    name: "Jun",
    revenue: 3800,
    profit: 2390,
  },
]
const LineChartComponent = () => {
  return (
    <ResponsiveContainer>
      <LineChart
        width={500}
        height={400}
        margin={{ right: 30 }}
        data={salesData}
      >
        <YAxis />
        <XAxis dataKey="name" />
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip />
        <Legend />
        <Line
          dataKey="revenue"
          stroke="#2563eb"
          fill="#3b82f6"
          type="monotone"
        />
        <Line
          dataKey="profit"
          stroke="#7c3aed"
          fill="#8b5cf6"
          type="monotone"
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

export default LineChartComponent
