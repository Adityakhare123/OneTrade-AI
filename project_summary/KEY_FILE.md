# OneTradeAI - Project Key File

## 1) Project Purpose
This project is an AI-based trading dashboard that lets users:
- sign up / log in
- add trade entries with profit/stop-loss limits
- view recent trades
- get market prediction suggestions from a backend ML model

## 2) Main Tech Stack
- Frontend: React + React Bootstrap + React Router
- Backend: Flask + Flask RESTful + Flask SQLAlchemy
- Database: SQLite
- Prediction logic: Python + TensorFlow / Keras + pandas + yfinance + TA-Lib

## 3) Folder Structure
- `backend/backend/` → Flask server and API logic
- `frontend/frontend/` → React web app
- `back_algo/back_algo/` → notebook / experiment scripts for crypto prediction

## 4) How the app works
1. User opens the frontend and signs in or signs up.
2. The frontend stores user data in `localStorage`.
3. The backend validates credentials and stores trade details.
4. The dashboard shows recent trade history.
5. The prediction endpoint checks pending trades and tries to decide if the market is likely to go up/down.

## 5) Important API Endpoints
- `POST /login` → login user
- `POST /sign_up` → create user
- `POST /add_trade` → add new trade
- `GET /recent_trades?userId=...` → get user's recent trades
- `GET /predict` → run prediction logic for pending trades

## 6) Key Frontend Pages
- `/` → home page
- `/login` → login form
- `/signup` → signup form
- `/dashboard` → recent trades and add trade form
- `/profile` and `/settings` → profile-related screens

## 7) Key Backend Files
- `backend/backend/main.py` → starts Flask app and registers routes
- `backend/backend/controllers/auth.py` → login/signup logic
- `backend/backend/controllers/trade.py` → trade creation and history logic
- `backend/backend/controllers/predict.py` → prediction logic and market decision logic
- `backend/backend/models/User.py` → user database model
- `backend/backend/models/Trades.py` → trade database model

## 8) Suggested Run Instructions
### Backend
- cd backend/backend
- pip install -r requirements.txt
- python main.py

### Frontend
- cd frontend/frontend
- npm install
- npm start

## 9) Notes for Sharing
The project is a demo/training-style application. Some parts may still need cleanup, especially the prediction logic and API response handling.
