// Function to render the charts
function renderCharts(pieLabels, pieValues, barLabels, barValues) {
    // Pie Chart
    const ctxPie = document.getElementById('myPieChart').getContext('2d');
    const myPieChart = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: pieLabels,
            datasets: [{
                label: 'Pie Chart Example',
                data: pieValues,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        }
    });

    // Bar Chart
    const ctxBar = document.getElementById('myBarChart').getContext('2d');
    const myBarChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: barLabels,
            datasets: [
                {
                    label: 'Visa 189',
                    data: barValuesA,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Visa 190',
                    data: barValuesB,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Visa 491',
                    data: barValuesC,
                    backgroundColor: 'rgba(115, 227, 45, 0.2)',
                    borderColor: 'rgba(115, 227, 45, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true
        }
    });
}

// Ensure the charts are rendered as soon as the page is loaded
window.onload = function() {
    const pieLabels = window.pieLabels;
    const pieValues = window.pieValues;
    const barLabels = window.barLabels;
    const barValuesA = window.barValuesA;
    const barValuesB = window.barValuesB;
    const barValuesC = window.barValuesC;

    // Call the function to render the charts immediately
    renderCharts(pieLabels, pieValues, barLabels, barValuesA, barValuesB, barValuesC);
};
