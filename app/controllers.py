import os
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from app import db
from app.models import Data, ModelResult

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
