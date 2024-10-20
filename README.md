# Technology Design Project: EasyResi Application

## Table of Contents
1. [Project Overview](#project-overview)
2. [Team Members](#team-members)
3. [Technologies Used](#technologies-used)
4. [Installation and Setup](#installation-and-setup)
   1. [Clone the Repository](#clone-the-repository)
   2. [Create a Virtual Environment](#create-a-virtual-environment)
   3. [Activate the Virtual Environment](#activate-the-virtual-environment)
   4. [Install Dependencies](#install-dependencies)
   5. [Set Up PostgreSQL Database](#set-up-postgresql-database)
   6. [Run the Flask Application](#run-the-flask-application)
   7. [Access the Application](#access-the-application)
5. [Usage](#usage)
6. [Key Features](#key-features)
7. [Project Structure](#project-structure)
8. [License](#license)

## Project Overview
EasyResi is a Flask web application designed to assist users planning to migrate to Australia. Applicants can use the questionnaires to check visa eligibility, find the optimal study pathway, and analyze the cost of living. Education providers, such as universities, can input their available courses and see the statistics related to education. Migration agencies can input the cost of living and occupation list and relevant statistics. This application follows a Model-View-Controller (MVC) architecture to ensure maintainability and scalability.

## Team Members
- Hani Omar M. Alharbi - Team Leader & Backend Developer
- Danny Steven Simanungkalit - Backend Developer
- Ha Ngo - Frontend Developer
- Tserennadmid Battulga - Frontend Developer
- Chiara To - Backend Developer

## Technologies Used
- **Python 3.8+**
- **Flask** (Web Framework)
- **SQLAlchemy** (ORM for database management)
- **PostgreSQL** (Database)
- **Jinja2** (Templating Engine for HTML)
- **Flask-Migrate** (Database migrations)
- **DataTables** (Client-side table management)
- **jQuery** (JavaScript library)
- **HTML5/CSS3** (Frontend)

## Installation and Setup

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/your-username/tdp_easyresi.git
```

### 2. Create a Virtual Environment
Create a Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
Activate the virtual environment. The command on Windows operating system:
```bash
venv\Scripts\activate
```

### 4. Install Dependencies
Install the necessary Python packages using pip:
```bash
pip install -r requirements.txt
```

### 5. Set Up PostgreSQL Database
- Ensure PostgreSQL is installed on your system.
- Create the PostgreSQL database and user:
  
  ```sql
  CREATE DATABASE tdp_easyresi_db;
  CREATE USER tdp_easyresi WITH PASSWORD 'your-password';
  GRANT ALL PRIVILEGES ON DATABASE tdp_easyresi_db TO tdp_easyresi;
  ```
- Update the config.py file with your database credentials:
  ```sql
  SQLALCHEMY_DATABASE_URI = 'postgresql://tdp_easyresi:your-password@localhost/tdp_easyresi_db?options=-csearch_path=tdp-easyresi'
  ```
- Run the SQL initialization script to create the database schema:
  ```sql
  psql -U tdp_easyresi -d tdp_easyresi_db -f init.sql
  ```

### 6. Run the Flask Application
Run the Flask application with:

