# Chemical Equipment Parameter Visualizer

### Hybrid Web + Desktop Application

**📌 Overview**
This project is a hybrid analytics application built as part of an internship screening task. It allows users to upload CSV files containing chemical equipment parameters, performs analysis on a Django backend, and visualizes results through two distinct frontends:
* **Web Application:** React.js
* **Desktop Application:** PyQt5

Both frontends communicate with the same **Django REST API**, ensuring consistent data handling, analytics, and reporting.

---

## 🧱 Technology Stack

| Component | Technologies |
| :--- | :--- |
| **Backend** | Python, Django, Django REST Framework, SQLite |
| **Data Processing** | Pandas (Analytics), ReportLab (PDF Generation) |
| **Frontend (Web)** | React.js, Chart.js, Fetch API |
| **Frontend (Desktop)** | PyQt5, Matplotlib, Python Requests |

---

## 📂 Project Structure

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

---

## 📄 CSV Data Format

The application expects CSV files with the following headers:

| Column Name | Data Type | Example |
| :--- | :--- | :--- |
| **Equipment Name** | String | `Pump A` |
| **Type** | String | `Pump` |
| **Flowrate** | Float | `120` |
| **Pressure** | Float | `5.6` |
| **Temperature** | Float | `75` |

**Raw CSV Example:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,120,5.6,75
Valve B,Valve,80,3.2,60
```

---

## ⚙️ Key Functionality

### 1. Backend (Django)
* **CSV Parsing:** Uses Pandas to compute total count, average flowrate, pressure, and temperature.
* **Data Retention:** Stores analytics in SQLite but keeps only the **last 5 uploaded datasets** (older records are auto-removed).
* **PDF Generation:** Creates a summary report using ReportLab. Protected by **HTTP Basic Auth**.

### 2. Web App (React)
* Dynamic CSV upload interface.
* **Visualization:** Equipment type distribution rendered via `Chart.js`.
* **Auth:** Browser handles the Basic Auth popup automatically when downloading the PDF.

### 3. Desktop App (PyQt5)
* Native file dialogs for CSV selection.
* **Visualization:** Charts rendered via `Matplotlib`.
* **Auth:** Credentials are sent programmatically (no browser popup). Includes a custom modal for download feedback.

---

## 🔐 Authentication

| Endpoint | Method | Authentication Required |
| :--- | :--- | :--- |
| `/api/upload/` | POST | ❌ No |
| `/api/report/` | GET | ✅ **HTTP Basic Auth** |

---

## ▶️ How to Run

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### 2. Web Frontend
```bash
cd frontend_web
npm install
npm start
```

### 3. Desktop Application
```bash
cd frontend_desktop
python desktop_app.py
```

---

## 🧪 Sample Data
A file named `sample_equipment_data.csv` is included in the root directory for testing purposes.
