from app import db

class UserRole(db.Model):
	__tablename__ = 'user_role'

	user_role = db.Column(db.String(20), primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(255), nullable=False)

	def __init__(self, user_role, name, description):
		self.user_role = user_role
		self.name = name
		self.description = description


class User(db.Model):
	__tablename__ = 'users'

	username = db.Column(db.String(50), primary_key=True) # Username as primary key
	first_name = db.Column(db.String(50), nullable=False) # User first name
	last_name = db.Column(db.String(50), nullable=False) # User last name
	email = db.Column(db.String(100), nullable=False) # User email
	phone = db.Column(db.String(20), nullable=False) # User phone number
	user_role = db.Column(db.String(20), db.ForeignKey('user_role.user_role'), nullable=False) # e.g., IT, Engineering, etc.

	# Define relationship with UserRole
	role = db.relationship('UserRole', backref='users')
	
	# Define relationship with Login
	login = db.relationship('Login', back_populates='user')

	def __init__(self, username, first_name, last_name, email, phone, user_role):
		self.username = username
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.phone = phone
		self.user_role = user_role


class Login(db.Model):
	__tablename__ = 'login'

	username = db.Column(db.String(50), db.ForeignKey('users.username'), primary_key=True)
	password = db.Column(db.String(255), nullable=False)
	hashed_password = db.Column(db.String(255), nullable=False)

	# Define relationship with User
	user = db.relationship('User', back_populates='login')

	def __init__(self, username, password, hashed_password):
		self.username = username
		self.password = password
		self.hashed_password = hashed_password

class Data(db.Model):
	__tablename__ = 'data'

	id = db.Column(db.Integer, primary_key=True)
	occupation_pathway = db.Column(db.Integer, nullable=False)  # e.g., IT, Engineering, etc.
	location = db.Column(db.Integer, nullable=False)  # e.g., SA metro, VIA metro
	commitment_regional = db.Column(db.Integer, nullable=False)  # Binary (Yes/No)
	state_nomination = db.Column(db.Integer, nullable=False)  # Binary (Yes/No)
	course_duration = db.Column(db.Integer, nullable=False)  # Duration in years
	course_cost = db.Column(db.Float, nullable=False)  # Cost of the course in AUD
	cost_of_living = db.Column(db.Float, nullable=False)  # Cost of living in AUD
	visa_processing_time = db.Column(db.Integer, nullable=False)  # Visa processing time in months
	visa_cost = db.Column(db.Float, nullable=False)  # Cost of visa in AUD
	approval_probability = db.Column(db.Float, nullable=False)  # Probability of visa approval (0-1)
	recommended_visa = db.Column(db.String(10), nullable=False)  # Predicted visa type (e.g., '189', '190')

	def __init__(self, occupation_pathway, location, commitment_regional, state_nomination, course_duration, course_cost, cost_of_living, visa_processing_time, visa_cost, approval_probability, recommended_visa):
		self.occupation_pathway = occupation_pathway
		self.location = location
		self.commitment_regional = commitment_regional
		self.state_nomination = state_nomination
		self.course_duration = course_duration
		self.course_cost = course_cost
		self.cost_of_living = cost_of_living
		self.visa_processing_time = visa_processing_time
		self.visa_cost = visa_cost
		self.approval_probability = approval_probability
		self.recommended_visa = recommended_visa


class ModelResult(db.Model):
	__tablename__ = 'model_result'

	id = db.Column(db.Integer, primary_key=True)
	model_type = db.Column(db.String(50), nullable=False)  # e.g., 'DecisionTree'
	accuracy = db.Column(db.Float, nullable=False)  # Accuracy of the model
	created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp when the model was trained

	def __init__(self, model_type, accuracy):
		self.model_type = model_type
		self.accuracy = accuracy
  
class VisaPoints(db.Model):
    __tablename__ = 'visa_points'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer, nullable=False)
    english_language = db.Column(db.String(20), nullable=False)
    overseas_employment = db.Column(db.Integer, nullable=False)
    australian_employment = db.Column(db.Integer, nullable=False)
    education_level = db.Column(db.String(50), nullable=False)
    specialist_education = db.Column(db.String(3), nullable=False)  # Yes or No
    australian_study = db.Column(db.String(3), nullable=False)  # Yes or No
    professional_year = db.Column(db.String(3), nullable=False)  # Yes or No
    community_language = db.Column(db.String(3), nullable=False)  # Yes or No
    regional_study = db.Column(db.String(3), nullable=False)  # Yes or No
    partner_skills = db.Column(db.String(50), nullable=False)  # Age, English and Skill Criteria

    def __init__(self, age, english_language, overseas_employment, australian_employment, education_level, specialist_education, australian_study, professional_year, community_language, regional_study, partner_skills):
        self.age = age
        self.english_language = english_language
        self.overseas_employment = overseas_employment
        self.australian_employment = australian_employment
        self.education_level = education_level
        self.specialist_education = specialist_education
        self.australian_study = australian_study
        self.professional_year = professional_year
        self.community_language = community_language
        self.regional_study = regional_study
        self.partner_skills = partner_skills