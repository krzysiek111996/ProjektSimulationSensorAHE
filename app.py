from flask import Flask, jsonify, send_from_directory
from SimulationSensors import Sensor
from dataBase import db, SensorData
import threading

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Create new sensor instances
sensors = [
    Sensor("Temperature Sensor", "Temperature", "10-28", "Celsius", app),
    Sensor("Pressure Sensor", "Pressure", "0-10", "Bar", app),
    Sensor("Humidity Sensor", "Humidity", "20-80", "Percentage", app)
]

# Start measurement for the sensors in a separate thread(asynchronously cycle)
for s in sensors:
    threading.Thread(target=s.start_measurement, daemon= True).start()

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/api/data_sensor", methods=["GET"])
def data_sensor():
    data = [s.get_data_sensor() for s in sensors]
    return jsonify(data)

@app.route("/api/sensor/<int:sensor_id>", methods=["GET"])
def data_chosen_sensor(sensor_id):
    if sensor_id < 0 or sensor_id >= len(sensors):
        return jsonify({"error": "Sensor not found"}), 404
    
    sensor = sensors[sensor_id]
    return jsonify(sensor.get_data_sensor())

@app.route("/api/history/<sensor_name>", methods=["GET"])
def get_sensor_history(sensor_name):
    """Get historical data for a specific sensor"""
    history = SensorData.query.filter_by(sensor_name=sensor_name).order_by(SensorData.timestamp.desc()).limit(100).all()
    return jsonify([data.to_dict() for data in history])

@app.route("/api/history", methods=["GET"])
def get_all_history():
    """Get all historical data from database"""
    history = SensorData.query.order_by(SensorData.timestamp.desc()).limit(500).all()
    return jsonify([data.to_dict() for data in history])

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
