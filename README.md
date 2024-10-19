# Technology Design Project: EasyResi Application
## Table of Contents
1. [Project Overview](#project-overview)
2. [Team Members](#team-members)
3. [Technologies Used](#technologies-used)
4. [Installation and Setup](#installation-and-setup)
5. [Usage](#usage)
6. [Features](#features)
7. [Project Structure](#project-structure)
8. [License](#license)

## Project Overview
EasyResi is a Flask web application designed to assist users in planning to migrate to Australia. Applicants can use the questionnaires to check visa eligibility, find the optimal study pathway, and analyse the cost of living. Education providers, such as universities, can input their available courses and see the statistics related to education. Migration agencies can also use this application to input the cost of living and occupation list as well as statistics relevant to them. This application follows a Model-View-Controller (MVC) architecture to ensure maintainability and scalability. It organizes code into distinct components: models for database handling, Views for rendering web pages, and Controllers for processing user inputs.

Key Features:
1. Visa Eligibility Calculation: Users can calculate their eligibility for different visa subclasses (Visa 189, 190, 491) based on various factors such as age, work experience, education, and more.
2. Course and University Management: Users can manage educational courses and associated universities.
3. Occupation Management: Includes the management of a list of occupations with corresponding ANZSCO codes.
4. Cost-of-Living Calculator: Users can analyze living expenses (rent, utilities, groceries, etc.) across different regions and states.
5. Role-Based Access: User roles (Administrator, Applicant, Migration Agency, Educational Institution) control access to different functionalities and views.
   - Admin has complete access to all application features.
   - Applicant has 
7. Admin Dashboard: Statistical data visualization for admins, including login and course data.

## Team Members
- Hani Omar M. Alharbi - Team Leader & Backend Developer
- Danny Steven Simanungkalit - Backend Developer
- Ha Ngo - Frontend Developer
- Tserennadmid Battulga - Frontend Developer
- Chiara To - Backend Developer

## Technologies Used
- Python 3.8+
- Flask (Web Framework)
- SQLAlchemy (ORM for database management)
- PostgreSQL (Database)
- Jinja2 (Templating Engine for HTML)
- Flask-Migrate (Database migrations)
- DataTables (Client-side table management)
- jQuery (JavaScript library)
- HTML5/CSS3 (Frontend)
