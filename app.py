from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:YinYang1227@localhost/flights'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(50))
    flight = db.Column(db.String(20))
    source_city = db.Column(db.String(50))
    departure_time = db.Column(db.String(20))
    stops = db.Column(db.String(20))
    arrival_time = db.Column(db.String(20))
    destination_city = db.Column(db.String(50))
    flight_class = db.Column(db.String(20))
    duration = db.Column(db.Float)
    days_left = db.Column(db.Integer)
    price = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify("Flight Price API")


@app.route('/flights')
def get_flights():
    flights = Flight.query.limit(50).all()
    output = []
    for flight in flights:
        data = {
            "id": flight.id,
            "airline": flight.airline,
            "flight": flight.flight,
            "source_city": flight.source_city,
            "destination_city": flight.destination_city,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "stops": flight.stops,
            "class": flight.flight_class,
            "duration": flight.duration,
            "days_left": flight.days_left,
            "price": flight.price
        }
        output.append(data)
    return jsonify(output)


@app.route('/flights/<int:id>')
def get_flight(id):
    flight = Flight.query.get_or_404(id)
    return jsonify({
        "id": flight.id,
        "airline": flight.airline,
        "flight": flight.flight,
        "source_city": flight.source_city,
        "destination_city": flight.destination_city,
        "departure_time": flight.departure_time,
        "arrival_time": flight.arrival_time,
        "stops": flight.stops,
        "class": flight.flight_class,
        "duration": flight.duration,
        "days_left": flight.days_left,
        "price": flight.price
    })
    
    
    
@app.route('/flights/search')
def search_flights():
    source = request.args.get('source')
    destination = request.args.get('destination')
    airline = request.args.get('airline')
    flight_class = request.args.get('class')
    stops = request.args.get('stops')
    id=request.args.get('id')
    
    
    query = Flight.query

    if source:
        query = query.filter_by(source_city=source)
    if destination:
        query = query.filter_by(destination_city=destination)
    if airline:
        query = query.filter_by(airline=airline)
    if flight_class:
        query = query.filter_by(flight_class=flight_class)
    if stops:
        query = query.filter_by(stops=stops)
    if id:
        query = query.filter_by(id=id)    
        

    flights = query.limit(50).all()
    output = []
    for flight in flights:
        data = {
            "id": flight.id,
            "airline": flight.airline,
            "flight": flight.flight,
            "source_city": flight.source_city,
            "destination_city": flight.destination_city,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "stops": flight.stops,
            "class": flight.flight_class,
            "duration": flight.duration,
            "days_left": flight.days_left,
            "price": flight.price
        }
        output.append(data)
    
    return jsonify(output)