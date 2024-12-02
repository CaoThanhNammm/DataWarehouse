import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
} from "recharts"
import CustomTooltip from "./CustomTooltip"
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
const BarChartComponent = () => {
  return (
    <ResponsiveContainer>
      <BarChart width={500} height={400} data={salesData}>
        <YAxis />
        <XAxis dataKey="name" />
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Bar
          dataKey="revenue"
          stroke="#2563eb"
          fill="#3b82f6"
          type="monotone"
        />
        <Bar dataKey="profit" stroke="#7c3aed" fill="#8b5cf6" type="monotone" />
      </BarChart>
    </ResponsiveContainer>
  )
}

export default BarChartComponent
