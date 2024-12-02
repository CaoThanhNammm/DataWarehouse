import "./App.css"
import AreaChart from "./components/Charts/AreaChart"
import BarChartComponent from "./components/Charts/BarChart"
import LineChartComponent from "./components/Charts/LineChart"
function App() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4 md:px-8 xl:px-10 py-44">
      <div className="grid xl:grid-cols-3 lg:grid-cols-2 w-full gap-10 max-w-[1400px]">
        <GridItem title="Area Chart">
          <AreaChart />
        </GridItem>
        <GridItem title="Bar Chart">
          <BarChartComponent />
        </GridItem>
        <GridItem title="Line Chart">
          <LineChartComponent />
        </GridItem>
      </div>
    </main>
  )
}
// eslint-disable-next-line react/prop-types
const GridItem = ({ title, children }) => {
  return (
    <div className="flex flex-col items-center justify-center p-4 border border-slate-900 bg-slate-900 rounded-xl h-[400px]">
      <h3 className="text-2xl font-semibold text-white mb-4">{title}</h3>
      {children}
    </div>
  )
}
export default App
