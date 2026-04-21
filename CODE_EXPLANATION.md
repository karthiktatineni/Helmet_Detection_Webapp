# 📂 MP Deployment Codebase & Architecture Explanation

This document serves as a comprehensive guide to understanding every folder and file in the Helmet Detection Web Application. The project is split into a **Frontend (React)** and **Backend (FastAPI)** architecture.

---

## 🏗️ Root Directory

* **`README.md`**: The main presentation of the GitHub repository outlining how to setup, deploy, and understand the project.
* **`requirements.txt`**: Python dependencies list used by the backend. We swapped `tensorflow` with `tensorflow-cpu` to ensure extremely fast cloud deployment speeds.
* **`run.bat`**: A convenient script for Windows users that boots up both the Vite Frontend and Python Backend simultaneously with a single double-click.
* **`.gitignore`**: Prevents Git from tracking or uploading huge 500MB+ ML models, sensitive emails/passwords from `.env`, and unneeded build files (`node_modules/`, `__pycache__`).
* **`.env` (not tracked in Git)**: Central configuration file holding the database paths, model paths, API settings, and email setup (SENDER_EMAIL, RECEIVER_EMAIL).
* **`helmet_detection_system_design.md`**: The original system planning document outlining the overall goals and structure.

---

## 🎨 1. Frontend Directory (`/frontend/`)

This folder contains the **React 18 + Vite** application providing the UI for the detection system.

* **`index.html`**: The root HTML file that React launches inside.
* **`package.json`** & **`package-lock.json`**: Lists all Javascript libraries and scripts (like `npm run dev`) installed for the UI.
* **`vite.config.js`**: Settings for the Vite server (the ultra-fast build tool substituting standard Create React App).
* **`tsconfig.json`**: Configuration for standardizing Javascript/Typescript language formats.
* **`.env`**: Holds `VITE_API_URL` pointing the UI to the FastAPI server.

### `/frontend/src/`
The core component logic for React:
* **`App.jsx`**: The main Shell of the application containing the Sidebar Navigation, Toast Notifications, the Application Routing to the 4 pages, and a background keep-alive ping loop.
* **`main.jsx`**: The entry point mounting `App.jsx` onto `index.html`.

### `/frontend/src/pages/`
The 4 main screens of the UI:
* **`DashboardPage.jsx`**: The landing page displaying total violations, graphs, and the UI hero banner.
* **`DetectionPage.jsx`**: Allows the user to physically drag-and-drop Image/Video files, configure confidence sliders, and display annotated boundary box outputs.
* **`HistoryPage.jsx`**: Shows the database history of all past runs with search/filter mechanics.
* **`AboutPage.jsx`**: Displays info about the detection technology stack.

### `/frontend/src/services/`
* **`api.js`**: Contains all Axios `GET`/`POST` requests formatting the browser calls into proper shapes for the Backend API. Includes the `/health` pings.

### `/frontend/src/styles/`
* **`index.css`**: Defines all core vanilla CSS formatting logic like background colors, text layouts, input fields, and UI animations.

---

## ⚙️ 2. Backend Directory (`/backend/`)

This acts as the main Engine of the whole project built on **FastAPI (Python)**. 

* **`main.py`**: The heart of the Python server. Combines routers, controls CORS allowing Vercel to ping Render, serves `data/` folder files to the web, and begins the application lifecycle.
* **`config.py`**: Intercepts variables generated in your root `.env` file (like model paths and email passwords) handling them dynamically within the code using Pydantic Validation.

### `/backend/api/`
The physical URL paths exposed by the server.
* **`health.py`**: Houses `/health` responding with "ok" to keep uptime bots happy, and `/api/v1/stats` to aggregate numbers for the frontend Dashboard.
* **`detection.py`**: Houses `/api/v1/detect/image` and `/api/v1/detect/video`. These intercept dropped files from React, calculate their sizes/authenticity, initiate background emails, and invoke the Detection Pipelines to scan the media.
* **`history.py`**: Connects UI History page requests to backend database reads/deletes.

### `/backend/services/`
The logic bridging endpoints to the inner systems.
* **`detection_service.py`**: Maps and manages the extremely complex loop of: finding a person -> sending them to the helmet detector -> calculating violation logic -> drawing boxes on the image -> saving image to the internal disk.
* **`notification_service.py`**: Intercepts triggered violations and logs in to `yagmail` using your `.env` SMTP login to dispatch alert emails cleanly.

### `/backend/inference/`
The actual Machine Learning "Brains". 
* **`model_manager.py`**: "Lazy Loading" manager making sure humongous models are only loaded into RAM ONCE effectively caching them to prevent lag.
* **`bike_person_detector.py`**: Code configuring OpenCV to load `yolov3.weights` looking explicitly for classes "Person" and "Motorbike".
* **`helmet_detector.py`**: Code configuring OpenCV to load custom-trained `yolov3-obj_2400.weights` to detect single-class "Helmet" bounding boxes.
* **`plate_classifier.py`**: Tensorflow scripts processing cropped bounding boxes through `model_weights.h5` checking mapping against predefined 20 JSON plates.

### `/backend/database/`
Where everything gets saved for History.
* **`database.py`**: Establishes standard Async SQLite connection.
* **`models.py`**: The actual database tables (specifically mapping SQLAlchemy shapes for "Detections").
* **`crud.py`**: Easy-to-use functions like `get_stats`, `save_detection`, and `delete_detection`.

### `/backend/schemas/`
* Holds Python object shapes defining what Data React is allowed to send FastAPI, and exactly what Data FastAPI has to send back.

---

## 💾 3. Secondary Folders

* **`/models/`**: The local storage location of all your `.weights`, `.cfg`, and `.h5` files allowing `.gitignore` to easily stop GitHub from stealing 1GB of upload space.
* **`/data/`**: Runtime locations that act as the internal Hard-Drive for the backend application while it is booted up.
  * **`data/uploads/`**: Temporarily stores raw incoming Mp4s / JPGs from React.
  * **`data/outputs/`**: Holds newly drawn annotated images generated before emailing them.
  * **`data/helmet_detection.db`**: The SQLite raw file containing your active history.
* **`/logs/`**: Keeps a running timeline of developer server bugs.
