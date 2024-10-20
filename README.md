# Technology Design Project: EasyResi Application

## Table of Contents
1. [Project Overview](#project-overview)
2. [Team Members](#team-members)
3. [Technologies Used](#technologies-used)
4. [Installation and Setup](#installation-and-setup)
   - [Clone the Repository](#clone-the-repository)
   - [Create a Virtual Environment](#create-a-virtual-environment)
   - [Activate the Virtual Environment](#activate-the-virtual-environment)
   - [Install Dependencies](#install-dependencies)
   - [Set Up PostgreSQL Database](#set-up-postgresql-database)
   - [Run the Flask Application](#run-the-flask-application)
   - [Access the Application](#access-the-application)
5. [Usage](#usage)
6. [Key Features](#key-features)
7. [Project Structure](#project-structure)

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
```bash
python app.py
```
Or alternatively, use this command:
```bash
flask run
```

### 7. Access the Application
Once the application is running, open your web browser and navigate to:
```bash
http://127.0.0.1:5000
```

## Usage
Once the set up is complete, user can register as either admin, applicant, educational institution, or migration agency. After finish registering, user can login and perform tasks such as managing visa points, recommending courses, inputting data, and analyzing statistics.

## Key Features:
1. Visa Eligibility Calculation: Users can calculate their eligibility for different visa subclasses (Visa 189, 190, 491) based on various factors such as age, work experience, education, and more.
2. Course and University Management: Users can manage educational courses and associated universities, including living expenses (rent, utilities, groceries, etc.) across different regions and states.
3. Role-Based Access: User roles (Administrator, Applicant, Migration Agency, Educational Institution) control access to different functionalities and views.
   - Applicant can access questionnaires for Visa Eligibility Calculation and Study Pathway Calculation. The result will be saved and can be seen in their profile.
   - Education Provider can manage their list of universities and courses for Study Pathway Calculation. They also can see relevant statistics.
   - Migration Agency can manage their list of skilled occupations and living costs for Visa Eligibility and Study Pathway Calculation, respectively. They also can see relevant statistics.
   - Admin has complete access to all application features.
4. Security: All users who want to access this application must create their accounts before using it. Every password will be encrypted to ensure the security of each account.

## Project Structure
tdp_easyresi/  
│  
├── app/                               # Main application folder  
│   ├── __init__.py                    # Initializes the Flask app and imports views, controllers, and models  
│   ├── controllers.py                 # Handles business logic and database interactions  
│   ├── models.py                      # Defines database models using SQLAlchemy  
│   ├── views.py                       # Defines the routes and view functions for rendering templates  
│   ├── static/                        # Contains all static assets like CSS, JS, and images  
│   │   ├── css/                       # Folder for CSS files  
│   │   │   ├── Admin_Dashboard.css    # CSS file for the admin dashboard page  
│   │   │   ├── styles2.css            # Main CSS file for global styles  
│   │   │   ├── styles3.css            # CSS file for the education dashboard page  
│   │   │   ├── styles4.css            # CSS file for the migration dashboard page  
│   │   ├── js/                        # Folder for JavaScript files  
│   │   │   ├── charts.js              # JavaScript for rendering statistics charts  
│   │   │   ├── scripts.js             # Global JavaScript file for dynamic behaviors  
│   ├── templates/                     # Folder for all HTML templates  
│   │   ├── base.html                  # Base template used by all other templates  
│   │   ├── index.html                 # Home page template  
│   │   ├── login.html                 # Login page template  
│   │   ├── register.html              # Registration page template  
│   │   ├── visa_points.html           # Visa eligibility result page template  
│   │   ├── recommendation.html        # Recommended courses page template  
│   │   ├── courses.html               # Courses management page template  
│   │   ├── manage_course.html         # Add/Edit course form page template  
│   │   ├── university.html            # University management page template  
│   │   ├── manage_university.html     # Add/Edit university form page template  
│   │   ├── occupation.html            # Occupation management page template  
│   │   ├── manage_occupation.html     # Add/Edit occupation form page template  
│   │   ├── living_cost.html           # Living cost management page template  
│   │   ├── manage_living_cost.html    # Add/Edit living cost form page template  
│   │   ├── admin_statistics.html      # Admin dashboard for statistics  
│   │   ├── profile.html               # User profile page template  
│   │   ├── path_to_visa.html          # Path to visa options page template  
│   │   └── migra_statistics.html      # Migration statistics dashboard template  
├── database/                          # Folder containing CSV files for database population  
├── config.py                          # Configuration file for setting up the database, secret keys, etc.  
├── app.py                             # Main entry point for running the Flask app  
├── requirements.txt                   # List of Python dependencies to be installed  
├── README.md                          # Documentation for the project setup, usage, and structure  
├── init.sql                           # SQL script for initializing the database schema and tables  
├── .gitignore                         # Specifies files and directories to ignore in version control
