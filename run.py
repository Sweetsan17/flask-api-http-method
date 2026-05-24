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


# PLAYER HTTP METHODS USED
# POST METHOD ROUTE


@app.route("/api/players", methods=["POST"])
def create_player():
    data = request.get_json()

    # POST METHOD VAILDATIONS

    if not data:
        return jsonify({"message": "You Must Feed Player Data"}), 400

    elif not data.get("name"):
        return jsonify({"message": "Player Name Is Required"}), 400

    elif not data.get("age"):
        return jsonify({"message": "Player Age is Required"}), 400

    elif not data.get("phone_no"):
        return jsonify({"messsage": "Player Phone Number is Required"}), 400

    elif not data.get("sport"):
        return jsonify({"message": "Player In Sports Must Be Required"}), 400

    else:
        existing = Player.query.filter_by(phone_no=data["phone_no"]).first()
        if existing:
            return jsonify({"message": "This Phone Number Already Existed"}), 409

    new_player = Player(
        name=data["name"],
        age=data["age"],
        phone_no=data["phone_no"],
        sport=data["sport"],
    )

    db.session.add(new_player)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Player Records Are Added Successfully >>>",
                "id": new_player.player_id,
            }
        ),
        201,
    )


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
