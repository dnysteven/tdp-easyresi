from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models import Data, db, User, UserRole, Login, VisaPoints
from werkzeug.security import generate_password_hash, check_password_hash
from app.controllers import train_model, predict_model, visa_points_calculator, calculate_age, process_visa_path, user_course_preferences, get_user_course_preferences

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

@main.route('/questionnaire', methods=['GET', 'POST'])
#@login_required
def questionnaire():
  if current_app.config['ENV'] == 'development':
    session['username'] = 'dnysteven'
    
  username = session.get('username')
  if not username:
    return redirect(url_for('main.login'))
  
  if request.method == 'POST':
    date_of_birth, age = calculate_age(request)
    
    form = {
      'username': session['username'],
			'date_of_birth': date_of_birth,
			'age': age,
			'english_language': request.form.get('english_language'),
			'overseas_employment': int(request.form.get('overseas_employment')),
			'australian_employment': int(request.form.get('australian_employment')),
			'education_level': request.form.get('education_level'),
			'specialist_education': request.form.get('specialist_education'),
			'australian_study': request.form.get('australian_study'),
			'professional_year': request.form.get('professional_year'),
			'community_language': request.form.get('community_language'),
			'regional_study': request.form.get('regional_study'),
			'partner_skills': request.form.get('partner_skills'),
			'state_nomination': request.form.get('state_nomination'),
			'regional_nomination': request.form.get('regional_nomination')
		}
    
    result = visa_points_calculator(form)
    
    session['visa_189_points'] = result['visa_189_points']
    session['visa_190_points'] = result['visa_190_points']
    session['visa_491_points'] = result['visa_491_points']
    session['visa_189_eligible'] = result['visa_189_eligible']
    session['visa_190_eligible'] = result['visa_190_eligible']
    session['visa_491_eligible'] = result['visa_491_eligible']
    session['completed_questionnaire'] = True  # Mark the form as completed
    return redirect(url_for('main.visa_points'))
  
  return render_template('questionnaire.html')

@main.route('/visa_points', methods=['GET'])
#@login_required
def visa_points():
  if not session.get('completed_questionnaire'):
    return redirect(url_for('main.questionnaire'))  # Redirect if questionnaire not completed
  
  # visa_189_points = session.get('visa_189_points')
  # visa_190_points = session.get('visa_190_points')
  # visa_491_points = session.get('visa_491_points')
  visa_189_eligible = session.get('visa_189_eligible', False)
  visa_190_eligible = session.get('visa_190_eligible', False)
  visa_491_eligible = session.get('visa_491_eligible', False)
  
  if not visa_189_eligible and not visa_190_eligible and not visa_491_eligible:
    session['eligible_for_path_to_visa'] = True
    
  return render_template('visa_points.html', visa_189_eligible=visa_189_eligible, visa_190_eligible=visa_190_eligible, visa_491_eligible=visa_491_eligible)

@main.route('/path_to_visa', methods=['GET', 'POST'])
#@login_required
def path_to_visa():
	# Check if the user has accessed visa_points and is eligible for the Path to Visa page
	#if not session.get('eligible_for_path_to_visa'):
		#return redirect(url_for('main.index'))

	# Remove session flag after accessing the page to prevent further direct access

	if current_app.config['ENV'] == 'development':
		session['username'] = 'dnysteven'

	username = session.get('username')
	if not username:
		return redirect(url_for('main.login'))
  
	session.pop('eligible_for_path_to_visa', None)

	if request.method == 'POST':
		data = request.form.to_dict()
		data['course_fees'] = ','.join(request.form.getlist('course_fees'))  # Store course fees as comma-separated string

		# Set session flag to allow access to recommendation.html
		session['submitted_path_to_visa'] = True
		session['path_to_visa_data'] = data

		return redirect(url_for('main.recommendation'))

	return render_template('path_to_visa.html')

@main.route('/recommendation', methods=['GET'])
#@login_required
def recommendation():
	# Check if user has submitted the form in path_to_visa.html
	if current_app.config['ENV'] == 'development':
		session['username'] = 'dnysteven'

	username = session.get('username')
	if not username:
		return redirect(url_for('main.login'))

	if not session.get('submitted_path_to_visa'):
		return redirect(url_for('main.path_to_visa'))

	data = session.get('path_to_visa_data')
	recommended_courses = process_visa_path(data)
  
	# Clear session flag after accessing the page
	session.pop('submitted_path_to_visa', None)

	return render_template('recommendation.html', recommended_courses=recommended_courses)

@main.route('/save_courses', methods=['POST'])
#@login_required
def save_courses():
	if current_app.config['ENV'] == 'development':
		session['username'] = 'dnysteven'

	username = session.get('username')
	if not username:
		return redirect(url_for('main.login'))  

	username = session['username']
	selected_courses = request.form.getlist('save_courses')

	if selected_courses:
		# Call the function to save multiple courses at once
		user_course_preferences(username, selected_courses, request.form)
		flash(f"Successfully saved {len(selected_courses)} course(s).")
	else:
		flash("No courses were selected.")

	return redirect(url_for('main.recommendation'))

@main.route('/profile', methods=['GET'])
#@login_required
def profile():
	if current_app.config['ENV'] == 'development':
		session['username'] = 'dnysteven'

	username = session.get('username')
	if not username:
		return redirect(url_for('main.login'))
  
	# Retrieve user data from database
	username = session['username']
	user = User.query.filter_by(username=username).first()

	# Fetch the user's saved course preferences
	user_courses = get_user_course_preferences(username)

	return render_template('profile.html', user=user, user_courses=user_courses)

@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	# Process the data for both Pie and Bar charts
	# Pie Chart Data
	pie_labels = ['Eligible', 'Not Eligible']
	pie_values = [70, 30]

	# Bar Chart Data
	bar_labels = ['January', 'February', 'March', 'April', 'May']
	bar_values_category_A = [12, 19, 3, 5, 2]
	bar_values_category_B = [14, 16, 4, 7, 3]
	bar_values_category_C = [10, 14, 8, 6, 4]

	# Pass the data to the HTML template
	return render_template('dashboard.html', pie_labels=pie_labels, pie_values=pie_values,
                        bar_labels=bar_labels, bar_values_A=bar_values_category_A,
                        bar_values_B=bar_values_category_B, bar_values_C=bar_values_category_C)

@main.route('/edu_statistics')
def edu_statistics():
	return render_template('edu_statistics.html')