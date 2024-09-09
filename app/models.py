from app import db

class Data(db.Model):
	__tablename__ = 'data'
	
	id = db.Column(db.Integer, primary_key=True)
	occupation_pathway = db.Column(db.Integer, nullable=False)
	location = db.Column(db.Integer, nullable=False)
	commitment_regional = db.Column(db.Integer, nullable=False)
	state_nomination = db.Column(db.Integer, nullable=False)
	course_duration = db.Column(db.Integer, nullable=False)
	course_cost = db.Column(db.Float, nullable=False)
	cost_of_living = db.Column(db.Float, nullable=False)
	visa_processing_time = db.Column(db.Integer, nullable=False)
	visa_cost = db.Column(db.Float, nullable=False)
	approval_probability = db.Column(db.Float, nullable=False)
	recommended_visa = db.Column(db.String(10), nullable=False)

class ModelResult(db.Model):
	__tablename__ = 'model_result'
	
	id = db.Column(db.Integer, primary_key=True)
	model_type = db.Column(db.String(50), nullable=False)
	accuracy = db.Column(db.Float, nullable=False)
	created_at = db.Column(db.DateTime, default=db.func.current_timestamp())