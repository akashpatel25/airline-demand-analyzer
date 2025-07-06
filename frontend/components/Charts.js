import { Bar, Line } from 'react-chartjs-2'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  LineElement,
  PointElement,
  Title, 
  Tooltip, 
  Legend 
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
)

export default function Charts({ flights, routes }) {
  console.log('Rendering charts with data:', { flights, routes })
  
  // Process data for charts
  const airlines = [...new Set(flights.map(f => f.airline))]
  const avgPrices = airlines.map(airline => {
    const airlineFlights = flights.filter(f => f.airline === airline)
    return (airlineFlights.reduce((sum, f) => sum + f.price, 0) / airlineFlights.length).toFixed(2)
  })

  return (
    <div className="chart-grid">
      <div className="chart-container">
        <h3>Flight Prices by Airline</h3>
        <Bar
          data={{
            labels: airlines,
            datasets: [{
              label: 'Average Price (AUD)',
              data: avgPrices,
              backgroundColor: 'rgba(53, 162, 235, 0.5)',
            }]
          }}
          options={{ responsive: true }}
        />
      </div>

      <div className="chart-container">
        <h3>Popular Routes</h3>
        <Line
          data={{
            labels: routes.map(r => r.route),
            datasets: [{
              label: 'Daily Flights',
              data: routes.map(r => r.flights_per_day),
              borderColor: 'rgb(255, 99, 132)',
              backgroundColor: 'rgba(255, 99, 132, 0.5)',
            }]
          }}
          options={{ responsive: true }}
        />
      </div>
    </div>
  )
}