Chemical Equipment Parameter Visualizer

Hybrid Web + Desktop Application

📌 Overview

This project is a hybrid analytics application built as part of an internship screening task.
It allows users to upload CSV files containing chemical equipment parameters, performs analysis on the backend, and visualizes results through:

a Web application (React)

a Desktop application (PyQt5)

Both frontends communicate with the same Django REST backend, ensuring consistent data handling and analytics.

The project focuses on:

correct backend logic

API integration

data analytics

cross-platform visualization

🧱 Technology Stack
Backend

Python

Django

Django REST Framework

Pandas (CSV processing & analytics)

SQLite (data storage)

ReportLab (PDF generation)

HTTP Basic Authentication (for PDF access)

Frontend – Web

React.js

Chart.js

Fetch API

Frontend – Desktop

PyQt5

Matplotlib

Requests (HTTP client)

```text
📂 Project Structure
project-root/
│
├── backend/
│   ├── api/
│   │   ├── views.py
│   │   ├── urls.py
│   ├── backend/
│   ├── db.sqlite3
│   ├── instruments.db
│   └── manage.py
│
├── frontend_desktop/
│   └── desktop_app.py
│
├── frontend_web/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
│
├── sample_equipment_data.csv
├── equipment_report.pdf
└── README.md
```

📄 CSV Format

The uploaded CSV file should contain the following columns:

Equipment Name, Type, Flowrate, Pressure, Temperature


Example:

Pump A,Pump,120,5.6,75
Valve B,Valve,80,3.2,60

⚙️ Backend Functionality
CSV Upload API

Accepts CSV files via REST endpoint

Parses data using Pandas

Computes:

total equipment count

average flowrate

average pressure

average temperature

equipment type distribution

Data Storage

Stores analytics results in SQLite

Keeps only the last 5 uploaded datasets

Older records are automatically removed

PDF Report Generation

Generates a PDF report for the latest uploaded dataset

Includes summary statistics and equipment distribution

Protected using HTTP Basic Authentication

🌐 Web Application (React)
Features

CSV upload interface

Equipment type distribution chart (Chart.js)

Summary statistics display

PDF download button (authenticated)

Behavior

CSV is uploaded to the Django backend

Analytics are returned as JSON

Charts are rendered dynamically

PDF download opens authenticated backend endpoint

🖥️ Desktop Application (PyQt5)
Features

CSV upload via file dialog

Summary display

Equipment type distribution chart (Matplotlib)

Secure PDF download with save-location dialog

Modal feedback during PDF download

Design Notes

Desktop client sends authentication credentials programmatically

No browser-style auth popup (expected desktop behavior)

UI kept simple for clarity and correctness

🔐 Authentication
Endpoint	Authentication
CSV Upload	No authentication
PDF Report	HTTP Basic Authentication

Browser handles auth popup automatically (Web)

Desktop client uses explicit credentials (PyQt)

▶️ How to Run
Backend
cd backend
pip install -r requirements.txt
python manage.py runserver

Web Frontend
cd frontend_web
npm install
npm start

Desktop App
cd frontend_desktop
python desktop_app.py

🧪 Sample Data

A sample CSV file sample_equipment_data.csv is included for testing and demonstration.
