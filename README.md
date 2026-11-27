# Student Performance Dashboard

An interactive Streamlit dashboard with database-integrated user authentication (Signup and Login) using SQL Server, built for exploring the Student Performance dataset.

## Features
- User registration (Signup) and login with hashed passwords stored in SQL Server (`Users` table)
- Dataset preview showing total rows and columns along with sample records
- Interactive visualization allowing users to select columns and view bar charts
- Session logout functionality

## Setup and Execution
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate