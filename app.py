from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///numbers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)

# database model for storing the number
class Number(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, *args, **kwargs):
        existing = Number.query.first()
        if existing:
            self.id = existing.id
            self.value = kwargs.get('value', existing.value)
        else:
            super(Number, self).__init__(*args, **kwargs)


    def __repr__(self):
        return f'<Number {self.value}>'

# create the database tables if they don't exist
@app.before_request
def create_tables():
    if not os.path.exists('numbers.db'):
        db.create_all()
        print("Database tables created")

# default route
@app.route('/')
def index():
    return "Welcome to the number storage API!"

# route to create or update the number
@app.route('/upsert', methods=['POST'])
def upsert_number():
    if not request.json or 'number' not in request.json:
        return jsonify({"error": "No number provided"}), 400

    try:
        number_value = float(request.json['number'])
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

    number = Number.query.first()
    if number:
        number.value = number_value
        db.session.commit()
        return jsonify({"message": "Number updated successfully!"}), 200
    else:
        new_number = Number(value=number_value)
        db.session.add(new_number)
        db.session.commit()
        return jsonify({"message": "Number created successfully!", "id": new_number.id}), 201

# route to get the current number
@app.route('/get_value', methods=['GET'])
def get_value():
    number = Number.query.first()
    if number:
        return jsonify({"number": number.value}), 200
    else:
        return jsonify({"error": "No number found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
