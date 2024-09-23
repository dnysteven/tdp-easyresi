import os

class Config:
	# Secret key to protect session data and other security features
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'tdp_project_easyresi'

	# Database configuration with schema set to `tdp-easyresi`
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost/postgres?options=-csearch_path=tdp-easyresi'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Set environment for development mode
	ENV = 'development'