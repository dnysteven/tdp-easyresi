// Function to create Pie Charts
function renderPieChart(specialistEducationLabels, specialistEducationValues) {
	const ctx = document.getElementById('specialistEducationChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: specialistEducationLabels, 
		datasets: [{
		  data: specialistEducationValues,
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

// Function to create Pie Charts
function renderPieChart(australianStudyRequirementLabels, australianStudyRequirementValues) {
	const ctx = document.getElementById('australianStudyRequirementChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: australianStudyRequirementLabels,  
		datasets: [{
		  data: australianStudyRequirementValues,  
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
  
// Function to create Pie Charts
function renderPieChart(professionalYearLabels, professionalYearValues) {
	const ctx = document.getElementById('professionalYearChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: professionalYearLabels,  
		datasets: [{
		  data: professionalYearValues,  
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

// Function to create Pie Charts
function renderPieChart(communityLanguageLabels, communityLanguageValues) {
	const ctx = document.getElementById('communityLanguageChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: communityLanguageLabels,  
		datasets: [{
		  data: communityLanguageValues,  
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

// Function to create Pie Charts
function renderPieChart(regionalStudyLabels, regionalStudyValues) {
	const ctx = document.getElementById('regionalStudyChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: regionalStudyLabels,  
		datasets: [{
		  data: regionalStudyValues,  
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
  function renderBarChart(ageGroupLabels, ageGroupValues) {
	const ctx = document.getElementById('ageGroupChart').getContext('2d');
	new Chart(ctx, {
	  type: 'bar',
	  data: {
		labels: ageGroupLabels,
		datasets: [{
		  data: ageGroupValues,
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
  
    // Function to create Bar Charts
	function renderBarChart(englishLevelLabels, englishLevelValues) {
		const ctx = document.getElementById('englishLevelChart').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: englishLevelLabels,
			datasets: [{
			  data: englishLevelValues,
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

	  // Function to create Bar Charts
	function renderBarChart(overseasEmploymentLabels, overseasEmploymentValues) {
		const ctx = document.getElementById('overseasEmploymentChar').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: overseasEmploymentLabels,
			datasets: [{
			  data: overseasEmploymentValues,
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

	  // Function to create Bar Charts
	function renderBarChart(australianEmploymentLabels, australianEmploymentValues) {
		const ctx = document.getElementById('australianEmploymentChart').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: australianEmploymentLabels,
			datasets: [{
			  data: australianEmploymentValues,
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

	  // Function to create Bar Charts
	function renderBarChart(educationLevelLabels, ducationLevelValues) {
		const ctx = document.getElementById('educationLevelChart').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: educationLevelLabels,
			datasets: [{
			  data: ducationLevelValues,
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

		// Pie Chart for Specialist Education
	if (window.specialistEducationLabels && window.specialistEducationValues) {
    renderPieChart(window.specialistEducationLabels, window.specialistEducationValues);
	}

		// Pie Chart for Australian Study Requirement
	if (window.australianStudyRequirementLabels && window.australianStudyRequirementValues) {
    renderPieChart(window.australianStudyRequirementLabels, window.australianStudyRequirementValues);
	}

		// Pie Chart for Professional Year
	if (window.professionalYearLabels && window.professionalYearValues) {
    renderPieChart(window.professionalYearLabels, window.professionalYearValues);
	}

		// Pie Chart for Community Language
	if (window.communityLanguageLabels && window.communityLanguageValues) {
    renderPieChart(window.communityLanguageLabels, window.communityLanguageValues);
	}

		// Pie Chart for Regional Study
	if (window.regionalStudyLabels && window.regionalStudyValues) {
    renderPieChart(window.regionalStudyLabels, window.regionalStudyValues);
	}

		// Bar Chart for Age Groups
	if (window.ageGroupLabels && window.ageGroupValues) {
		renderBarChart(window.ageGroupLabels, window.ageGroupValues);
	}

	// Bar Chart for English Levels
	if (window.englishLevelLabels && window.englishLevelValues) {
		renderBarChart(window.englishLevelLabels, window.englishLevelValues);
	}

	// Bar Chart for Overseas Employment
	if (window.overseasEmploymentLabels && window.overseasEmploymentValues) {
		renderBarChart(window.overseasEmploymentLabels, window.overseasEmploymentValues);
	}

	// Bar Chart for Australian Employment
	if (window.australianEmploymentLabels && window.australianEmploymentValues) {
		renderBarChart(window.australianEmploymentLabels, window.australianEmploymentValues);
	}

	// Bar Chart for Education Levels
	if (window.educationLevelLabels && window.educationLevelValues) {
		renderBarChart(window.educationLevelLabels, window.educationLevelValues);
	}	
});