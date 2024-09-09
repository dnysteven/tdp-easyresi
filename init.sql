-- Create the schema if it does not exist
CREATE SCHEMA IF NOT EXISTS "tdp-easyresi";

-- Set the schema to use
SET search_path TO "tdp-easyresi";

-- Drop tables if they exist in the schema
DROP TABLE IF EXISTS model_result;
DROP TABLE IF EXISTS data;

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
