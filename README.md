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

Author: Danny Steven Simanungkalit, Hani Omar M. Alharbi, Ha Ngo, Tserennadmid Battulga, Chiara To
## Project Overview
EasyResi is a Flask web application that assists users in visa-related processes, educational and migration course selection, and cost-of-living analysis. The application follows a Model-View-Controller (MVC) architecture to ensure maintainability and scalability, organizing code into distinct components: Models for database handling, Views for rendering web pages, and Controllers for processing user inputs.

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
