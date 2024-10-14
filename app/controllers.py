import os
import joblib
import pandas as pd
from flask import request, session
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app import db
from app.models import Data, ModelResult, VisaPoints, UniCourse, User, Login, University, UserCoursePref, UserSession, CostOfLiving, OccupationList

# Define a path to store the model .pkl files in the ml folder
MODEL_PATH = os.path.join(os.getcwd(), 'ml')

if not os.path.exists(MODEL_PATH):
  os.makedirs(MODEL_PATH)  # Create the directory if it doesn't exist

# Check if the email and password combination is valid.
def check_login(email, password):
  user = User.query.filter_by(email=email).first()
  
  if user and check_password_hash(user.login.hashed_password, password):
    return True, user.user_role
  
  return False, None

def get_user_name():
  if 'username' in session:
    # Get the user from the database
    user = User.query.filter_by(email=session['username']).first()
    
    if user:
      # Return the first and last name of the user
      return user.first_name, user.last_name
  
  # Return None if the user is not found
  return None, None

# Register a new user
def register_user(data):
  # Ensure that no existing user with the same email exists
  existing_user = User.query.filter_by(email=data['email']).first()
  if existing_user is not None:
    return False

  # Hash the password
  hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

  # Create the user and login entries
  user = User(
    email=data['email'],
    first_name=data['first_name'],
    last_name=data['last_name'],
    user_role=data['user_role'],
    phone=data['phone'],
    edu_id=data.get('edu_id'),
    abn=data.get('abn'),
    street_address=data.get('street_address'),
    suburb=data.get('suburb'),
    state=data.get('state'),
    postcode=data.get('postcode')
  )

  login = Login(
    email=data['email'],
    password=data['password'],  # Optionally store the plain password
    hashed_password=hashed_password
  )

  # Commit both records to the database
  db.session.add(user)
  db.session.add(login)
  db.session.commit()

  return True

# Record the login time when a user logs in.
def record_login(email):
  login_time = datetime.now(timezone.utc)
  
  user_session = UserSession(email=email, login_time=login_time)
  db.session.add(user_session)
  db.session.commit()
  return login_time

# Update the logout time and time elapsed for a user session.
def record_logout(email):
  user_session = UserSession.query.filter_by(email=email).order_by(UserSession.login_time.desc()).first()
  
  if user_session:
    logout_time = datetime.now(timezone.utc)
    
    user_session.logout_time = logout_time
    user_session.time_elapsed = logout_time - user_session.login_time
    db.session.commit()

# Fetch all data from the 'data' table in the database and return it as a pandas DataFrame.
def get_data():
  data_records = Data.query.all()
  data_dict = {
    'occupation_pathway': [d.occupation_pathway for d in data_records],
    'location': [d.location for d in data_records],
    'commitment_regional': [d.commitment_regional for d in data_records],
    'state_nomination': [d.state_nomination for d in data_records],
    'course_duration': [d.course_duration for d in data_records],
    'course_cost': [d.course_cost for d in data_records],
    'cost_of_living': [d.cost_of_living for d in data_records],
    'visa_processing_time': [d.visa_processing_time for d in data_records],
    'visa_cost': [d.visa_cost for d in data_records],
    'approval_probability': [d.approval_probability for d in data_records],
    'recommended_visa': [d.recommended_visa for d in data_records]
  }
  df = pd.DataFrame(data_dict)
  return df

# Train the DecisionTreeClassifier using the data from the database, and save the model as a .pkl file.
def train_model(max_depth, criterion, test_size):
  # Fetch the data from the database
  df = get_data()

  # Separate features and target
  X = df.drop('recommended_visa', axis=1)
  y = df['recommended_visa']
  
  # Split the data into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
  
  # Train the decision tree model
  model = DecisionTreeClassifier(max_depth=max_depth, criterion=criterion, random_state=42)
  model.fit(X_train, y_train)
  
  # Evaluate the model
  accuracy = accuracy_score(y_test, model.predict(X_test))
  
  # Save the trained model to a .pkl file
  model_filename = os.path.join(MODEL_PATH, 'decision_tree_model.pkl')
  joblib.dump(model, model_filename)
  print(f"Model saved to {model_filename}")
  
  # Save the model result (accuracy) to the database
  model_result = ModelResult(
    model_type='DecisionTree',
    accuracy=accuracy
  )
  db.session.add(model_result)
  db.session.commit()

  return f"Model trained with accuracy: {accuracy:.2f}. Model saved successfully."

# Load the trained DecisionTreeClassifier model and use it to make predictions.
def predict_model(features):
  # Load the trained model from the .pkl file
  model_filename = os.path.join(MODEL_PATH, 'decision_tree_model.pkl')
  
  if not os.path.exists(model_filename):
    return "No trained model found"
  
  # Load the saved model
  model = joblib.load(model_filename)
  print(f"Model loaded from {model_filename}")
  
  # Make a prediction
  prediction = model.predict([features])
  return prediction[0]

def get_occupation_list(visa_189_eligible, visa_190_eligible, visa_491_eligible):
  if visa_189_eligible and not visa_190_eligible and not visa_491_eligible:
    # If eligible for 189 only
    return OccupationList.query.filter_by(type='MLTSSL').all()
  elif visa_189_eligible and visa_190_eligible and not visa_491_eligible:
    # If eligible for both 189 and 190
    return OccupationList.query.filter(OccupationList.type.in_(['MLTSSL', 'STSOL'])).all()
  else:
    # If eligible for all or visa 491
    return OccupationList.query.all()

def visa_points_calculator(data):
  points = 0
  
  # Age points calculation
  if data['age'] == '18-24' or data['age'] == '33-39':
    points += 25
  elif data['age'] == '25-32':
    points += 30
  elif data['age'] == '40-44':
    points += 15
  else:
    points += 0

  # English language level points
  if data['english_level'] == 'competent':
    points += 10
  elif data['english_level'] == 'proficient':
    points += 20
  elif data['english_level'] == 'superior':
    points += 30

  # Overseas employment points
  if data['overseas_employment'] == '0-2':
    points += 0
  elif data['overseas_employment'] == '3-4':
    points += 5
  elif data['overseas_employment'] == '5-7':
    points += 10
  elif data['overseas_employment'] == '>=8':
    points += 15

  # Australian employment points
  if data['australian_employment'] == '<1':
    points += 0
  elif data['australian_employment'] == '1-2':
    points += 5
  elif data['australian_employment'] == '3-4':
    points += 10
  elif data['australian_employment'] == '5-7':
    points += 15
  elif data['australian_employment'] == '>=8':
    points += 20

  # Education level points
  if data['education_level'] == 'doctorate':
    points += 20
  elif data['education_level'] == 'bachelors':
    points += 15
  elif data['education_level'] == 'diploma_or_trade':
    points += 10
  elif data['education_level'] == 'other_recognised':
    points += 5
  
  # Initialize all optional fields to prevent UnboundLocalError
  specialist_education = False
  australian_study = False
  professional_year = False
  community_language = False
  regional_study = False
  
  # Convert 'yes'/'no' to boolean
  def to_bool(value):
    return value.lower() == 'yes' if value else False

  # Specialist education qualification points
  if to_bool(data.get('specialist_education', 'no')):
    specialist_education = True
    points += 10

  # Australian study requirement points
  if to_bool(data.get('australian_study', 'no')):
    australian_study = True
    points += 5

  # Professional year in Australia points
  if to_bool(data.get('professional_year', 'no')):
    professional_year = True
    points += 5

  # Community language points
  if to_bool(data.get('community_language', 'no')):
    community_language = community_language
    points += 5

  # Regional study points
  if to_bool(data.get('regional_study', 'no')):
    regional_study = regional_study
    points += 5

  # Partner skills points
  if data['partner_skills'] == 'age_eng_skill':
    points += 10
  elif data['partner_skills'] == 'comp_eng':
    points += 5
  elif data['partner_skills'] == 'single_citizen_pr':
    points += 15
  else:
    points += 0
  
  # State nomination points
  if data['nomination'] == 'state':
    points += 5
  elif data['nomination'] == 'state_regional':
    points += 15
  else:
    points += 0
  
  # Visa eligibility logic
  visa_189_eligible = False
  visa_190_eligible = False
  visa_491_eligible = False
  
  if points >= 65:
    visa_189_eligible = True
    if data['nomination'] == 'state':
      visa_190_eligible = True
    elif data['nomination'] == 'state_regional':
      visa_491_eligible = True
      
  occupation_list = get_occupation_list(visa_189_eligible, visa_190_eligible, visa_491_eligible)
  
  # Save to database with username
  visa_points_entry = VisaPoints(
    username=data['username'],
    age=data['age'],
    english_level=data['english_level'],
    overseas_employment=data['overseas_employment'],
    australian_employment=data['australian_employment'],
    education_level=data['education_level'],
    specialist_education=specialist_education,
    australian_study=australian_study,
    professional_year=professional_year,
    community_language=community_language,
    regional_study=regional_study,
    partner_skills=data['partner_skills'],
    nomination=data['nomination'],
    points=points,
    visa_189_eligible=visa_189_eligible,
    visa_190_eligible=visa_190_eligible,
    visa_491_eligible=visa_491_eligible
  )

  db.session.add(visa_points_entry)
  db.session.commit()

  return points, visa_189_eligible, visa_190_eligible, visa_491_eligible, occupation_list

def process_visa_path(data):
  # Extract data from form submission
  educational_qualification = data.get('education_level')
  specialist_education = data.get('specialist_education')
  prof_year = data.get('proffesional_year', 'off')  # Default to 'off' if not checked
  course_duration = data.get('course_duration')
  regional_study = data.get('regional_study', 'off')  # Default to 'off' if not checked
  tuition_fee = data.get('tuition_fee')
  state = data.get('state')

  # Build the query
  query = UniCourse.query \
      .join(User, UniCourse.provider_id == User.email) \
      .join(University, UniCourse.univ_id == University.id) \
      .filter(University.state == state)

  # Level filter logic
  if educational_qualification == 'bachelor':
    query = query.filter(func.lower(UniCourse.level) == 'bachelor')
  elif educational_qualification == 'master':
    query = query.filter(func.lower(UniCourse.level).in_(['bachelor', 'master']))
  elif educational_qualification == 'doctorate':
    query = query.filter(func.lower(UniCourse.level).in_(['bachelor', 'master', 'doctorate']))

  # Specialist education filter logic
  if specialist_education != 'none':
    query = query.filter(func.lower(UniCourse.specialist_education) == specialist_education)
    
  # Tuition fee filter logic
  if tuition_fee == '<60k':
    query = query.filter(UniCourse.tuition_fee < 60000)
  elif tuition_fee == '60k-100k':
    query = query.filter(UniCourse.tuition_fee.between(60000, 100000))
  elif tuition_fee == '>100k':
    query = query.filter(UniCourse.tuition_fee > 100000)

  # Duration filter logic
  if course_duration == '2':
    query = query.filter(UniCourse.duration <= 2)
  elif course_duration == '4':
    query = query.filter(UniCourse.duration <= 4)
  elif course_duration == '6':
    query = query.filter(UniCourse.duration <= 6)

  # Professional year filter logic
  if prof_year == 'on':  # Checkbox was checked
    query = query.filter(UniCourse.prof_year == True)

  # Regional study filter logic
  if regional_study == 'on':  # Checkbox was checked
    query = query.filter(UniCourse.regional == True)

  # Execute the query to get recommended courses
  recommended_courses = query.all()
  
  # Add cost of living calculation for each course
  for course in recommended_courses:
    if course.regional:
      # If the course is regional, query the cost_of_living for the corresponding state and area = 'regional'
      cost_living_entry = CostOfLiving.query.filter_by(state=state, area='regional').first()
    else:
      # If the course is metro, query the cost_of_living for the corresponding state and area = 'metro'
      cost_living_entry = CostOfLiving.query.filter_by(state=state, area='metro').first()

    # Calculate the sum of rent, grocery, transportation, utilities, and entertainment
    if cost_living_entry:
      cost_of_living = (
        cost_living_entry.rent +
        cost_living_entry.grocery +
        cost_living_entry.transportation +
        cost_living_entry.utilities +
        cost_living_entry.entertainment
      )
      # Monthly & Annual cost of living
      course.cost_of_living = cost_of_living
      course.cost_of_living_annual = cost_of_living * 12
    else:
      course.cost_of_living = None
      course.cost_of_living_annual = None

  # Add points to each course based on the new function
  for course in recommended_courses:
    course.points = calculate_ref_points(course)

  sorted_courses = sorted(recommended_courses, key=lambda x: x.points, reverse=True)

  return sorted_courses

def calculate_ref_points(course):
  # Define points for levels
  level_points = {
    'bachelor': 1,
    'master': 2,
    'doctorate': 3
  }

  # Calculate points based on course attributes
  points = level_points.get(course.level.lower(), 0)  # Get points for level
  points += 1 if course.specialist_education != 'none' else 0  # Add 1 if specialist_education is not 'none'
  points += 1 if course.prof_year else 0  # Add 1 if professional year is True
  points += 1 if course.regional else 0  # Add 1 if regional is True

  return points

def save_user_course_pref(selected_courses, username):  
  print("Selected Courses:", selected_courses)
  print("Username:", username)
  
  # Create a list to store new entries to be added
  saved_courses = []
  
  for course_id in selected_courses:
    # Query the course data by course_id
    course = UniCourse.query.filter_by(id=course_id).first()

    if course:
      if course.regional:
        cost_living_entry = CostOfLiving.query.filter_by(state=course.university.state, area='regional').first()
      else:
        cost_living_entry = CostOfLiving.query.filter_by(state=course.university.state, area='metro').first()

      # Calculate cost_of_living and cost_of_living_annual
      cost_of_living = (
          cost_living_entry.rent +
          cost_living_entry.grocery +
          cost_living_entry.transportation +
          cost_living_entry.utilities +
          cost_living_entry.entertainment
      )
      cost_of_living_annual = cost_of_living * 12

      # Create a new entry for each selected course
      saved_course = UserCoursePref(
          username=username,
          course_id=course.id,
          cost_of_living=cost_of_living,
          cost_of_living_annual=cost_of_living_annual
      )
      # Append to the list of saved courses
      saved_courses.append(saved_course)

  if saved_courses:
    db.session.bulk_save_objects(saved_courses)
    db.session.commit()
  
def get_user_course_pref(username):
  if username:
    user_pref_courses = db.session.query(UserCoursePref, UniCourse, University) \
                      .join(UniCourse, UserCoursePref.course_id == UniCourse.id) \
                      .join(University, UniCourse.univ_id == University.id) \
                      .filter(UserCoursePref.username == username).all()
    
    return user_pref_courses
  
  return None

def get_user_visa_points(username):
  if username:
      visa_points = db.session.query(VisaPoints).filter(VisaPoints.username == username).all()
      
      return visa_points
  
  return None

def get_chart_admin():
  # Pie Chart Data (Total registered users by group)
  pie_labels = ['Applicants', 'Educational Institution', 'Migration Agencies']
  pie_values = [500, 200, 150]

  # Line Chart Data (Users logged in by group over the last 6 months)
  line_labels = ['April', 'May', 'June', 'July', 'August', 'September']
  line_values_applicants = [120, 130, 100, 90, 110, 115]
  line_values_institutions = [40, 45, 30, 35, 50, 48]
  line_values_agencies = [30, 25, 20, 18, 22, 19]

  # Stacked Bar Chart Data (Courses added in the last 6 months)
  bar_labels = ['April', 'May', 'June', 'July', 'August', 'September']
  bar_values_science = [15, 18, 12, 20, 25, 30]
  bar_values_technology = [10, 12, 8, 15, 22, 27]
  bar_values_engineering = [12, 14, 10, 18, 20, 25]
  bar_values_math = [8, 10, 6, 12, 15, 20]
  bar_values_ict = [9, 11, 7, 13, 16, 21]
  bar_values_others = [5, 6, 4, 8, 9, 10]

  return pie_labels, pie_values, line_labels, line_values_applicants, line_values_institutions, line_values_agencies, bar_labels, bar_values_science, bar_values_technology, bar_values_engineering, bar_values_math, bar_values_ict, bar_values_others

def get_chart_migrant():
  # Pie Chart Data (Applicants Completed Specialist Education Qualification)
  specialist_education_labels = ['yes', 'no']
  specialist_education_values = [300, 100]
  
  # Pie Chart Data (Applicants Met Australian Study Requirement)
  australian_study_labels = ['yes', 'no']
  australian_study_values = [200, 100]
  
  # Pie Chart Data (Applicants Completed Professional Year in Australia)
  professional_year_labels = ['yes', 'no']
  professional_year_values = [100, 100]
  
  # Pie Chart Data (Applicants Who Can Speak Community Language)
  community_language_labels = ['yes', 'no']
  community_language_values = [100, 200]
  
  # Pie Chart Data (Applicants Completed Regional Study)
  regional_study_labels = ['yes', 'no']
  regional_study_values = [100, 300]
  
  # Bar Chart Data (Applicants by Age Group)
  age_group_labels = ['18-24', '25-32', '33-39', '40-44', '>=45']
  age_group_values = [50, 100, 120, 200, 70]
  
  # Bar Chart Data (Applicants by English Language Level)
  english_level_labels = ['competent', 'proficient', 'superior']
  english_level_values = [50, 100, 120]
  
  # Bar Chart Data (Overseas Skilled Employment)
  overseas_employment_labels = ['0-1', '1-2', '3-4', '5-7', '>=8']
  overseas_employment_values = [50, 60, 70, 80, 90]
  
  # Bar Chart Data (Australian Skilled Employment)
  australian_employment_labels = ['0-1', '1-2', '3-4', '5-7', '>=8']
  australian_employment_values = [90, 80, 70, 60, 50]
  
  # Bar Chart Data (Highest Level of Education)
  education_level_labels = ['doctorate', 'bachelor', 'diploma_or_trade', 'other_recognised']
  education_level_values = [100, 80, 60, 40]
  
  return specialist_education_labels, specialist_education_values, australian_study_labels, australian_study_values, professional_year_labels, professional_year_values, community_language_labels, community_language_values, regional_study_labels, regional_study_values, age_group_labels, age_group_values, english_level_labels, english_level_values, overseas_employment_labels, overseas_employment_values, australian_employment_labels, australian_employment_values, education_level_labels, education_level_values

# Get all courses
def get_courses(username, user_role):
  if user_role == 'admin':
    courses = db.session.query(UniCourse, User.first_name, User.last_name, University) \
            .join(User, UniCourse.provider_id == User.email) \
            .join(University, UniCourse.univ_id == University.id) \
            .all()
  elif user_role == 'education':
    courses = db.session.query(UniCourse, User.first_name, User.last_name, University) \
            .join(User, UniCourse.provider_id == User.email) \
            .join(University, UniCourse.univ_id == University.id) \
            .filter(User.email == username) \
            .all()
  else:
    courses = []
  return courses

# Function to get a course by its ID
def get_course_by_id(course_id):
  return UniCourse.query.filter_by(id=course_id).first()

# Add new course to the database
def add_new_course(data):
  # Get and process the specialist education field
  specialist_education = data.get('specialist_education')

  # Capitalize first letter, except for "ICT" which is fully capitalized
  if specialist_education == 'ict':
    specialist_education = 'ICT'
  else:
    specialist_education = specialist_education.capitalize()
  
  # Ensure the data is cleaned and prepared before adding to the database
  course = UniCourse(
    course_num=data['course_num'],
    course_name=data['course_name'],
    univ_id=data['univ_id'],
    provider_id=data['username'],
    level=data['level'].capitalize(),  # Capitalize first letter
    specialist_education=specialist_education,
    prof_year=bool(data.get('prof_year')),
    duration=int(data['duration']),
    tuition_fee=float(data['tuition_fee']),
    regional=bool(data.get('regional'))
  )
  db.session.add(course)
  db.session.commit()
  
def update_course(data, course_id):
  # Find the course by ID
  course = UniCourse.query.filter_by(id=course_id).first()
  
  # Get and process the specialist education field
  specialist_education = data.get('specialist_education')

  # Capitalize first letter, except for "ICT" which is fully capitalized
  if specialist_education == 'ict':
    specialist_education = 'ICT'
  else:
    specialist_education = specialist_education.capitalize()

  # If the course is found, update its values
  if course:
    course.course_num = data['course_num']
    course.course_name = data['course_name']
    course.univ_id = data['univ_id']
    course.provider_id = data['username']
    course.level = data['level'].capitalize()  # Capitalize first letter
    course.specialist_education = specialist_education
    course.prof_year = bool(data.get('prof_year'))
    course.duration = int(data['duration'])
    course.tuition_fee = float(data['tuition_fee'])
    course.regional = bool(data.get('regional'))

    db.session.commit()

# Delete course
def delete_course(course_id):
  course = UniCourse.query.filter_by(id=course_id).first()
  # Log the course data for debugging
  print(f"Attempting to delete course with ID: {course_id}")
  
  if course:
    db.session.delete(course)
    db.session.commit()

# Function to get all universities
def get_universities():
  return University.query.all()

def get_university_by_id(university_id):
  return University.query.filter_by(id=university_id).first()

def add_new_university(data):
  university = University(
    university=data['university'],
    street=data.get('street'),
    suburb=data.get('suburb'),
    state=data['state'],
    postcode=data['postcode'],
    phone=data.get('phone'),
    email=data['email']
  )
  db.session.add(university)
  db.session.commit()

def update_university(data, university_id):
  university = University.query.filter_by(id=university_id).first()
  if university:
    university.university = data['university']
    university.street = data.get('street')
    university.suburb = data.get('suburb')
    university.state = data['state']
    university.postcode = data['postcode']
    university.phone = data.get('phone')
    university.email = data['email']
    db.session.commit()

def delete_university_by_id(university_id):
  university = University.query.filter_by(id=university_id).first()
  if university:
    db.session.delete(university)
    db.session.commit()