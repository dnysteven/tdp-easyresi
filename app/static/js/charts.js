// Function to render the Pie Chart for registered users by groups
function renderPieChart(pieLabels, pieValues) {
    const ctxPie = document.getElementById('myPieChart').getContext('2d');
    const myPieChart = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: pieLabels,
            datasets: [{
                label: 'Total Registered Users',
                data: pieValues,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(94, 235, 52, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(94, 235, 52, 1)'
                ],
                borderWidth: 1
            }]
        }
    });
}

// Function to render the Line Chart for user logins
function renderLineChart(lineLabels, lineValuesApplicants, lineValuesInstitutions, lineValuesAgencies) {
    const ctxLine = document.getElementById('myLineChart').getContext('2d');
    const myLineChart = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: lineLabels, // Months
            datasets: [
                {
                    label: 'Applicants',
                    data: lineValuesApplicants,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Educational Institutions',
                    data: lineValuesInstitutions,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Migration Agencies',
                    data: lineValuesAgencies,
                    borderColor: 'rgba(94, 235, 52, 1)',
                    backgroundColor: 'rgba(94, 235, 52, 0.2)',
                    fill: false,
                    tension: 0.1
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

// Function to render the Bar Chart for courses added
function renderBarChart(barLabels, barValues) {
    const ctxBar = document.getElementById('myBarChart').getContext('2d');
    const myBarChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: barLabels, // Months
            datasets: [{
                label: 'Total Courses Added',
                data: barValues,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
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

// Wait for the DOM content to load before rendering the charts
document.addEventListener('DOMContentLoaded', function() {
    // Pie Chart
    renderPieChart(window.pieLabels, window.pieValues);

    // Line Chart
    renderLineChart(window.lineLabels, window.lineValuesApplicants, window.lineValuesInstitutions, window.lineValuesAgencies);

    // Bar Chart
    renderBarChart(window.barLabels, window.barValues);
});
