-- Create the schema if it does not exist
CREATE SCHEMA IF NOT EXISTS "tdp-easyresi";

-- Set the schema to use
SET search_path TO "tdp-easyresi";

-- Create the user_role table to store roles information
CREATE TABLE user_role (
	user_role VARCHAR(20) PRIMARY KEY,      -- User role, primary key
	name VARCHAR(50) NOT NULL,              -- Role name, required
	description VARCHAR(255) NOT NULL       -- Role description, required
);

-- Create the users table to store user information
CREATE TABLE users (
	username VARCHAR(50) PRIMARY KEY,       -- Username is the primary key
	first_name VARCHAR(50) NOT NULL,        -- First name, required
	last_name VARCHAR(50) NOT NULL,         -- Last name, required
	email VARCHAR(100) NOT NULL,            -- Email, required
	phone VARCHAR(20) NOT NULL,             -- Phone number, required
	user_role VARCHAR(20) NOT NULL,         -- Foreign key to user_role table, required
	CONSTRAINT fk_user_role FOREIGN KEY (user_role) 
		REFERENCES user_role (user_role)    -- Establishing the foreign key
);

-- Create the login table to store login credentials
CREATE TABLE login (
	username VARCHAR(50) PRIMARY KEY,      -- Username is the primary key, related to users table
	password VARCHAR(255) NOT NULL,        -- Plain-text password (for example purposes, should be hashed)
	hashed_password VARCHAR(255) NOT NULL, -- Hashed password, required
	CONSTRAINT fk_username FOREIGN KEY (username)
		REFERENCES users (username)        -- One-to-one relationship with the users table
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
CREATE TABLE visa_points (
	id SERIAL PRIMARY KEY,
	username VARCHAR(50) NOT NULL,
	age INTEGER NOT NULL,
	english_language VARCHAR(50) NOT NULL,
	overseas_employment INTEGER NOT NULL,
	australian_employment INTEGER NOT NULL,
	education_level VARCHAR(50) NOT NULL,
	specialist_education VARCHAR(10) NOT NULL,
	australian_study VARCHAR(10) NOT NULL,
	professional_year VARCHAR(10) NOT NULL,
	community_language VARCHAR(10) NOT NULL,
	regional_study VARCHAR(10) NOT NULL,
	partner_skills VARCHAR(50) NOT NULL,
	state_nomination VARCHAR(10) NOT NULL,
	regional_nomination VARCHAR(10) NOT NULL,
	visa_189_points INTEGER NOT NULL,
	visa_190_points INTEGER NOT NULL,
	visa_491_points INTEGER NOT NULL,
	visa_189_eligible BOOLEAN NOT NULL,
	visa_190_eligible BOOLEAN NOT NULL,
	visa_491_eligible BOOLEAN NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_username FOREIGN KEY (username)
		REFERENCES users (username)
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