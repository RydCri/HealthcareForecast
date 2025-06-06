import './src/style.css'
import { renderAdmissionsChart } from './components/charts.js'

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('admissionsChart').getContext('2d')
    renderAdmissionsChart(ctx)
})
