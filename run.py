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
    phone_no = db.Column(db.String(10), nullable=False, unique=True)
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


# GET ALL METHOD ROUTE


@app.route("/api/players", methods=["GET"])
def get_players():
    players = Player.query.all()

    details = []

    for player in players:
        details.append(
            {
                "id": player.player_id,
                "name": player.name,
                "age": player.age,
                "phone_no": player.phone_no,
                "sport": player.sport,
                "created_at": player.created_at,
            }
        )
    return jsonify(details), 200


# GET ONE METHOD ROUTE


@app.route("/api/players/<int:player_id>", methods=["GET"])
def get_player(player_id):
    player = Player.query.get(player_id)

    # GET ONE METHOD VAILDATION

    if not player:
        return jsonify({"message": "Player Not Found"}), 404

    return jsonify(
        {
            "id": player.player_id,
            "name": player.name,
            "age": player.age,
            "phone_no": player.phone_no,
            "sport": player.sport,
            "created_at": player.created_at,
        }
    )


#  PUT METHOD ROUTE


@app.route("/api/players/<int:player_id>", methods=["PUT"])
def update_player(player_id):
    player = Player.query.get(player_id)

    # PUT METHOD VAILDATION

    data = request.json

    if not data:
        return jsonify({"message": "Data Must Be Required"}), 400

    elif not player:
        return jsonify({"message": "Player Not Found"}), 404

    if "name" in data:
        player.name = data["name"]

    if "age" in data:
        player.age = data["age"]

    if "phone_no" in data:
        player.phone_no = data["phone_no"]

    if "sport" in data:
        player.sport = data["sport"]

    db.session.commit()

    return jsonify({"message": "Player Has Been Updated Successfully"}), 200


# DELETE METHOD ROUTE


@app.route("/api/players/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    player = Player.query.get(player_id)

    # DELETE METHOD VAILDATION

    if not player:
        return jsonify({"message": "Player Not Found"}), 404

    db.session.delete(player)
    db.session.commit()

    return jsonify({"message": f"Player id={player_id} is Deleted Successfully"}), 200


# SPORT HTTP METHODS USED
# POST METHODE ROUTE


@app.route("/api/sports", methods=["POST"])
def create_sport():
    data = request.get_json()

    # POST METHOD VAILDATIONS

    if not data:
        return jsonify({"message": "You Must Feed Sport Data"}), 400

    elif not data.get("sport_name"):
        return jsonify({"message": "Sport Name Is Required"}), 400

    elif not data.get("entry_token"):
        return jsonify({"message": "Sport Entry Token is Required"}), 400

    elif not data.get("entry_fee"):
        return jsonify({"messsage": "Sport Entry Fee is Required"}), 400

    else:
        existing = Sport.query.filter_by(entry_token=data["entry_token"]).first()
        if existing:
            return jsonify({"message": "This Entry Token Already Existed"}), 409

    new_sports = Sport(
        sport_name=data["name"],
        entry_token=data["entry_token"],
        entry_fee=data["entry_fee"],
        trainer=data["trainer"],
    )

    db.session.add(new_sports)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Sport Records Are Added Successfully >>>",
                "id": new_sports.sport_id,
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
