import pandas as pd
from app import app, db, Flight

df = pd.read_csv('Clean_Dataset.csv')

with app.app_context():
    for _, row in df.iterrows():
        flight = Flight(
            airline=row['airline'],
            flight=row['flight'],
            source_city=row['source_city'],
            departure_time=row['departure_time'],
            stops=row['stops'],
            arrival_time=row['arrival_time'],
            destination_city=row['destination_city'],
            flight_class=row['class'],
            duration=row['duration'],
            days_left=row['days_left'],
            price=row['price']
        )
        db.session.add(flight)
    
    db.session.commit()
    print("Data loaded successfully")