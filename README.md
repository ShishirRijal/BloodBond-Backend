# BloodBond: Revolutionizing Blood Donation 🩸

![BloodBond](https://img.shields.io/badge/Project-BloodBond-red?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyMS4zNWwtMS40NS0xLjMyQzUuNCAxNS4zNiAyIDEyLjI4IDIgOC41IDIgNS40MiA0LjQyIDMgNy41IDNjMS43NCAwIDMuNDEuODEgNC41IDIuMDlDMTMuMDkgMy44MSAxNC43NiAzIDE2LjUgMyAxOS41OCAzIDIyIDUuNDIgMjIgOC41YzAgMy43OC0zLjQgNi44Ni04LjU1IDExLjU0TDEyIDIxLjM1eiIvPjwvc3ZnPg==)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

## 📱 Overview

**BloodBond** is a revolutionary mobile app designed to transform the blood donation experience. Our mission is to connect donors with those in need, making the process of giving and receiving blood simpler, faster, and more engaging than ever before.

### 🌟 Key Features

- 🩸 Easy donor registration and search
- 📍 Location-based donor matching
- 🚨 Real-time push notifications for urgent needs
- 🎮 Gamified donation system with redeemable points
- 🦠 Real-time alerts on viral diseases
- 🤝 Social media integration for sharing donation stories

## 🏗️ Project Structure

```
bloodbond-backend/
├── .idea/
├── .myenv/
├── alembic/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── o2auth.py
│   ├── schemas.py
│   └── utils.py
├── models/
├── routes/
├── .env
├── .gitignore
├── alembic.ini
├── gunicorn.service
├── Procfile
├── requirements.txt
└── runtime.txt
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- pip (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/ShishirRijal/bloodbond-backend.git
cd bloodbond-backend
```

### 2. Set Up Virtual Environment

```bash
# For macOS/Linux
python3 -m venv .myenv
source .myenv/bin/activate

# For Windows
python -m venv .myenv
.myenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```env
DATABASE_URL="postgresql://<username>:<password>@<host>/<database_name>"
SECRET_KEY="<your_secret_key>"
ALGORITHM="<your_algorithm>"
ACCESS_TOKEN_EXPIRE_MINUTES=<your_expiry_time_in_minutes>
EMAIL_APP_PASSWORD="<your_email_app_password>"
MY_EMAIL_ADDRESS="<your_email_address>"
ONESIGNAL_API_KEY="<your_onesignal_api_key>"
```

### 5. Set Up Database

```bash
alembic upgrade head
```

### 6. Start the Application

For production:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

For development:
```bash
uvicorn app.main:app --reload
```

### 7. Access the API

Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore the API documentation.

## 💼 Business Model

BloodBond operates on a freemium model, ensuring sustainability through:

- 🏥 Hospital subscriptions
- 🎉 Sponsored events
- 📱 In-app advertising
- 👕 Branded merchandise sales

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 💖 All our amazing donors and users
- 🏥 Partnering hospitals and blood banks
- 🚑 Emergency services for their invaluable support

---

<div align="center">
  Made with ❤️ by the BloodBond Team
  <br>
  Saving lives, one donation at a time 🩸
</div>
