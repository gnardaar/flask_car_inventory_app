# Location and rules of the server
# Allows two machines to talk to each other

# jsonify will reformat our data into json so we can use it with Python and JS
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

# url_prefix means we need api in front of our end slug.
api = Blueprint('api',__name__, url_prefix='/api')

# allows us to pull data into insomnia
@api.route('/getdata')
def getdata():
    return {'driver': 'car'}

# This will post car data to the database (on insomnia) -- mimics another back end app requesting data with our flask app
# token is required to send the data
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    condition = request.json['condition']
    user_token = current_user_token.token

# Tells us in the terminal if everything up to this point has worked.
    print(f'BIG TESTER: {current_user_token.token}')

# Instantiates the Car class with the data we just pulled from the json
    car = Car(make, model, year, condition, user_token = user_token )

# puts all the info into the database
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)


# Gets all the car data from our database and displays it in Insomnia in json format
@api.route('/cars', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# If we want a specific car we can call it with an id number
# We're querying by id number, then returning the data that query grabs
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# Get all the data from our query by the passed in ID
# save them all to a car, and then individually rewrite them
# We have to manually update the JSON piece
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token,id):
    car = Car.query.get(id) 
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.condition = request.json['condition']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete cars by id
# If we didn't do it by id we'd delete the whole database
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)