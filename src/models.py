from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class DeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    eco_score = db.Column(db.Float, nullable=True)
    date_fetched = db.Column(db.DateTime, default=datetime.utcnow)
