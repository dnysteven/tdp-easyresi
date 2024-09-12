from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Data, User, UserRole, Login, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.controllers import train_model, predict_model

main = Blueprint('main', __name__)

# Secret key for user session management
SECRET_KEY = 'tdp_easyresi_session'
main.secret_key = SECRET_KEY

@main.route('/login', methods=['GET', 'POST'])
def login():
	# Check if user is already logged in
	if 'username' in session:
		return redirect(url_for('main.index'))

	if request.method == 'POST':
		# Get username and password from the form
		username = request.form.get('username')
		password = request.form.get('password')

		# Fetch user from the login table
		user_login = Login.query.filter_by(username=username).first()

		if user_login and check_password_hash(user_login.hashed_password, password):
			# If the password matches, store user info in session and redirect to index
			session['username'] = username
			return redirect(url_for('main.index'))
		else:
			# Invalid credentials
			message = "Invalid username or password"
			return render_template('login.html', message=message)

	return render_template('login.html')

@main.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('main.login'))

def login_required(f):
	def wrap(*args, **kwargs):
		if 'username' not in session:
			return redirect(url_for('main.login'))
		return f(*args, **kwargs)
	wrap.__name__ = f.__name__
	return wrap

@main.route('/register', methods=['GET', 'POST'])
def register():
  # Check if user is already logged in
	if 'username' in session:
		return redirect(url_for('main.index'))
  
	if request.method == 'POST':
		# Get form data
		username = request.form.get('username')
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		email = request.form.get('email')
		phone = request.form.get('phone')
		user_role = request.form.get('user_role')
		password = request.form.get('password')

		# Check if username already exists
		existing_user = User.query.filter_by(username=username).first()
		if existing_user:
			message = "Username already exists. Please choose another one."
			roles = UserRole.query.all()
			return render_template('registration.html', message=message, roles=roles)

		# Create a new user entry in the users table
		new_user = User(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email,
			phone=phone,
			user_role=user_role
		)
		db.session.add(new_user)

		# Hash the password and save it to the login table
		hashed_password = generate_password_hash(password)
		new_login = Login(
			username=username,
			password=password,
			hashed_password=hashed_password
		)
		db.session.add(new_login)

		# Commit changes to the database
		db.session.commit()

		# Redirect to a success page or homepage after registration
		return redirect(url_for('main.index'))

	# Fetch user roles for the dropdown
	roles = UserRole.query.all()
	return render_template('registration.html', roles=roles)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/189', methods=['GET'])
def visa_189():
	return render_template('189.html')

@main.route('/train', methods=['GET', 'POST'])
# @login_required
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
# @login_required
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
