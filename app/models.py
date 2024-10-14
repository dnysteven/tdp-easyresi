from app import db
from datetime import datetime, timezone

class UserRole(db.Model):
	__tablename__ = 'user_role'

	user_role = db.Column(db.String(20), primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(255), nullable=False)

	# Relationship to User
	users = db.relationship('User', backref='role', lazy=True)

	def __init__(self, user_role, name, description):
		self.user_role = user_role
		self.name = name
		self.description = description


class User(db.Model):
	__tablename__ = 'users'

	email = db.Column(db.String(255), primary_key=True)
	first_name = db.Column(db.String(255), nullable=False)
	last_name = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(20), nullable=False)
	user_role = db.Column(db.String(50), db.ForeignKey('user_role.user_role'), nullable=False)
	edu_id = db.Column(db.String(50), nullable=True)
	abn = db.Column(db.String(50), nullable=True)
	street_address = db.Column(db.String(255), nullable=True)
	suburb = db.Column(db.String(255), nullable=True)
	state = db.Column(db.String(3), nullable=True)
	postcode = db.Column(db.String(4), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

	# Define relationship with Other model
	login = db.relationship('Login', backref='user', uselist=False, lazy=True)
	courses = db.relationship('UniCourse', backref='provider', lazy=True)
	user_course_prefs = db.relationship('UserCoursePref', backref='user', lazy=True)

	def __init__(self, email, first_name, last_name, phone, user_role, edu_id=None, abn=None, street_address=None, suburb=None, state=None, postcode=None):
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.phone = phone
		self.user_role = user_role
		self.edu_id = edu_id
		self.abn = abn
		self.street_address = street_address
		self.suburb = suburb
		self.state = state
		self.postcode = postcode

class Login(db.Model):
	__tablename__ = 'login'

	email = db.Column(db.String(255), db.ForeignKey('users.email'), primary_key=True)
	password = db.Column(db.String(255), nullable=False)
	hashed_password = db.Column(db.String(255), nullable=False)

	def __init__(self, email, password, hashed_password):
		self.email = email
		self.password = password
		self.hashed_password = hashed_password

class UserSession(db.Model):
	__tablename__ = 'user_sessions'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), db.ForeignKey('users.email'), nullable=False)
	login_time = db.Column(db.DateTime, nullable=False)
	logout_time = db.Column(db.DateTime, nullable=True)
	time_elapsed = db.Column(db.Interval, nullable=True)

	def __init__(self, email, login_time):
		self.email = email
		self.login_time = login_time

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

class OccupationList(db.Model):
	__tablename__ = 'occupation_list'

	id = db.Column(db.Integer, primary_key=True)
	occupation = db.Column(db.String(255), nullable=False)
	anzsco = db.Column(db.String(6), nullable=False)
	type = db.Column(db.String(6), nullable=False)

	def __init__(self, occupation, anzsco, type):
		self.occupation = occupation
		self.anzsco = anzsco
		self.type = type

class VisaPoints(db.Model):
	__tablename__ = 'visa_points'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), db.ForeignKey('users.email'), nullable=False)
	age = db.Column(db.String(50), nullable=False)
	english_level = db.Column(db.String(50), nullable=False)
	overseas_employment = db.Column(db.String(50), nullable=False)
	australian_employment = db.Column(db.String(50), nullable=False)
	education_level = db.Column(db.String(50), nullable=False)
	specialist_education = db.Column(db.Boolean, nullable=False, default=False)
	australian_study = db.Column(db.Boolean, nullable=False, default=False)
	professional_year = db.Column(db.Boolean, nullable=False, default=False)
	community_language = db.Column(db.Boolean, nullable=False, default=False)
	regional_study = db.Column(db.Boolean, nullable=False, default=False)
	partner_skills = db.Column(db.String(50), nullable=False)
	nomination = db.Column(db.String(50), nullable=False)
	points = db.Column(db.Integer, nullable=False)
	visa_189_eligible = db.Column(db.Boolean, nullable=False, default=False)
	visa_190_eligible = db.Column(db.Boolean, nullable=False, default=False)
	visa_491_eligible = db.Column(db.Boolean, nullable=False, default=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

	user = db.relationship('User', backref='visa_points')

	def __init__(self, username, age, english_level, overseas_employment, australian_employment, 
							education_level, specialist_education, australian_study, professional_year, 
							community_language, regional_study, partner_skills, nomination, points, 
							visa_189_eligible, visa_190_eligible, visa_491_eligible):
		self.username = username
		self.age = age
		self.english_level = english_level
		self.overseas_employment = overseas_employment
		self.australian_employment = australian_employment
		self.education_level = education_level
		self.specialist_education = specialist_education
		self.australian_study = australian_study
		self.professional_year = professional_year
		self.community_language = community_language
		self.regional_study = regional_study
		self.partner_skills = partner_skills
		self.nomination = nomination
		self.points = points
		self.visa_189_eligible = visa_189_eligible
		self.visa_190_eligible = visa_190_eligible
		self.visa_491_eligible = visa_491_eligible
  
class University(db.Model):
	__tablename__ = 'university'

	id = db.Column(db.Integer, primary_key=True)
	university = db.Column(db.String(100), nullable=False)
	street = db.Column(db.String(100), nullable=True)
	suburb = db.Column(db.String(100), nullable=False)
	state = db.Column(db.String(3), nullable=False)
	postcode = db.Column(db.String(4), nullable=False)
	phone = db.Column(db.String(15), nullable=False)
	email = db.Column(db.String(100), nullable=False)

	# Relationship with UniCourse
	courses = db.relationship('UniCourse', backref='university', lazy=True)

	def __init__(self, university, street, suburb, state, postcode, phone, email):
		self.university = university
		self.street = street
		self.suburb = suburb
		self.state = state
		self.postcode = postcode
		self.phone = phone
		self.email = email
  
class UniCourse(db.Model):
	__tablename__ = 'uni_course'

	id = db.Column(db.Integer, primary_key=True)
	course_num = db.Column(db.String(50), unique=True, nullable=False)
	course_name = db.Column(db.String(150), nullable=False)
	provider_id = db.Column(db.String(50), db.ForeignKey('users.email'), nullable=False)  # ForeignKey to User
	univ_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)  # ForeignKey to University
	level = db.Column(db.String(50), nullable=False)  # Bachelor, Master, Doctorate
	specialist_education = db.Column(db.String(50), nullable=False)  # Specialist options: science, technology, etc.
	prof_year = db.Column(db.Boolean, default=False)  # Professional year program
	duration = db.Column(db.Integer, nullable=False)  # Course duration in years
	tuition_fee = db.Column(db.Float, nullable=False)  # Fee range (<60k, 60k-100k, >100k)
	regional = db.Column(db.Boolean, default=False)  # Regional study
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	# Define relationship with Other model
	user_course_prefs = db.relationship('UserCoursePref', backref='course', lazy=True)

	def __init__(self, course_num, course_name, provider_id, univ_id, level, specialist_education, prof_year, duration, tuition_fee, regional):
		self.course_num = course_num
		self.course_name = course_name
		self.provider_id = provider_id
		self.univ_id = univ_id
		self.level = level
		self.specialist_education = specialist_education
		self.prof_year = prof_year
		self.duration = duration
		self.tuition_fee = tuition_fee
		self.regional = regional

class UserCoursePref(db.Model):
	__tablename__ = 'user_course_pref'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), db.ForeignKey('users.email', ondelete="CASCADE"), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('uni_course.id', ondelete="CASCADE"), nullable=False)
	cost_of_living = db.Column(db.Float, nullable=False)
	cost_of_living_annual = db.Column(db.Float, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	def __init__(self, username, course_id, cost_of_living, cost_of_living_annual):
		self.username = username
		self.course_id = course_id
		self.cost_of_living = cost_of_living
		self.cost_of_living_annual = cost_of_living_annual
		self.created_at = datetime.utcnow()
  
class CostOfLiving(db.Model):
	__tablename__ = 'cost_of_living'
	
	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.String(100), nullable=False)
	area = db.Column(db.String(100), nullable=False)
	rent = db.Column(db.Float, nullable=False)
	grocery = db.Column(db.Float, nullable=False)
	transportation = db.Column(db.Float, nullable=False)
	utilities = db.Column(db.Float, nullable=False)
	entertainment = db.Column(db.Float, nullable=False)

	def __init__(self, state, area, rent, grocery, transportation, utilities, entertainment):
		self.state = state
		self.area = area
		self.rent = rent
		self.grocery = grocery
		self.transportation = transportation
		self.utilities = utilities
		self.entertainment = entertainment

# ---- Admin Dashboard Charts ----
class UserGroup(db.Model):
	__tablename__ = 'user_groups'

	id = db.Column(db.Integer, primary_key=True)
	group_name = db.Column(db.String(255), nullable=False)
	total_users = db.Column(db.Integer, nullable=False)

	def __init__(self, group_name, total_users):
		self.group_name = group_name
		self.total_users = total_users

class UserLogin(db.Model):
	__tablename__ = 'user_logins'

	id = db.Column(db.Integer, primary_key=True)
	group_name = db.Column(db.String(255), nullable=False)
	login_month = db.Column(db.String(255), nullable=False)
	total_logins = db.Column(db.Integer, nullable=False)

	def __init__(self, group_name, login_month, total_logins):
		self.group_name = group_name
		self.login_month = login_month
		self.total_logins = total_logins


class CourseAdded(db.Model):
	__tablename__ = 'courses_added'

	id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(255), nullable=False)
	added_month = db.Column(db.String(255), nullable=False)
	total_courses = db.Column(db.Integer, nullable=False)

	def __init__(self, category_name, added_month, total_courses):
		self.category_name = category_name
		self.added_month = added_month
		self.total_courses = total_courses