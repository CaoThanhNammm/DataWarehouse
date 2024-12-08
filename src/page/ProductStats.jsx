import { useEffect, useState } from "react"

import BarChartComponent from "../components/Charts/BarChart"
import LineChartComponent from "../components/Charts/LineChart"
import axios from "axios"
import PieChartComponent from "../components/Charts/PieChart"

const ProductStats = () => {
  const [stats, setStats] = useState([
    {
      highestPrice: 0,
      lowestPrice: 0,
    },
  ])
  const [priceRange, setPriceRange] = useState([])
  const [totalProduct, setTotalProduct] = useState(0)
  const [countAvailableProduct, setCountAvailableProduct] = useState(0)
  const [countNotAvailableProduct, setCountNotAvailableProduct] = useState(0)
  const fetchStats = async () => {
    try {
      const [highestPrice, lowestPrice] = await Promise.all([
        axios.get("http://localhost:5000/api/products/highest-price"),
        axios.get("http://localhost:5000/api/products/lowest-price"),
      ])
      console.log(lowestPrice)
      setStats({
        highestPrice: highestPrice?.data[0]?.price,
        lowestPrice: lowestPrice?.data[0]?.minPrice,
      })
    } catch (err) {
      console.log(err)
    }
  }
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
  const fetchTotalProduct = async () => {
    try {
      const response = await axios.get("http://localhost:5000/total-products")
      const totalProductData = response?.data.total
      setTotalProduct(totalProductData)
    } catch (error) {
      console.log(error)
    }
  }

  const fetchAvailableProduct = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/available-products"
      )
      const countAvailableProduct = response?.data?.total_in_stock
      setCountAvailableProduct(countAvailableProduct)
    } catch (err) {
      console.log(err)
    }
  }
  const fetchNotAvailableProduct = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/out-of-stock-products"
      )
      const countNotAvailableProduct = response?.data?.total_out_of_stock
      setCountNotAvailableProduct(countNotAvailableProduct)
    } catch (err) {
      console.log(err)
    }
  }
  useEffect(() => {
    fetchTotalProduct()
    fetchAvailableProduct()
    fetchNotAvailableProduct()
    fetchStats()
    fetchPriceRange()
  }, [])

  return (
    <div>
      <div className="p-10 text-xl">
        <h1 className="text-center text-3xl font-bold">Thống kê sản phẩm</h1>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Tổng số sản phẩm:</p>
          <p>{totalProduct} sản phẩm</p>
        </div>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Số sản phẩm còn hàng:</p>
          <p>{countAvailableProduct} sản phẩm</p>
        </div>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Số sản phẩm hết hàng:</p>
          <p>{countNotAvailableProduct} sản phẩm</p>
        </div>
      </div>
      <div className="p-10 text-xl">
        {" "}
        <h1>Thống kê sản phẩm theo giá:</h1>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Giá cao nhất:</p>

          <p>{stats.highestPrice} triệu VND</p>
        </div>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Giá thấp nhất:</p>

          <p>{stats.lowestPrice} triệu VND</p>
        </div>
        {priceRange?.map((item, index) => {
          return (
            <div key={index} className="flex gap-10 my-4">
              <p className="font-bold w-[30%]">{item.priceRange}</p>

              <p> {item.count} sản phẩm</p>
            </div>
          )
        })}
      </div>
      <main className=" min-h-screen items-center px-4 md:px-8 xl:px-10 py-44">
        <div className="flex flex-col w-full gap-20 max-w-[1400px]">
          <GridItem title="Biểu đồ cột">
            <BarChartComponent
              highestPrice={stats?.highestPrice}
              lowestPrice={stats?.lowestPrice}
            />
          </GridItem>
          {/* <GridItem title="Bar Chart">
            <BarChartComponent />
          </GridItem>
          <GridItem title="Line Chart">
            <LineChartComponent />
          </GridItem> */}
          <GridItem title="Biểu đồ tròn">
            <PieChartComponent />
          </GridItem>
          <GridItem title="Biểu đồ đường">
            <LineChartComponent />
          </GridItem>
        </div>
      </main>
    </div>
  )
}

// eslint-disable-next-line react/prop-types
const GridItem = ({ title, children }) => {
  return (
    <div className="flex flex-col items-center justify-center p-4 border  rounded-xl w-[1000px] h-[500px]">
      <h3 className="text-2xl font-semibold text-black mb-4s">{title}</h3>
      {children}
    </div>
  )
}
export default ProductStats
