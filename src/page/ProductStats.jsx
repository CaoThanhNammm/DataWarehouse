import { useEffect, useState } from "react"

import BarChartComponent from "../components/Charts/BarChart"
import LineChartComponent from "../components/Charts/LineChart"
import axios from "axios"
import PieChartComponent from "../components/Charts/PieChart"

const ProductStats = () => {
  const [products, setProducts] = useState([])

  const [stats, setStats] = useState([
    {
      highestPrice: 0,
      lowestPrice: 0,
    },
  ])
  const fetchStats = async () => {
    try {
      const [highestPrice, lowestPrice] = await Promise.all([
        axios.get("http://localhost:5000/api/products/highest-price"),
        axios.get("http://localhost:5000/api/products/lowest-price"),
      ])
      setStats({
        highestPrice: highestPrice.data[0].price,
        lowestPrice: lowestPrice.data[0].price,
      })
    } catch (err) {
      console.log(err)
    }
  }
  useEffect(() => {
    const fetchDataProducts = async () => {
      try {
        const reponse = await axios.get("http://localhost:5000/products")

        const productData = reponse?.data
        console.log(productData)
        setProducts(productData)
      } catch (error) {
        console.log(error)
      }
    }
    fetchDataProducts()
    fetchStats()
  }, [])
  return (
    <div>
      <div className="p-10 text-xl">
        {" "}
        <h1>Thống kê sản phẩm theo giá:</h1>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Giá cao nhất:</p>

          <p>{stats.highestPrice}</p>
        </div>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Giá thấp nhất:</p>

          <p>{stats.lowestPrice}</p>
        </div>
        <div className="flex gap-10 my-4">
          <p className="font-bold w-[30%]">Sản phẩm dưới 2 triệu:</p>

          <p>
            {" "}
            {products.filter((product) => product.price < 2000000).length} sản
            phẩm
          </p>
        </div>
        <div className="flex gap-10">
          <p className="font-bold w-[30%]">Sản phẩm có giá từ 2 đến 5 triệu:</p>
          <p>
            {" "}
            {
              products.filter(
                (product) =>
                  product.price >= 2000000 && product.price <= 5000000
              ).length
            }{" "}
            sản phẩm
          </p>
        </div>
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
