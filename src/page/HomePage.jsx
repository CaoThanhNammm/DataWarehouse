import { useEffect, useState } from "react"
import axios from "axios"
import ReactPaginate from "react-paginate"
import { Link } from "react-router-dom"

const HomePage = () => {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [itemsPerPage] = useState(15)
  const [currentPage, setCurrentPage] = useState(0)
  const offset = currentPage * itemsPerPage
  const currentItems = products.slice(offset, offset + itemsPerPage)
  const handlePageClick = (event) => {
    setCurrentPage(event.selected)
  }

  useEffect(() => {
    const fetchDataProducts = async () => {
      try {
        const reponse = await axios.get("http://localhost:5000/products")

        const productData = reponse?.data
        console.log(productData)
        setProducts(productData)
      } catch (error) {
        setError(error.message || "Something went wrong")
      } finally {
        setLoading(false)
      }
    }
    fetchDataProducts()
  }, [])
  if (loading) {
    return <div className="text-center text-blue-500">Loading...</div>
  }

  if (error) {
    return <div className="text-center text-red-500">Error: {error}</div>
  }
  return (
    <div>
      <div className="flex justify-center gap-10">
        <h1 className="text-black text-center text-3xl font-semibold my-4 ">
          Danh sách sản phẩm
        </h1>
        <Link
          to="/stats"
          className="text-black text-center text-3xl font-semibold my-4 underline "
        >
          Thống kê sản phẩm
        </Link>
      </div>

      <div className="overflow-x-auto max-h-[800px]">
        <table className="min-w-full border border-gray-300 text-sm text-left">
          <thead className="bg-gray-200 bg-gray-200 sticky top-0 z-10">
            <tr>
              {Object.keys(products[0]).map((thead) => {
                return (
                  <th
                    className="border border-gray-300 px-4 py-2 text-gray-700 font-medium"
                    key={thead}
                  >
                    {thead}
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody>
            {currentItems.map((product, idx) => (
              <tr key={idx} className="hover:bg-gray-100">
                {Object.values(product).map((value, index) => (
                  <td
                    key={index}
                    className="border border-gray-300 px-4 py-2 text-gray-600"
                  >
                    {typeof value === "string" && value.includes(". ")
                      ? value.split(". ").map((line, i) => (
                          <span key={i}>
                            {line}.
                            <br />
                          </span>
                        ))
                      : value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <ReactPaginate
        previousLabel={"<"}
        nextLabel={">"}
        breakLabel={"..."}
        pageCount={Math.ceil(products.length / itemsPerPage)}
        marginPagesDisplayed={2}
        pageRangeDisplayed={3}
        onPageChange={handlePageClick}
        containerClassName={"pagination flex justify-center mt-4 space-x-2"}
        pageClassName={"px-4 py-2 rounded-md bg-gray-200 hover:bg-gray-300"}
        activeClassName={"bg-blue-500 text-white"}
        previousClassName={"px-4 py-2 rounded-md bg-gray-200 hover:bg-gray-300"}
        nextClassName={"px-4 py-2 rounded-md bg-gray-200 hover:bg-gray-300"}
      />
    </div>
  )
}

export default HomePage
