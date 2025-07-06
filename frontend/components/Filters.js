import { useState } from 'react'
import styles from '../styles/Home.module.css'

export default function Filters({ onSubmit, loading }) {
  const [form, setForm] = useState({
    origin: 'SYD',
    destination: 'MEL',
    date: new Date().toISOString().split('T')[0],
    return_date: ''
  })

  const handleChange = (e) => {
    console.log('Form field changed:', e.target.name, e.target.value)
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Form submitted:', form)
    onSubmit(form)
  }

  return (
    <form onSubmit={handleSubmit} className={styles.filters}>
      <div className={styles.filterGroup}>
        <label>Origin Airport</label>
        <select 
          name="origin" 
          value={form.origin}
          onChange={handleChange}
          required
          disabled={loading}
        >
          <option value="SYD">Sydney (SYD)</option>
          <option value="MEL">Melbourne (MEL)</option>
          <option value="BNE">Brisbane (BNE)</option>
          <option value="PER">Perth (PER)</option>
        </select>
      </div>

      <div className={styles.filterGroup}>
        <label>Destination Airport</label>
        <select 
          name="destination" 
          value={form.destination}
          onChange={handleChange}
          required
          disabled={loading}
        >
          <option value="MEL">Melbourne (MEL)</option>
          <option value="SYD">Sydney (SYD)</option>
          <option value="BNE">Brisbane (BNE)</option>
          <option value="PER">Perth (PER)</option>
        </select>
      </div>

      <div className={styles.filterGroup}>
        <label>Departure Date</label>
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
          min={new Date().toISOString().split('T')[0]}
          required
          disabled={loading}
        />
      </div>

      <div className={styles.filterGroup}>
        <label>Return Date (Optional)</label>
        <input
          type="date"
          name="return_date"
          value={form.return_date}
          onChange={handleChange}
          min={form.date}
          disabled={loading}
        />
      </div>

      <button 
        type="submit" 
        disabled={loading}
        className={styles.submitButton}
      >
        {loading ? 'Searching...' : 'Find Flights'}
      </button>
    </form>
  )
}