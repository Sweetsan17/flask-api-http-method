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

# Error handling with if condition

if __name__ == "__main__":
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            print("SUCCESS: Your Database Have Connected Successfully >>>>")
    except Exception as error:
        print("ERROR: Your Database Connection Is Failed >>>>")
        print(error)
    app.run(debug=True, port=5200)
