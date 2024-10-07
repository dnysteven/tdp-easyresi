import os
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Data, ModelResult, VisaPoints, UniCourse, User, Login, University, UserCoursePref, UserSession

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

  # Specialist education qualification points
  if 'specialist_education' in data and data['specialist_education'] == 'yes':
    specialist_education = True
    points += 10

  # Australian study requirement points
  if 'australian_study' in data and data['australian_study'] == 'yes':
    australian_study = True
    points += 5

  # Professional year in Australia points
  if 'professional_year' in data and data['professional_year'] == 'yes':
    professional_year = True
    points += 5

  # Community language points
  if 'community_language' in data and data['community_language'] == 'yes':
    community_language = True
    points += 5

  # Regional study points
  if 'regional_study' in data and data['regional_study'] == 'yes':
    regional_study = True
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
  
  # Convert 'yes'/'no' to boolean
  def to_bool(value):
    return value.lower() == 'yes'
  
  # Convert 'yes'/'no' to boolean for checkbox values
  specialist_education = to_bool(data.get('specialist_education', 'no'))
  australian_study = to_bool(data.get('australian_study', 'no'))
  professional_year = to_bool(data.get('professional_year', 'no'))
  community_language = to_bool(data.get('community_language', 'no'))
  regional_study = to_bool(data.get('regional_study', 'no'))
  
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

  return points, visa_189_eligible, visa_190_eligible, visa_491_eligible

def calculate_age(request):
  date_of_birth_str = request.form.get('date_of_birth')
  date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
  
  today = datetime.today()
  age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
  
  return date_of_birth, age

def process_visa_path(data):
  # Extract data from form submission
  educational_qualification = data.get('educational_qualification')
  specialist = data.get('specialist_education')
  professional_year = data.get('professional_year')
  course_duration = data.get('course_duration')
  regional = data.get('regional')
  course_fees = data.get('course_fees')
  
  # Convert course_fees into a list if it's comma-separated
  if course_fees:
    course_fees = course_fees.split(',')
  
  # Build the query with mandatory filters
  query = UniCourse.query \
    .join(User, UniCourse.provider_id == User.username) \
    .join(University, UniCourse.univ_id == University.id) \
    .filter(
      UniCourse.level == educational_qualification,
      UniCourse.specialist == bool(int(specialist)),
      UniCourse.prof_year == bool(int(professional_year)),
      UniCourse.duration == int(course_duration)
    )

  # Add the regional filter if it's checked
  if regional:
    query = query.filter_by(regional=True)

  # Add the course fees filter if any checkboxes were selected
  if course_fees:
    query = query.filter(UniCourse.fee_points.in_(course_fees))

  recommended_courses = query.all()
  
  # Add points to each course based on the new function
  for course in recommended_courses:
    course.points = calculate_ref_points(course)

  return recommended_courses

def calculate_ref_points(course):
  # Define points for levels
  level_points = {
    'bachelor': 1,
    'master': 2,
    'doctorate': 3
  }

  # Calculate points based on course attributes
  points = level_points.get(course.level.lower(), 0)  # Get points for level
  points += 1 if course.specialist else 0  # Add 1 if specialist is True
  points += 1 if course.prof_year else 0  # Add 1 if prof_year is True
  points += 1 if course.regional else 0  # Add 1 if regional is True

  return points


def user_course_preferences(username, selected_courses, form_data):
  # Loop through selected courses and save the course preferences
  for course_id in selected_courses:
    course_num = form_data.get(f'course_num_{course_id}')
    course_name = form_data.get(f'course_name_{course_id}')
    provider_name = form_data.get(f'provider_name_{course_id}')
    university_name = form_data.get(f'university_name_{course_id}')
    university_address = form_data.get(f'university_address_{course_id}')
    state = form_data.get(f'state_{course_id}')
    postcode = form_data.get(f'postcode_{course_id}')
    duration = form_data.get(f'duration_{course_id}')
    tuition_fee = form_data.get(f'tuition_fee_{course_id}')

    # Create a new UserCoursePref object
    user_pref = UserCoursePref(
      username=username,
      course_num=course_num,  # Save course_num instead of course_id
      course_name=course_name,
      provider_name=provider_name,
      university_name=university_name,
      university_address=university_address,
      state=state,
      postcode=postcode,
      duration=int(duration),
      tuition_fee=float(tuition_fee)
    )
    
    # Add the course to the session
    db.session.add(user_pref)

  # Commit the changes to the database in one transaction
  db.session.commit()
  
def get_user_course_preferences(username):
  # Query the user_course_pref table based on the username
  return UserCoursePref.query.filter_by(username=username).all()

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
  specialist_education_labels = ['Completed', 'Not Completed']
  specialist_education_values = [300, 100]
  
  return specialist_education_labels, specialist_education_values
