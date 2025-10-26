document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('expensesChart');
    if (!chartCanvas) return;

    const dataUrl = chartCanvas.getAttribute('data-url');

    fetch(dataUrl)
    .then(response => response.json())
    .then(data => {
        const labels = Object.keys(data);
        const expenses = Object.values(data);

        const ctx = chartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Expenses',
                    data: expenses,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }).catch(error => console.error('Error fetching expenses data:', error));
});
