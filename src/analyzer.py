import pika
import json
from flask import Flask
from src.models import db, DeviceData
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_url = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'EcoPrice.sqlite3'))
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def compute_eco_score(price):
    # Simulated computation for sustainability
    # e.g., mapping price to a score between 0 and 100
    score = 100 - (price / 20)
    return max(0.0, min(100.0, score))

def callback(ch, method, properties, body):
    data = json.loads(body)
    title = data.get('title')
    price = data.get('price')
    print(f" [x] Received {title} at ${price}")
    
    # Calculate score
    score = compute_eco_score(price)
    
    with app.app_context():
        # Insert or update in database
        device = DeviceData(title=title, price=price, eco_score=score)
        db.session.add(device)
        db.session.commit()
    print(f" [x] Processed and saved. Eco Score: {score}")

def start_worker():
    with app.app_context():
        db.create_all()
    
    rabbitmq_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    channel.queue_declare(queue='raw_device_data')
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue='raw_device_data', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
