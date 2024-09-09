from flask import Blueprint, render_template, request
from app.models import Data, db
from app.controllers import train_model, predict_model

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/train', methods=['GET', 'POST'])
def train():
	if request.method == 'POST':
		# Get user-provided settings from the form
		max_depth = int(request.form.get('max_depth'))
		criterion = request.form.get('criterion')
		test_size = float(request.form.get('test_size'))
		
		# Train the model with the provided settings
		message = train_model(max_depth=max_depth, criterion=criterion, test_size=test_size)
		
		# Fetch the data table after training
		data_entries = Data.query.all()
		
		# Show a success message and display the data table
		return render_template('training.html', message=message, data_entries=data_entries)
	
	# Fetch the data table if no form submission yet
	data_entries = Data.query.all()
	return render_template('training.html', data_entries=data_entries)

@main.route('/test', methods=['GET', 'POST'])
def test():
	if request.method == 'POST':
		# Fetch form data
		occupation_pathway = int(request.form.get('occupation_pathway'))
		location = int(request.form.get('location'))
		commitment_regional = int(request.form.get('commitment_regional'))
		state_nomination = int(request.form.get('state_nomination'))
		course_duration = int(request.form.get('course_duration'))
		course_cost = float(request.form.get('course_cost'))
		cost_of_living = float(request.form.get('cost_of_living'))
		visa_processing_time = int(request.form.get('visa_processing_time'))
		visa_cost = float(request.form.get('visa_cost'))
		approval_probability = float(request.form.get('approval_probability'))
		
		# Prepare data for prediction (same format as what the model expects)
		features = [
				occupation_pathway, location, commitment_regional, state_nomination, 
				course_duration, course_cost, cost_of_living, visa_processing_time, 
				visa_cost, approval_probability
		]
			
		# Get the prediction from the model (recommended_visa)
		prediction = predict_model(features)
		
		# Store the data and prediction in the database
		new_data = Data(
			occupation_pathway=occupation_pathway,
			location=location,
			commitment_regional=commitment_regional,
			state_nomination=state_nomination,
			course_duration=course_duration,
			course_cost=course_cost,
			cost_of_living=cost_of_living,
			visa_processing_time=visa_processing_time,
			visa_cost=visa_cost,
			approval_probability=approval_probability,
			recommended_visa=prediction
		)
		db.session.add(new_data)
		db.session.commit()

		# Pass the prediction (recommended_visa) to the template
		return render_template('test.html', prediction=prediction)

	return render_template('test.html')
