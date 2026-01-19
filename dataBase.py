from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_name = db.Column(db.String(100), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "sensor_name": self.sensor_name,
            "sensor_type": self.sensor_type,
            "value": round(self.value, 1),
            "unit": self.unit,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

def save_sensor_data(sensor_name, sensor_type, value, unit):
    """Save sensor measurement to database"""
    from flask import current_app
    
    try:
        with current_app.app_context():
            data = SensorData(
                sensor_name=sensor_name,
                sensor_type=sensor_type,
                value=value,
                unit=unit
            )
            db.session.add(data)
            db.session.commit()
    except RuntimeError:
        # If called outside of app context, skip saving (shouldn't happen in normal use)
        pass

