// Function to create Pie Charts
function createPieChart(canvasId, labels, data) {
	const ctx = document.getElementById(canvasId).getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: labels,
		datasets: [{
		  data: data,
		  backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
		  hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
		}]
	  },
	  options: {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
		  legend: {
			position: 'bottom',
		  }
		}
	  }
	});
  }
  
  // Function to create Bar Charts
  function createBarChart(canvasId, labels, data) {
	const ctx = document.getElementById(canvasId).getContext('2d');
	new Chart(ctx, {
	  type: 'bar',
	  data: {
		labels: labels,
		datasets: [{
		  label: 'Count',
		  data: data,
		  backgroundColor: '#36A2EB',
		  borderColor: '#36A2EB',
		  borderWidth: 1
		}]
	  },
	  options: {
		responsive: true,
		maintainAspectRatio: false,
		scales: {
		  x: {
			beginAtZero: true
		  },
		  y: {
			beginAtZero: true
		  }
		},
		plugins: {
		  legend: {
			display: false
		  }
		}
	  }
	});
  }
  
  // Function to render the Pie Chart for registered users by groups
  function renderPieChart(pieLabels, pieValues) {
	const ctxPie = document.getElementById('myPieChart').getContext('2d');
	new Chart(ctxPie, {
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
	  },
	  options: {
		responsive: true
	  }
	});
  }
  
  // Function to render the Line Chart for user logins
  function renderLineChart(lineLabels, lineValuesApplicants, lineValuesInstitutions, lineValuesAgencies) {
	const ctxLine = document.getElementById('myLineChart').getContext('2d');
	new Chart(ctxLine, {
	  type: 'line',
	  data: {
		labels: lineLabels,
		datasets: [
		  {
			label: 'Applicants',
			data: lineValuesApplicants,
			borderColor: 'rgba(255, 99, 132)',
			backgroundColor: 'rgba(255, 99, 132)',
			fill: false,
			tension: 0.1
		  },
		  {
			label: 'Educational Institutions',
			data: lineValuesInstitutions,
			borderColor: 'rgba(54, 162, 235)',
			backgroundColor: 'rgba(54, 162, 235)',
			fill: false,
			tension: 0.1
		  },
		  {
			label: 'Migration Agencies',
			data: lineValuesAgencies,
			borderColor: 'rgba(94, 235, 52)',
			backgroundColor: 'rgba(94, 235, 52)',
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
  
  // Function to render the Stacked Bar Chart for categories
  function renderStackedBarChart(barLabels, barValuesScience, barValuesTechnology, barValuesEngineering, barValuesMath, barValuesICT, barValuesOthers) {
	const ctxBar = document.getElementById('myBarChart').getContext('2d');
	new Chart(ctxBar, {
	  type: 'bar',
	  data: {
		labels: barLabels,
		datasets: [
		  {
			label: 'Science',
			data: barValuesScience,
			backgroundColor: 'rgba(255, 99, 132)',
			borderColor: 'rgba(255, 99, 132)',
			borderWidth: 1
		  },
		  {
			label: 'Technology',
			data: barValuesTechnology,
			backgroundColor: 'rgba(54, 162, 235)',
			borderColor: 'rgba(54, 162, 235)',
			borderWidth: 1
		  },
		  {
			label: 'Engineering',
			data: barValuesEngineering,
			backgroundColor: 'rgba(235, 64, 52)',
			borderColor: 'rgba(235, 64, 52)',
			borderWidth: 1
		  },
		  {
			label: 'Mathematics',
			data: barValuesMath,
			backgroundColor: 'rgba(153, 102, 255)',
			borderColor: 'rgba(153, 102, 255)',
			borderWidth: 1
		  },
		  {
			label: 'ICT',
			data: barValuesICT,
			backgroundColor: 'rgba(255, 159, 64)',
			borderColor: 'rgba(255, 159, 64)',
			borderWidth: 1
		  },
		  {
			label: 'Others',
			data: barValuesOthers,
			backgroundColor: 'rgba(18, 196, 44)',
			borderColor: 'rgba(18, 196, 44)',
			borderWidth: 1
		  }
		]
	  },
	  options: {
		scales: {
		  x: {
			stacked: true
		  },
		  y: {
			stacked: true,
			beginAtZero: true
		  }
		},
		responsive: true
	  }
	});
  }
  
  // Function to render the Line Chart for Visa Applications
  function renderVisaLineChart(lineLabels, lineValuesVisa189, lineValuesVisa190, lineValuesVisa491) {
	const ctxLine = document.getElementById('visaLineChart').getContext('2d');
	new Chart(ctxLine, {
	  type: 'line',
	  data: {
		labels: lineLabels,
		datasets: [
		  {
			label: 'Visa 189 Applications',
			data: lineValuesVisa189,
			borderColor: 'rgba(255, 99, 132)',
			backgroundColor: 'rgba(255, 99, 132)',
			fill: false,
			tension: 0.1
		  },
		  {
			label: 'Visa 190 Applications',
			data: lineValuesVisa190,
			borderColor: 'rgba(54, 162, 235)',
			backgroundColor: 'rgba(54, 162, 235)',
			fill: false,
			tension: 0.1
		  },
		  {
			label: 'Visa 491 Applications',
			data: lineValuesVisa491,
			borderColor: 'rgba(94, 235, 52)',
			backgroundColor: 'rgba(94, 235, 52)',
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
  
	// Stacked Bar Chart for categories
	if (window.barLabels && window.barValuesScience && window.barValuesTechnology && window.barValuesEngineering && window.barValuesMath && window.barValuesICT && window.barValuesOthers) {
	  renderStackedBarChart(window.barLabels, window.barValuesScience, window.barValuesTechnology, window.barValuesEngineering, window.barValuesMath, window.barValuesICT, window.barValuesOthers);
	}
  
	// Line Chart for Visa Applicants
	if (window.lineLabels && window.lineValuesVisa189 && window.lineValuesVisa190 && window.lineValuesVisa491) {
	  renderVisaLineChart(window.lineLabels, window.lineValuesVisa189, window.lineValuesVisa190, window.lineValuesVisa491);
	}
  });
  