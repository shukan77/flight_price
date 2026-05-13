from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Password123@localhost/flights'
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
    flight_class = request.args.get('flight_class')
    stops = request.args.get('stops')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

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
    if min_price:
        query = query.filter(Flight.price >= min_price)
    if max_price:
        query = query.filter(Flight.price <= max_price)
    if sort_by == 'price':
        query = query.order_by(Flight.price)
    elif sort_by == 'price_desc':
        query = query.order_by(Flight.price.desc())
    elif sort_by == 'duration':
        query = query.order_by(Flight.duration)
    elif sort_by == 'days_left':
        query = query.order_by(Flight.days_left)

    flights = query.paginate(page=page, per_page=per_page, error_out=False)

    output = []
    for flight in flights.items:
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

    return jsonify({
        "total": flights.total,
        "pages": flights.pages,
        "current_page": flights.page,
        "per_page": per_page,
        "flights": output
    })
@app.route('/flights', methods=['POST'])
def add_flight():
    data = request.json
    flight = Flight(
        airline=data['airline'],
        flight=data['flight'],
        source_city=data['source_city'],
        departure_time=data['departure_time'],
        stops=data['stops'],
        arrival_time=data['arrival_time'],
        destination_city=data['destination_city'],
        flight_class=data['flight_class'],
        duration=data['duration'],
        days_left=data['days_left'],
        price=data['price']
    )
    db.session.add(flight)
    db.session.commit()
    return jsonify({"message": "Flight added", "id": flight.id}), 201


@app.route('/flights/<int:id>', methods=['PUT'])
def update_flight(id):
    flight = Flight.query.get_or_404(id)
    data = request.json

    flight.airline = data.get('airline', flight.airline)
    flight.flight = data.get('flight', flight.flight)
    flight.source_city = data.get('source_city', flight.source_city)
    flight.departure_time = data.get('departure_time', flight.departure_time)
    flight.stops = data.get('stops', flight.stops)
    flight.arrival_time = data.get('arrival_time', flight.arrival_time)
    flight.destination_city = data.get('destination_city', flight.destination_city)
    flight_class = data.get('flight_class', flight.flight_class)
    flight.duration = data.get('duration', flight.duration)
    flight.days_left = data.get('days_left', flight.days_left)
    flight.price = data.get('price', flight.price)

    db.session.commit()
    return jsonify({"message": "Flight updated"}), 200


@app.route('/flights/<int:id>', methods=['DELETE'])
def delete_flight(id):
    flight = Flight.query.get_or_404(id)
    db.session.delete(flight)
    db.session.commit()
    return jsonify({"message": "Flight deleted"}), 200