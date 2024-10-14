from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models import Data, db, User, UserRole, UserGroup, CourseAdded, UserLogin, UniCourse
from app.controllers import register_user, get_user_name, check_login, record_login, record_logout, train_model, predict_model, visa_points_calculator, process_visa_path, save_user_course_pref, get_user_course_pref, get_user_visa_points, get_chart_migrant, get_courses, get_course_by_id, add_new_course, update_course, delete_course, get_universities, add_new_university, update_university, get_university_by_id, delete_university_by_id

main = Blueprint('main', __name__)

# Secret key for user session management
SECRET_KEY = 'tdp_easyresi_session'
main.secret_key = SECRET_KEY

@main.route('/')
def index():
  user_first_name, user_last_name = get_user_name()
  return render_template('index.html', header=True, footer=True,
                        user_first_name=user_first_name, user_last_name=user_last_name)

@main.route('/login', methods=['GET', 'POST'])
def login():
	# Check if user is already logged in
	if 'username' in session:
		return redirect(url_for('main.index'))

	user_first_name, user_last_name = get_user_name()

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

	return render_template('login.html', header=True, footer=True,
                        user_first_name=user_first_name, user_last_name=user_last_name)

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
  
	user_first_name, user_last_name = get_user_name()
  
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
	return render_template('register.html', header=True, footer=True, roles=roles,
                        user_first_name=user_first_name, user_last_name=user_last_name)

@main.route('/profile', methods=['GET'])
@login_required
def profile():
	# Retrieve user data from database
	username = session.get('username')
	user_role = session.get('user_role')
	user = User.query.filter_by(email=username).first()

	user_first_name, user_last_name = get_user_name()

	if user_role == 'applicant':
		user_courses = get_user_course_pref(username)
		user_visa_points = get_user_visa_points(username)
	else:
		user_courses = None
		user_visa_points = None

	# # Fetch specific data based on user role
	# if user.user_role == 'admin':
	# 	# Fetch admin-specific data
	# 	user_profile = fetch_admin_data()
	# elif user.user_role == 'applicant':
	# 	# Fetch applicant-specific data
	# 	user_profile = fetch_applicant_data()
	# elif user.user_role == 'agency':
	# 	# Fetch agency-specific data
	# 	user_profile = fetch_agency_data()
	# elif user.user_role == 'education':
	# 	# Fetch education-specific data
	# 	user_profile = fetch_education_data()
	# else:
	# 	user_profile = None

	# Fetch the user's saved course preferences

	return render_template('profile.html', header=True, footer=True,
                        user=user, user_first_name=user_first_name, user_last_name=user_last_name,
                        user_courses=user_courses, user_visa_points=user_visa_points)

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
@login_required
def questionnaire():
  user_first_name, user_last_name = get_user_name()
  
  if request.method == 'POST':
    username = session.get('username')
    
    # Save the form data to the session
    form_data = {
      'username': username,
			'age': request.form.get('age'),
			'english_level': request.form.get('english_level'),
			'overseas_employment': request.form.get('overseas_employment'),
			'australian_employment': request.form.get('australian_employment'),
			'education_level': request.form.get('education_level'),
			'specialist_education': request.form.get('specialist_education'),
			'australian_study': request.form.get('australian_study'),
			'professional_year': request.form.get('professional_year'),
			'community_language': request.form.get('community_language'),
			'regional_study': request.form.get('regional_study'),
			'partner_skills': request.form.get('partner_skills'),
			'nomination': request.form.get('nomination'),
		}
    
    session['form_data'] = form_data
    session['completed_questionnaire'] = True
    
    return redirect(url_for('main.visa_points'))
  
  return render_template('questionnaire.html', header=True, footer=True,
                        user_first_name=user_first_name, user_last_name=user_last_name)

@main.route('/visa_points', methods=['GET'])
@login_required
def visa_points():
  # Redirect if questionnaire not completed
  if not session.get('completed_questionnaire'):
    return redirect(url_for('main.questionnaire'))
  
  user_first_name, user_last_name = get_user_name()
  
  # Call the visa_points_calculator
  form_data = session.get('form_data')
  points, visa_189_eligible, visa_190_eligible, visa_491_eligible, occupation_list = visa_points_calculator(form_data)
  
  session.pop('form_data', None)
  session.pop('completed_questionnaire', None)
  
  # if not visa_189_eligible and not visa_190_eligible and not visa_491_eligible:
  #   session['eligible_for_path_to_visa'] = True
    
  return render_template('visa_points.html', header=True, footer=True,
                        user_first_name=user_first_name, user_last_name=user_last_name,
                        points=points, visa_189_eligible=visa_189_eligible,
                        visa_190_eligible=visa_190_eligible, visa_491_eligible=visa_491_eligible,
                        occupation_list=occupation_list)

@main.route('/path_to_visa', methods=['GET', 'POST'])
@login_required
def path_to_visa():
  user_first_name, user_last_name = get_user_name()
  
  if request.method == 'POST':
    # Collect the form data from path_to_visa.html
    data = {
			'education_level': request.form['education_level'],
			'specialist_education': request.form['specialist_education'],
			'professional_year': request.form.get('professional_year', 'off') == 'on',
			'regional_study': request.form.get('regional_study', 'off') == 'on',
			'course_duration': request.form['course_duration'],
			'tuition_fee': request.form['tuition_fee'],
			'state': request.form['state']
		}
    
    # Save the form data to session for use in the redirected page
    session['path_to_visa_data'] = data
    
    # Redirect to the recommendation route
    return redirect(url_for('main.recommendation'))
  
  return render_template('path_to_visa.html', header=True, footer=True,
                        user_first_name=user_first_name, user_last_name=user_last_name)

@main.route('/recommendation', methods=['GET'])
@login_required
def recommendation():
  user_first_name, user_last_name = get_user_name()
  
  # Retrieve the form data from the session
  data = session.get('path_to_visa_data', None)
  
  # Check if user has submitted the form in path_to_visa.html
  if not data:
    return redirect(url_for('main.path_to_visa'))
  
  # Pass the form data to the controller to get recommended courses
  recommended_courses = process_visa_path(data)
  
  # Clear session flag after accessing the page
  session.pop('path_to_visa_data', None)
  
  return render_template('recommendation.html', header=True, footer=True,
                        user_first_name=user_first_name, user_last_name=user_last_name,
                        recommended_courses=recommended_courses)

@main.route('/user_course_pref', methods=['POST'])
@login_required
def user_course_pref():
	selected_courses = request.form.getlist('user_courses_pref')
	username = session.get('username')

	selected_courses = [int(course_id) for course_id in selected_courses]

	# print("Selected Courses:", selected_courses)
	# print("Username:", username)
	
	if selected_courses:
		save_user_course_pref(selected_courses, username)
	
	return redirect(url_for('main.index'))

# Route for the charts (admin_statistics)
@main.route('/admin_statistics')
def admin_statistics():
    # Query for pie chart data (User Groups)
    user_groups = UserGroup.query.all()
    pie_labels = [group.group_name for group in user_groups]
    pie_values = [group.total_users for group in user_groups]

    # Query for line chart data (User Logins by Month)
    line_labels = ['April', 'May', 'June', 'July', 'August', 'September']
    logins_applicants = UserLogin.query.filter_by(group_name='Applicants').all()
    logins_institutions = UserLogin.query.filter_by(group_name='Educational Institution').all()
    logins_agencies = UserLogin.query.filter_by(group_name='Migration Agencies').all()
    
    # Extract data for each group (for the last 6 months)
    line_values_applicants = [login.total_logins for login in logins_applicants]
    line_values_institutions = [login.total_logins for login in logins_institutions]
    line_values_agencies = [login.total_logins for login in logins_agencies]

    # Query for stacked bar chart data (Courses Added by Month)
    bar_labels = ['April', 'May', 'June', 'July', 'August', 'September']
    courses_science = CourseAdded.query.filter_by(category_name='Science').all()
    courses_technology = CourseAdded.query.filter_by(category_name='Technology').all()
    courses_engineering = CourseAdded.query.filter_by(category_name='Engineering').all()
    courses_math = CourseAdded.query.filter_by(category_name='Math').all()
    courses_ict = CourseAdded.query.filter_by(category_name='ICT').all()
    courses_others = CourseAdded.query.filter_by(category_name='Others').all()

    bar_values_science = [course.total_courses for course in courses_science]
    bar_values_technology = [course.total_courses for course in courses_technology]
    bar_values_engineering = [course.total_courses for course in courses_engineering]
    bar_values_math = [course.total_courses for course in courses_math]
    bar_values_ict = [course.total_courses for course in courses_ict]
    bar_values_others = [course.total_courses for course in courses_others]

    return render_template('admin_statistics.html',
													pie_labels=pie_labels, pie_values=pie_values,
													line_labels=line_labels,
													line_values_applicants=line_values_applicants,
													line_values_institutions=line_values_institutions,
													line_values_agencies=line_values_agencies,
													bar_labels=bar_labels, 
													bar_values_science=bar_values_science,
													bar_values_technology=bar_values_technology,
													bar_values_engineering=bar_values_engineering,
													bar_values_math=bar_values_math,
													bar_values_ict=bar_values_ict,
													bar_values_others=bar_values_others)
    
@main.route('/edu_statistics')
def edu_statistics():
	return render_template('edu_statistics.html')

@main.route('/migra_statistics')
def migra_statistics():
	# Get chart data from the controller
	specialist_education_labels, specialist_education_values, australian_study_labels, australian_study_values, professional_year_labels, professional_year_values, community_language_labels, community_language_values, regional_study_labels, regional_study_values, english_level_labels, english_level_values, overseas_employment_labels, overseas_employment_values, australian_employment_labels, australian_employment_values, education_level_labels, education_level_values = get_chart_migrant()

	# Ensure that none of the variables are undefined or None
	specialist_education_labels = specialist_education_labels or []
	specialist_education_values = specialist_education_values or []
	australian_study_labels = australian_study_labels or []
	australian_study_values = australian_study_values or []
	professional_year_labels = professional_year_labels or []
	professional_year_values = professional_year_values or []
	community_language_labels = community_language_labels or []
	community_language_values = community_language_values or []
	regional_study_labels = regional_study_labels or []
	regional_study_values = regional_study_values or []
	english_level_labels = english_level_labels or []
	english_level_values = english_level_values or []
	overseas_employment_labels = overseas_employment_labels or []
	overseas_employment_values = overseas_employment_values or []
	australian_employment_labels = australian_employment_labels or []
	australian_employment_values = australian_employment_values or []
	education_level_labels = education_level_labels or []
	education_level_values = education_level_values or []

	return render_template(
        'migra_statistics.html', header=True, footer=True,
							specialist_education_labels=specialist_education_labels,
							specialist_education_values=specialist_education_values,
							australian_study_labels=australian_study_labels,
							australian_study_values=australian_study_values,
							professional_year_labels=professional_year_labels,
							professional_year_values=professional_year_values,
							community_language_labels=community_language_labels,
							community_language_values=community_language_values,
							regional_study_labels=regional_study_labels,
							regional_study_values=regional_study_values,
							english_level_labels=english_level_labels,
							english_level_values=english_level_values,
							overseas_employment_labels=overseas_employment_labels,
							overseas_employment_values=overseas_employment_values,
							australian_employment_labels=australian_employment_labels, 
							australian_employment_values=australian_employment_values,
							education_level_labels=education_level_labels,
							education_level_values=education_level_values
)

@main.route('/applicant_profile')
def applicant_profile():
	return render_template('applicant_profile.html', header=True, footer=True)

@main.route('/edu_profile')
def edu_profile():
	return render_template('edu_profile.html', header=True, footer=True)

@main.route('/agent_profile')
def agent_profile():
	return render_template('agent_profile.html', header=True, footer=True)

@main.route('/courses')
@login_required
def courses():
  username = session.get('username')
  role = session.get('user_role')
  user_first_name, user_last_name = get_user_name()
  
  courses = get_courses(username, role)
  return render_template('courses.html', user_first_name=user_first_name, user_last_name=user_last_name, header=True, footer=True, courses=courses)

# Route for adding/editing courses via manage_courses.html
@main.route('/manage_course', methods=['GET', 'POST'])
@login_required
def manage_course():
  username = session.get('username')
  user_first_name, user_last_name = get_user_name()
  
  course_id = request.args.get('course_id')
  course = None
  universities = get_universities()
  
  if request.method == 'POST':
    data = request.form
    
    data = dict(data)
    data['username'] = username
    
    if course_id:
      update_course(data, course_id)
    else:
      add_new_course(data)
    
    return redirect(url_for('main.courses'))
  
  if course_id:
    course = get_course_by_id(course_id)
  
  return render_template('manage_courses.html', header=True, footer=True, user_first_name=user_first_name, user_last_name=user_last_name, course=course, universities=universities)

@main.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
	delete_course(course_id)

	return redirect(url_for('main.courses'))

@main.route('/universities')
@login_required
def universities():
  username = session.get('username')
  role = session.get('user_role')
  user_first_name, user_last_name = get_user_name()
  universities = get_universities()
  
  return render_template('university.html', user_first_name=user_first_name, user_last_name=user_last_name, header=True, footer=True, universities=universities)

@main.route('/manage_university', methods=['GET', 'POST'])
@login_required
def manage_university():
	username = session.get('username')
	role = session.get('user_role')
	user_first_name, user_last_name = get_user_name()

	university_id = request.args.get('university_id')
	university = None

	if request.method == 'POST':
		data = request.form
		if university_id:
			update_university(data, university_id)
		else:
			add_new_university(data)
		return redirect(url_for('main.universities'))

	if university_id:
		university = get_university_by_id(university_id)

	return render_template('manage_university.html',  user_first_name=user_first_name, user_last_name=user_last_name, header=True, footer=True, university=university)

@main.route('/delete_university/<int:university_id>', methods=['POST'])
@login_required
def delete_university(university_id):
	delete_university_by_id(university_id)
	return redirect(url_for('main.universities'))