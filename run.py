from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)

# Database Configurations

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:root123@localhost/practice_for_myself_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Blueprint For Table Models


class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_no = db.Column(db.Integer, nullable=False, unique=True)
    sport = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Sport(db.Model):
    sport_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sport_name = db.Column(db.String(60), nullable=False)
    entry_token = db.Column(db.Integer, nullable=False, unique=True)
    entry_fee = db.Column(db.Float, nullable=False)
    trainer = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Error handling with if condition

if __name__ == "__main__":
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            print("SUCCESS: Your Database Have Connected Successfully >>>>")
            db.create_all()
    except Exception as error:
        print("ERROR: Your Database Connection Is Failed >>>>")
        print(error)
    app.run(debug=True, port=5200)
