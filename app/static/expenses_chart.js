document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('expensesChart');
    if (!chartCanvas) return;

    const dataUrl = chartCanvas.getAttribute('data-url');
    const ctx = chartCanvas.getContext('2d');

    let charInstance = null;
    let chartType = localStorage.getItem('chartType') || 'bar';


    function renderChart(type, labels, expenses) {
    if (charInstance) {
        charInstance.destroy();
    }
    charInstance = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses',
                data: expenses,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: 'rgba(255,255,255,1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: type === 'bar',
            maintainAspectRatio: type === 'pie',
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Expenses by Category' }
            },
            scales: type === 'bar' ? {
                y: { beginAtZero: true }
            } : {}
        }
    });
}


    fetch(dataUrl)
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data);
            const expenses = Object.values(data);

            renderChart(chartType, labels, expenses);
           document.getElementById('button').addEventListener('click', function () {
                chartType = 'bar';
                localStorage.setItem('chartType', 'bar');
                renderChart(chartType, charInstance.data.labels, charInstance.data.datasets[0].data);
            });
            document.getElementById('button2').addEventListener('click', function () {
                chartType = 'pie';
                localStorage.setItem('chartType', 'pie');
                renderChart(chartType, charInstance.data.labels, charInstance.data.datasets[0].data);
            });

        })
        .catch(error => console.error('Error fetching data:', error));
});