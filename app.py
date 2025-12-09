from flask import Flask, jsonify
from SimulationSensors import Sensor
import threading

app = Flask(__name__)

# Create new sensor instances
sensors = [
    Sensor("Temperature Sensor", "Temperature", "0-100", "Celsius"),
    Sensor("Pressure Sensor", "Pressure", "0-10", "Bar"),
    Sensor("Humidity Sensor", "Humidity", "0-100", "Percentage")
]

# Start measurement for the sensors in a separate thread(asynchronously cycle)
for s in sensors:
    threading.Thread(target=s.start_measurement, daemon= True).start()

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

if __name__ == "__main__":
    app.run(debug=False)
