import Chart from 'chart.js/auto'

const backend = 'http://127.0.0.1:5000'
export async function renderAdmissionsChart(ctx) {
    const res = await fetch(`${backend}/api/admissions/department`)
    const { labels, datasets } = await res.json()

    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: datasets.map(ds => ({
                label: ds.label,
                data: ds.data,
                fill: false,
                borderColor: randomColor(),
                tension: 0.2
            }))
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                x: { title: { display: true, text: 'Date' }},
                y: { title: { display: true, text: 'Admissions' }}
            }
        }
    })
}

function randomColor() {
    const hue = Math.floor(Math.random() * 360)
    return `hsl(${hue}, 70%, 50%)`
}
