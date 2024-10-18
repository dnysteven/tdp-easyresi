// Function to create Pie Charts
function sePieChart(specialistEducationLabels, specialistEducationValues) {
	const ctx = document.getElementById('specialistEducationChart').getContext('2d');
	new Chart(ctx, {
		type: 'pie',
    data: {
      labels: specialistEducationLabels, 
      datasets: [{
        data: specialistEducationValues,
        backgroundColor: ['#48AAAD', '#3A43BA'], // Using the specified colors
		hoverOffset: 4
	}]

    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
        },
      }
    }
  });
}

// Function to create Pie Charts
function asrPieChart(australianStudyRequirementLabels, australianStudyRequirementValues) {
	const ctx = document.getElementById('australianStudyRequirementChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: australianStudyRequirementLabels,  
		datasets: [{
		  data: australianStudyRequirementValues,  
		  backgroundColor: ['#48AAAD', '#3A43BA'], // Using the specified colors
		  hoverOffset: 4
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
function pyPieChart(professionalYearLabels, professionalYearValues) {
	const ctx = document.getElementById('professionalYearChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: professionalYearLabels,  
		datasets: [{
		  data: professionalYearValues,  
		  backgroundColor: ['#48AAAD', '#3A43BA'], // Using the specified colors
		  hoverOffset: 4
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
function clPieChart(communityLanguageLabels, communityLanguageValues) {
	const ctx = document.getElementById('communityLanguageChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: communityLanguageLabels,  
		datasets: [{
		  data: communityLanguageValues,  
		  backgroundColor: ['#48AAAD', '#3A43BA'], // Using the specified colors
		  hoverOffset: 4
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
function rsPieChart(regionalStudyLabels, regionalStudyValues) {
	const ctx = document.getElementById('regionalStudyChart').getContext('2d');
	new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: regionalStudyLabels,  
		datasets: [{
		  data: regionalStudyValues,  
		  backgroundColor: ['#48AAAD', '#3A43BA'], // Using the specified colors
		  hoverOffset: 4
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
  function agBarChart(ageGroupLabels, ageGroupValues) {
	const ctx = document.getElementById('ageGroupChart').getContext('2d');
	new Chart(ctx, {
	  type: 'bar',
	  data: {
		labels: ageGroupLabels,
		datasets: [{
		  data: ageGroupValues,
		  backgroundColor: ['#48AAAD', '#3A43BA', '#6693FA', '#3B8132', '#95C8D8']
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
	function elBarChart(englishLevelLabels, englishLevelValues) {
		const ctx = document.getElementById('englishLevelChart').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: englishLevelLabels,
			datasets: [{
			  data: englishLevelValues,
			  backgroundColor: ['#48AAAD', '#3B8132', '#95C8D8']
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
	function oeBarChart(overseasEmploymentLabels, overseasEmploymentValues) {
		const ctx = document.getElementById('overseasEmploymentChart').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: overseasEmploymentLabels,
			datasets: [{
			  data: overseasEmploymentValues,
			  backgroundColor: ['#48AAAD', '#3A43BA', '#6693FA', '#3B8132', '#95C8D8']
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
	function aeBarChart(australianEmploymentLabels, australianEmploymentValues) {
		const ctx = document.getElementById('australianEmploymentChart').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: australianEmploymentLabels,
			datasets: [{
			  data: australianEmploymentValues,
			  backgroundColor: ['#48AAAD', '#3A43BA', '#6693FA', '#3B8132', '#95C8D8']
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
	function elBarChart(educationLevelLabels, ducationLevelValues) {
		const ctx = document.getElementById('educationLevelChart').getContext('2d');
		new Chart(ctx, {
		  type: 'bar',
		  data: {
			labels: educationLevelLabels,
			datasets: [{
			  data: ducationLevelValues,
			  backgroundColor: ['#48AAAD', '#3A43BA','#3B8132', '#95C8D8']
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
		  backgroundColor: ['#48AAAD','#3A43BA','#3B8132'],
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
			backgroundColor: ['#48AAAD'],
			borderColor: ['#48AAAD'],
			fill: false,
			tension: 0.1
		  },
		  {
			label: 'Educational Institutions',
			data: lineValuesInstitutions,
			backgroundColor: ['#3A43BA'],
			borderColor: ['#3A43BA'],
			fill: false,
			tension: 0.1
		  },
		  {
			label: 'Migration Agencies',
			data: lineValuesAgencies,
			backgroundColor: ['#3B8132'],
			borderColor: ['#3B8132'],
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
			backgroundColor: ['#48AAAD'],
			borderWidth: 1
		  },
		  {
			label: 'Technology',
			data: barValuesTechnology,
			backgroundColor: ['#3A43BA'],
			borderWidth: 1
		  },
		  {
			label: 'Engineering',
			data: barValuesEngineering,
			backgroundColor: ['#6693FA'],
			borderWidth: 1
		  },
		  {
			label: 'Mathematics',
			data: barValuesMath,
			backgroundColor: ['#3B8132'],
			borderWidth: 1
		  },
		  {
			label: 'ICT',
			data: barValuesICT,
			backgroundColor: ['#95C8D8'],
			borderWidth: 1
		  },
		  {
			label: 'Others',
			data: barValuesOthers,
			backgroundColor: ['#12C42C'],
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
    sePieChart(window.specialistEducationLabels, window.specialistEducationValues);
	}

		// Pie Chart for Australian Study Requirement
	if (window.australianStudyRequirementLabels && window.australianStudyRequirementValues) {
    asrPieChart(window.australianStudyRequirementLabels, window.australianStudyRequirementValues);
	}

		// Pie Chart for Professional Year
	if (window.professionalYearLabels && window.professionalYearValues) {
    pyPieChart(window.professionalYearLabels, window.professionalYearValues);
	}

		// Pie Chart for Community Language
	if (window.communityLanguageLabels && window.communityLanguageValues) {
    clPieChart(window.communityLanguageLabels, window.communityLanguageValues);
	}

		// Pie Chart for Regional Study
	if (window.regionalStudyLabels && window.regionalStudyValues) {
    rsPieChart(window.regionalStudyLabels, window.regionalStudyValues);
	}

		// Bar Chart for Age Groups
	if (window.ageGroupLabels && window.ageGroupValues) {
		agBarChart(window.ageGroupLabels, window.ageGroupValues);
	}

	// Bar Chart for English Levels
	if (window.englishLevelLabels && window.englishLevelValues) {
		elBarChart(window.englishLevelLabels, window.englishLevelValues);
	}

	// Bar Chart for Overseas Employment
	if (window.overseasEmploymentLabels && window.overseasEmploymentValues) {
		oeBarChart(window.overseasEmploymentLabels, window.overseasEmploymentValues);
	}

	// Bar Chart for Australian Employment
	if (window.australianEmploymentLabels && window.australianEmploymentValues) {
		aeBarChart(window.australianEmploymentLabels, window.australianEmploymentValues);
	}

	// Bar Chart for Education Levels
	if (window.educationLevelLabels && window.educationLevelValues) {
		elBarChart(window.educationLevelLabels, window.educationLevelValues);
	}	
});