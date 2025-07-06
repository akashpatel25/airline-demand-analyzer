import { useState, useEffect } from 'react'
import Filters from '../components/Filters'
import Charts from '../components/Charts'
import Loader from '../components/Loader'
import styles from '../styles/Home.module.css'
import { fetchRoutes, searchFlights } from '../utils/api'

export default function Home() {
  const [flights, setFlights] = useState(null)
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState({
    routes: true,
    flights: false
  })
  const [error, setError] = useState(null)

  useEffect(() => {
    console.log('Initializing component...')
    const loadRoutes = async () => {
      try {
        console.log('Fetching route data...')
        const data = await fetchRoutes()
        console.log('Received route data:', data)
        setRoutes(data.routes)
      } catch (err) {
        console.error('Route fetch error:', err)
        setError('Failed to load route data. Please refresh the page.')
      } finally {
        setLoading(prev => ({ ...prev, routes: false }))
      }
    }
    loadRoutes()
  }, [])

  const handleSearch = async (params) => {
    console.log('Search initiated with params:', params)
    setError(null)
    setLoading(prev => ({ ...prev, flights: true }))
    
    try {
      const data = await searchFlights(params)
      console.log('Flight search results:', data)
      setFlights(data)
    } catch (err) {
      console.error('Flight search error:', err)
      setError('Failed to fetch flights. Please check your connection and try again.')
    } finally {
      setLoading(prev => ({ ...prev, flights: false }))
      console.log('Search completed')
    }
  }

  console.log('Current state:', { flights, routes, loading, error })

  if (loading.routes) {
    return <Loader message="Loading route information..." />
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Airline Demand Analyzer</h1>
      
      {error && (
        <div className={styles.error}>
          {error}
          <button 
            onClick={() => window.location.reload()} 
            className={styles.retryButton}
          >
            Retry
          </button>
        </div>
      )}
      
      <Filters onSubmit={handleSearch} loading={loading.flights} />
      
      {loading.flights ? (
        <Loader message="Searching for flights..." />
      ) : flights ? (
        <>
          <Charts flights={flights.data} routes={routes} />
          <div className={styles.insights}>
            <h2>Travel Insights</h2>
            <p>{flights.insights.recommendation}</p>
            <p>Average price: ${flights.insights.price_summary.average}</p>
            <p>Price trend: {flights.insights.price_summary.trend}</p>
            <p>Airlines: {flights.insights.airlines.join(', ')}</p>
          </div>
        </>
      ) : (
        <div className={styles.placeholder}>
          <p>Search for flights to see data visualization</p>
        </div>
      )}
    </div>
  )
}