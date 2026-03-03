from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
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
metrics = PrometheusMetrics(app)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    devices = DeviceData.query.all()
    result = []
    for d in devices:
        result.append({
            'id': d.id,
            'title': d.title,
            'price': d.price,
            'eco_score': d.eco_score,
            'date_fetched': d.date_fetched.isoformat() if d.date_fetched else None
        })
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)
