from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models import Data, db, User, UserRole
from app.controllers import register_user, check_login, record_login, record_logout, train_model, predict_model, visa_points_calculator, process_visa_path, user_course_preferences, get_user_course_preferences, get_chart_admin, get_chart_migrant

main = Blueprint('main', __name__)

# Secret key for user session management
SECRET_KEY = 'tdp_easyresi_session'
main.secret_key = SECRET_KEY

@main.route('/login', methods=['GET', 'POST'])
def login():
	# Check if user is already logged in
	#if 'username' in session:
		#return redirect(url_for('main.index'))

	if request.method == 'POST':
		# Get username and password from the form
		email = request.form['email']
		password = request.form['password']
		
		# Get login success and user role from check_login
		success, user_role = check_login(email, password)
		
		if success:
			session['username'] = email
			session['user_role'] = user_role
			record_login(email)
			flash('Login successful!', 'success')
			return redirect(url_for('main.index'))
		else:
			flash('Login failed. Incorrect email or password.', 'danger')
			return redirect(url_for('main.login'))

	return render_template('login.html', header=True, footer=True)

@main.route('/logout')
def logout():
  record_logout(session['username'])
  session.clear()
  flash('You have been logged out.', 'success')
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
		data = {
			'email': request.form['email'],
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'password': request.form['password'],
			'phone': request.form['phone'],
			'user_role': request.form['user_role'],
			'edu_id': request.form.get('edu_id'),
			'abn': request.form.get('abn'),
			'street_address': request.form.get('street_address'),
			'suburb': request.form.get('suburb'),
			'state': request.form.get('state'),
			'postcode': request.form.get('postcode')
		}

		if register_user(data):
			flash('Registration successful! Please log in.', 'success')
			return redirect(url_for('main.login'))
		else:
			flash('Registration failed. Please try again.', 'danger')

	# Fetch user roles for the dropdown
	roles = UserRole.query.all()
	return render_template('register.html', header=True, footer=True, roles=roles)

@main.route('/')
def index():
	return render_template('index.html', header=True, footer=True)

@main.route('/189', methods=['GET'])
def visa_189():
	return render_template('189.html', header=True, footer=True)

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
	return render_template('training.html', header=True, footer=True, data_entries=data_entries)

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

	return render_template('test.html', header=True, footer=True,)

@main.route('/questionnaire', methods=['GET', 'POST'])
#@login_required
def questionnaire():
  if current_app.config['ENV'] == 'development':
    session['username'] = '104685155@student.swin.edu.au'
    
  username = session.get('username')
  if not username:
    return redirect(url_for('main.login'))
  
  if request.method == 'POST':
    data = request.form.to_dict()
    data['username'] = session['username']
    
    # Calculate points and eligibility
    points, visa_189_eligible, visa_190_eligible, visa_491_eligible = visa_points_calculator(data)
    
    session['points'] = points
    session['visa_189_eligible'] = visa_189_eligible
    session['visa_190_eligible'] = visa_190_eligible
    session['visa_491_eligible'] = visa_491_eligible
    session['completed_questionnaire'] = True
    
    return redirect(url_for('main.visa_points'))
  
  return render_template('questionnaire.html', header=True, footer=True)

@main.route('/visa_points', methods=['GET'])
#@login_required
def visa_points():
  if not session.get('completed_questionnaire'):
    return redirect(url_for('main.questionnaire'))  # Redirect if questionnaire not completed
  
  points = session.get('points')
  visa_189_eligible = session.get('visa_189_eligible', False)
  visa_190_eligible = session.get('visa_190_eligible', False)
  visa_491_eligible = session.get('visa_491_eligible', False)
  
  session.pop('completed_questionnaire', None)
  
  if not visa_189_eligible and not visa_190_eligible and not visa_491_eligible:
    session['eligible_for_path_to_visa'] = True
    
  return render_template('visa_points.html', header=True, footer=True,
                        points=points, visa_189_eligible=visa_189_eligible,
                        visa_190_eligible=visa_190_eligible, visa_491_eligible=visa_491_eligible)

@main.route('/path_to_visa', methods=['GET', 'POST'])
#@login_required
def path_to_visa():
	# Check if the user has accessed visa_points and is eligible for the Path to Visa page
	#if not session.get('eligible_for_path_to_visa'):
		#return redirect(url_for('main.index'))

	# Remove session flag after accessing the page to prevent further direct access

	if current_app.config['ENV'] == 'development':
		session['username'] = '104685155@student.swin.edu.au'

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

	return render_template('path_to_visa.html', header=True, footer=True)

@main.route('/recommendation', methods=['GET'])
#@login_required
def recommendation():
	# Check if user has submitted the form in path_to_visa.html
	if current_app.config['ENV'] == 'development':
		session['username'] = '104685155@student.swin.edu.au'

	username = session.get('username')
	if not username:
		return redirect(url_for('main.login'))

	if not session.get('submitted_path_to_visa'):
		return redirect(url_for('main.path_to_visa'))

	data = session.get('path_to_visa_data')
	recommended_courses = process_visa_path(data)
  
	# Clear session flag after accessing the page
	session.pop('submitted_path_to_visa', None)

	return render_template('recommendation.html', header=True, footer=True, recommended_courses=recommended_courses)

@main.route('/save_courses', methods=['POST'])
#@login_required
def save_courses():
	if current_app.config['ENV'] == 'development':
		session['username'] = '104685155@student.swin.edu.au'

	username = session.get('username')
	if not username:
		return redirect(url_for('main.login'))  

	username = session['username']
	selected_courses = request.form.getlist('save_courses')

	if selected_courses:
		# Call the function to save multiple courses at once
		user_course_preferences(username, selected_courses, request.form)
		flash(f"Successfully saved {len(selected_courses)} course(s).")
  
		return redirect(url_for('main.profile'))
	else:
		flash("No courses were selected.")

	return redirect(url_for('main.recommendation'))

@main.route('/profile', methods=['GET'])
#@login_required
def profile():
	if current_app.config['ENV'] == 'development':
		session['username'] = '104685155@student.swin.edu.au'

	username = session.get('username')
	if not username:
		return redirect(url_for('main.login'))
  
	# Retrieve user data from database
	username = session['username']
	user = User.query.filter_by(username=username).first()

	# Fetch the user's saved course preferences
	user_courses = get_user_course_preferences(username)

	return render_template('profile.html', header=True, footer=True, user=user, user_courses=user_courses)

# Route for the charts (admin_statistics)
@main.route('/admin_statistics')
def admin_statistics():
	pie_labels, pie_values, line_labels, line_values_applicants, line_values_institutions, \
  line_values_agencies, bar_labels, bar_values_science, bar_values_technology, bar_values_engineering, bar_values_math, bar_values_ict, bar_values_others = get_chart_admin()
  
  # Ensure that none of the variables are undefined or None
	pie_labels = pie_labels or []
	pie_values = pie_values or []
  
	line_labels = line_labels or []
	line_values_applicants = line_values_applicants or []
	line_values_institutions = line_values_institutions or []
	line_values_agencies = line_values_agencies or []

	bar_labels = bar_labels or []
	bar_values_science = bar_values_science or []
	bar_values_technology = bar_values_technology or []
	bar_values_engineering = bar_values_engineering or []
	bar_values_math = bar_values_math or []
	bar_values_ict = bar_values_ict or []
	bar_values_others = bar_values_others or []


	return render_template('admin_statistics.html', 
												header=False, footer=False,
												pie_labels=pie_labels, pie_values=pie_values, 
												line_labels=line_labels, line_values_applicants=line_values_applicants,
												line_values_institutions=line_values_institutions, line_values_agencies=line_values_agencies,
												bar_labels=bar_labels, bar_values_science=bar_values_science,
												bar_values_technology=bar_values_technology, bar_values_engineering=bar_values_engineering,
												bar_values_math=bar_values_math, bar_values_ict=bar_values_ict, bar_values_others=bar_values_others)


@main.route('/edu_statistics')
def edu_statistics():
	return render_template('edu_statistics.html')

@main.route('/migra_statistics')
def migra_statistics():
	# Get chart data from the controller
	line_labels, line_values_visa189, line_values_visa190, line_values_visa491 = get_chart_migrant()

	# Ensure that none of the variables are undefined or None
	line_labels = line_labels or []  # Default to an empty list if None
	line_values_visa189 = line_values_visa189 or []
	line_values_visa190 = line_values_visa190 or []
	line_values_visa491 = line_values_visa491 or []

	return render_template('migra_statistics.html', header=True, footer=True,
													line_labels=line_labels,
													line_values_visa189=line_values_visa189,
													line_values_visa190=line_values_visa190,
													line_values_visa491=line_values_visa491)