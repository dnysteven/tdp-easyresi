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

-- Create the Visa_points table within the schema
CREATE TABLE visa_points (
	id SERIAL PRIMARY KEY,
	age INTEGER NOT NULL,
	english_language VARCHAR(20) NOT NULL,
	overseas_employment INTEGER NOT NULL,
	australian_employment INTEGER NOT NULL,
	education_level VARCHAR(50) NOT NULL,
	specialist_education VARCHAR(3) NOT NULL,  -- Yes or No
	australian_study VARCHAR(3) NOT NULL,      -- Yes or No
	professional_year VARCHAR(3) NOT NULL,     -- Yes or No
	community_language VARCHAR(3) NOT NULL,    -- Yes or No
	regional_study VARCHAR(3) NOT NULL,        -- Yes or No
	partner_skills VARCHAR(50) NOT NULL        -- Has age/English/skills, competent English, or single/citizen/pr
);
