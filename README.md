# CoinPay - Secure Payment Gateway

CoinPay is a secure and intuitive front-end payment gateway designed for student transactions. This project provides a clean user interface for capturing payment details and processes transactions securely using Razorpay. The backend is built with Flask and integrates with Supabase for user data storage.

## Features

* **Clean UI/UX:** A modern, two-step payment flow with a professional design.
* **Secure Payments:** Integrates with Razorpay for secure, PCI-compliant payment processing.
* **User Data Storage:** Saves user information to a Supabase database.
* **Full Stack Application:** Uses a Flask backend to handle API requests and serve the frontend.

## Technologies Used

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python (Flask)
* **Payment Gateway:** Razorpay
* **Database:** Supabase
* **Animations:** LottieFiles

## Project Structure

The project is organized into a standard Flask application structure:

```
/coinpay-app/
|
|-- app.py                # Main Flask application
|-- .env                  # Environment variables (API keys)
|-- requirements.txt      # (Optional) List of Python packages
|
|-- /static/              # Contains all static files
|   |-- /css/
|   |   |-- style.css
|   |-- /js/
|       |-- main.js
|       |-- payment.js
|
|-- /templates/           # Contains all HTML templates
|   |-- index.html
|   |-- payment.html
|
|-- venv/                 # Virtual environment folder
```

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

* Python 3.x installed on your system.
* API keys from [Razorpay](https://razorpay.com/) and [Supabase](https://supabase.com/).

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment folder
python -m venv venv
```

### 3. Activate the Virtual Environment

* **On Windows (Command Prompt / PowerShell):**
    ```bash
    venv\Scripts\activate
    ```
* **On Windows (Git Bash):**
    ```bash
    source venv/Scripts/activate
    ```
* **On macOS / Linux:**
    ```bash
    source venv/bin/activate
    ```
    Your terminal prompt should now start with `(venv)`.

### 4. Install Dependencies

Install all the required Python packages using pip.

```bash
pip install --upgrade setuptools
pip install Flask python-dotenv razorpay supabase
```

### 5. Configure Environment Variables

Create a new file named `.env` in the root directory of the project. This file will hold your secret API keys.

Copy the following into your `.env` file and replace the placeholder values with your actual keys.

```
SUPABASE_URL="your_supabase_url_here"
ANON_KEY="your_supabase_anon_key_here"
KEY_ID="your_razorpay_key_id_here"
KEY_SECRET="your_razorpay_key_secret_here"
```

## How to Run the Application

With your virtual environment activated and dependencies installed, start the Flask server:

```bash
python app.py
```

The server will start running in debug mode. Open your web browser and navigate to the following URL:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

You should now see the payment application's main page.
