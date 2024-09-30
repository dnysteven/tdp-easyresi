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
					'rgba(255, 99, 132)',
					'rgba(54, 162, 235)',
					'rgba(94, 235, 52)'
				],
				borderColor: [
					'rgba(255, 99, 132)',
					'rgba(54, 162, 235)',
					'rgba(94, 235, 52)'
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

// Function to render the Line Chart for Visa Applications
function renderVisaLineChart(lineLabels, lineValuesVisa189, lineValuesVisa190, lineValuesVisa191) {
	const ctxLine = document.getElementById('visaLineChart').getContext('2d');
	const visaLineChart = new Chart(ctxLine, {
		type: 'line',
		data: {
			labels: lineLabels, // Months
			datasets: [
				{
					label: 'Visa 189 Applications',
					data: lineValuesVisa189,
					borderColor: 'rgba(255, 99, 132, 1)',
					backgroundColor: 'rgba(255, 99, 132, 0.2)',
					fill: false,
					tension: 0.1
				},
				{
					label: 'Visa 190 Applications',
					data: lineValuesVisa190,
					borderColor: 'rgba(54, 162, 235, 1)',
					backgroundColor: 'rgba(54, 162, 235, 0.2)',
					fill: false,
					tension: 0.1
				},
				{
					label: 'Visa 191 Applications',
					data: lineValuesVisa191,
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
					beginAtZero: true,
					title: {
						display: true,
						text: 'Number of Applicants'
					}
				},
				x: {
					title: {
						display: true,
						text: 'Months'
					}
				}
			},
			responsive: true
		}
	});
}

// Wait for the DOM content to load before rendering the charts
document.addEventListener('DOMContentLoaded', function() {
	// Pie Chart
	if (window.pieLabels && window.pieValues) {
		renderPieChart(window.pieLabels, window.pieValues);
	}

	// Line Chart for user logins
	if (window.lineLabels && window.lineValuesApplicants && window.lineValuesInstitutions && window.lineValuesAgencies) {
		renderLineChart(window.lineLabels, window.lineValuesApplicants, window.lineValuesInstitutions, window.lineValuesAgencies);
	}

	// Bar Chart for courses added
	if (window.barLabels && window.barValues) {
		renderBarChart(window.barLabels, window.barValues);
	}

	// Line Chart for Visa Applicants
	if (window.lineLabels && window.lineValuesVisa189 && window.lineValuesVisa190 && window.lineValuesVisa191) {
		renderVisaLineChart(window.lineLabels, window.lineValuesVisa189, window.lineValuesVisa190, window.lineValuesVisa191);
	}
});
