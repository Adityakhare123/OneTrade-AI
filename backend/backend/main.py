from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS

from lib.db import db
from controllers.auth import Login, SignUp
from controllers.trade import AddTrade, RecentTrades

# Prediction may fail if ML packages like TensorFlow / TA-Lib are missing
try:
    from controllers.predict import PredictionModel
    prediction_available = True
    prediction_error = None
except Exception as e:
    PredictionModel = None
    prediction_available = False
    prediction_error = str(e)


app = Flask(__name__)

CORS(app)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db?timeout=30"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "OneTradeAI backend is running"
    })


api.add_resource(Login, "/login")
api.add_resource(SignUp, "/sign_up")
api.add_resource(AddTrade, "/add_trade")
api.add_resource(RecentTrades, "/recent_trades")


if prediction_available:
    api.add_resource(PredictionModel, "/predict")
else:
    @app.route("/predict")
    def predict_not_available():
        return jsonify({
            "status": "error",
            "message": "Prediction module is not available",
            "reason": prediction_error,
            "fix": "Install missing ML packages like tensorflow, pandas, yfinance, and TA-Lib."
        }), 500


def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
    app.run(host="127.0.0.1", port=5000, debug=True)