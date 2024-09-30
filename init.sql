-- Create the schema if it does not exist
CREATE SCHEMA IF NOT EXISTS "tdp-easyresi";

-- Set the schema to use
SET search_path TO "tdp-easyresi";

-- Create the user_role table to store roles information
CREATE TABLE user_role (
	user_role VARCHAR(20) PRIMARY KEY, 
	name VARCHAR(50) NOT NULL,
	description VARCHAR(255) NOT NULL
);

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
	email VARCHAR(255) PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	phone VARCHAR(20) NOT NULL,
	user_role VARCHAR(50) NOT NULL,
	edu_id VARCHAR(50),
	abn VARCHAR(50),
	street_address VARCHAR(255),
	suburb VARCHAR(255),
	state VARCHAR(3),
	postcode VARCHAR(4),
	created_at TIMESTAMP NOT NULL,
	FOREIGN KEY (user_role) REFERENCES user_role(user_role)
);

-- Create the login table
CREATE TABLE IF NOT EXISTS login (
	email VARCHAR(255) PRIMARY KEY,
	password VARCHAR(255) NOT NULL,
	hashed_password VARCHAR(255) NOT NULL,
	FOREIGN KEY (email) REFERENCES users(email)
);

-- Create the user_sessions table
CREATE TABLE user_sessions (
	id SERIAL PRIMARY KEY,
	email VARCHAR(255) REFERENCES users(email),
	login_time TIMESTAMPTZ NOT NULL,  -- Ensure this stores time with timezone
	logout_time TIMESTAMPTZ,  -- Ensure this stores time with timezone
	time_elapsed INTERVAL
);


-- Create the Data table within the schema
CREATE TABLE data (
	id SERIAL PRIMARY KEY,
	occupation_pathway INTEGER NOT NULL,       -- Numeric value for occupation pathway ('IT': 1, 'Engineering': 2, 'Nursing': 3, 'Education': 4)
	location INTEGER NOT NULL,                 -- Numeric value for location ('SA metro': 1, 'SA regional': 2, 'VIA regional': 3, 'VIA metro': 4)
	commitment_regional INTEGER NOT NULL,      -- Binary (1 for Yes, 0 for No)
	state_nomination INTEGER NOT NULL,         -- Binary (1 for Yes, 0 for No)
	course_duration INTEGER NOT NULL,          -- Duration of the course in years
	course_cost FLOAT NOT NULL,                -- Course cost in AUD
	cost_of_living FLOAT NOT NULL,             -- Cost of living in AUD
	visa_processing_time INTEGER NOT NULL,     -- Visa processing time in months
	visa_cost FLOAT NOT NULL,                  -- Visa cost in AUD
	approval_probability FLOAT NOT NULL,       -- Probability of visa approval (0 to 1)
	recommended_visa VARCHAR(10) NOT NULL      -- Predicted visa type (e.g., '189', '190')
);

-- Create the ModelResult table to store model training results within the schema
CREATE TABLE model_result (
	id SERIAL PRIMARY KEY,
	model_type VARCHAR(50) NOT NULL,           -- Type of the model (e.g., 'DecisionTree')
	accuracy FLOAT NOT NULL,                   -- Accuracy of the trained model
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the model was trained
);

-- Create visa_points table within the schema
CREATE TABLE IF NOT EXISTS visa_points (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	age VARCHAR(50) NOT NULL,
	english_level VARCHAR(50) NOT NULL,
	overseas_employment VARCHAR(50) NOT NULL,
	australian_employment VARCHAR(50) NOT NULL,
	education_level VARCHAR(50) NOT NULL,
	specialist_education BOOLEAN NOT NULL DEFAULT FALSE,
	australian_study BOOLEAN NOT NULL DEFAULT FALSE,
	professional_year BOOLEAN NOT NULL DEFAULT FALSE,
	community_language BOOLEAN NOT NULL DEFAULT FALSE,
	regional_study BOOLEAN NOT NULL DEFAULT FALSE,
	partner_skills VARCHAR(50) NOT NULL,
	nomination VARCHAR(50) NOT NULL,
	points INT NOT NULL,
	visa_189_eligible BOOLEAN NOT NULL DEFAULT FALSE,
	visa_190_eligible BOOLEAN NOT NULL DEFAULT FALSE,
	visa_491_eligible BOOLEAN NOT NULL DEFAULT FALSE,
	created_at TIMESTAMP NOT NULL,
	CONSTRAINT fk_username FOREIGN KEY (username) REFERENCES users(email)
);

-- Create university table with id as primary key
CREATE TABLE university (
	id SERIAL PRIMARY KEY,
	university VARCHAR(100) NOT NULL,
	street VARCHAR(100),
	suburb VARCHAR(100) NOT NULL,
	state CHAR(3) NOT NULL,
	postcode CHAR(4) NOT NULL,
	phone VARCHAR(15) NOT NULL,
	email VARCHAR(100) NOT NULL
);

-- Create uni_course table
CREATE TABLE uni_course (
	id SERIAL PRIMARY KEY,
	course_num VARCHAR(50) NOT NULL,
	course_name VARCHAR(100) NOT NULL,
	provider_id VARCHAR(50) NOT NULL,
	univ_id INTEGER NOT NULL,
	level VARCHAR(50) NOT NULL,
	specialist BOOLEAN NOT NULL,
	prof_year BOOLEAN NOT NULL,
	duration INTEGER NOT NULL,
	tuition_fee DECIMAL(10, 2) NOT NULL,
	regional BOOLEAN NOT NULL,
	CONSTRAINT fk_provider FOREIGN KEY (provider_id) REFERENCES users (username),
	CONSTRAINT fk_univ FOREIGN KEY (univ_id) REFERENCES university (id)
);

-- Update user_course_pref table (add created_at field)
CREATE TABLE user_course_pref (
	id SERIAL PRIMARY KEY,
	username VARCHAR(50) NOT NULL,
	course_num VARCHAR(50) NOT NULL,
	course_name VARCHAR(100) NOT NULL,
	provider_name VARCHAR(100) NOT NULL,
	university_name VARCHAR(100) NOT NULL,
	university_address VARCHAR(255) NOT NULL,
	state VARCHAR(3) NOT NULL,
	postcode CHAR(4) NOT NULL,
	duration INTEGER NOT NULL,
	tuition_fee DECIMAL(10, 2) NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_user_course FOREIGN KEY (username) REFERENCES users (username)
);