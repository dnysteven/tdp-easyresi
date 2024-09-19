import os
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime
from app import db
from app.models import Data, ModelResult, VisaPoints

# Define a path to store the model .pkl files in the ml folder
MODEL_PATH = os.path.join(os.getcwd(), 'ml')

if not os.path.exists(MODEL_PATH):
  os.makedirs(MODEL_PATH)  # Create the directory if it doesn't exist

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
  
  # Age points (this example uses hypothetical ranges)
  if 18 <= data['age'] <= 25:
    points += 25
  elif 26 <= data['age'] <= 32:
    points += 30
  elif 33 <= data['age'] <= 39:
    points += 25
  elif 40 <= data['age'] <= 44:
    points += 15

  # English language level points
  if data['english_language'] == 'competent':
    points += 10
  elif data['english_language'] == 'proficient':
    points += 20
  elif data['english_language'] == 'superior':
    points += 30

  # Overseas skilled employment points
  if data['overseas_employment'] >= 9:
    points += 15
  elif data['overseas_employment'] >= 6:
    points += 10
  elif data['overseas_employment'] >= 3:
    points += 5

  # Australian skilled employment points
  if data['australian_employment'] >= 9:
    points += 20
  elif data['australian_employment'] >= 6:
    points += 15
  elif data['australian_employment'] >= 3:
    points += 10

  # Education level points
  if data['education_level'] == 'doctorate':
    points += 20
  elif data['education_level'] == 'bachelors':
    points += 15
  elif data['education_level'] == 'diploma_trade':
    points += 10
  elif data['education_level'] == 'other_recognised':
    points += 5

  # Specialist education qualification points
  if data['specialist_education'] == 'yes':
    points += 10

  # Australian study requirement points
  if data['australian_study'] == 'yes':
    points += 10

  # Professional year in Australia points
  if data['professional_year'] == 'yes':
      points += 10

  # Community language points
  if data['community_language'] == 'yes':
    points += 10

  # Regional study points
  if data['regional_study'] == 'yes':
    points += 10

  # Partner skills points
  if data['partner_skills'] == 'age_eng_skill':
    points += 10
  elif data['partner_skills'] == 'comp_eng':
    points += 5
  elif data['partner_skills'] == 'single_citizen_pr':
    points += 15
  
  # Calculate points for visa 189
  visa_189_points = points
  
  # Check if eligible for visa 189
  visa_189_eligible = visa_189_points >= 65

  # State nomination points (for visa 190)
  state_nomination_points = 0
  if data['state_nomination'] == 'yes':
    state_nomination_points = 5
    points += 5
  visa_190_points = visa_189_points + state_nomination_points  # Adding state nomination points

  # Check if eligible for visa 190 (visa 189 points >= 65 AND state nomination > 0)
  visa_190_eligible = visa_189_points >= 65 and state_nomination_points > 0

  # Regional nomination points (for visa 491)
  regional_nomination_points = 0
  if data['regional_nomination'] == 'yes':
    regional_nomination_points = 15
    points += 15
  visa_491_points = visa_189_points + regional_nomination_points  # Adding regional nomination points

  # Check if eligible for visa 491 (visa 189 points >= 65 AND regional nomination > 0)
  visa_491_eligible = visa_189_points >= 65 and regional_nomination_points > 0
  
  # Save to database with username
  visa_points_entry = VisaPoints(
    username=data['username'],
    age=data['age'],
    english_language=data['english_language'],
    overseas_employment=data['overseas_employment'],
    australian_employment=data['australian_employment'],
    education_level=data['education_level'],
    specialist_education=data['specialist_education'],
    australian_study=data['australian_study'],
    professional_year=data['professional_year'],
    community_language=data['community_language'],
    regional_study=data['regional_study'],
    partner_skills=data['partner_skills'],
    state_nomination=data['state_nomination'],
    regional_nomination=data['regional_nomination'],
    visa_189_points=visa_189_points,
    visa_190_points=visa_190_points,
    visa_491_points=visa_491_points,
    visa_189_eligible=visa_189_eligible,
    visa_190_eligible=visa_190_eligible,
    visa_491_eligible=visa_491_eligible,
  )

  db.session.add(visa_points_entry)
  db.session.commit()

  return {
    'visa_189_points': visa_189_points,
    'visa_190_points': visa_190_points,
    'visa_491_points': visa_491_points,
    'visa_189_eligible': visa_189_eligible,
    'visa_190_eligible': visa_190_eligible,
    'visa_491_eligible': visa_491_eligible
  }

def calculate_age(request):
  date_of_birth_str = request.form.get('date_of_birth')
  date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d')
  
  today = datetime.today()
  age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
  
  return date_of_birth, age

def process_visa_path(data):
  # Extract data from form submission
  educational_qualification = data.get('educational_qualification')
  specialist_education = data.get('specialist_education')
  professional_year = data.get('professional_year')
  study_work_regional = data.get('study_work_regional')
  course_duration = data.get('course_duration')
  course_fees = data.get('course_fees')
  location = data.get('location')

  # Process the data here (e.g., save to database or perform calculations)
  # You can perform any necessary processing or validation here.
  
  # Example: Log the form data (replace this with your actual logic)
  print(f"Educational Qualification: {educational_qualification}")
  print(f"Specialist Education: {specialist_education}")
  print(f"Professional Year: {professional_year}")
  print(f"Study and Work in Regional Australia: {study_work_regional}")
  print(f"Course Duration: {course_duration} years")
  print(f"Maximum Course Fees: {course_fees}")
  print(f"Location: {location}")