import random
from time import sleep

class Sensor:
    def __init__(self, name, sensor_type, range, unit, app=None):
        self.name = name
        self.sensor_type = sensor_type
        self.range = range
        self.unit = unit
        self.app = app

        min_Val, max_Val = self.range.split('-')
        self.min_Val = float(min_Val)
        self.max_Val = float(max_Val)

        self.actValue = (self.min_Val + self.max_Val) / 2
        self.running = False
    
    def get_data_sensor(self):
        return {
            "name": self.name,
            "type": self.sensor_type,
            "range": self.range,
            "unit": self.unit,
            "actual_value": round(self.actValue, 1)
        }
    
    def start_measurement(self):
        from dataBase import db, SensorData
        
        self.running = True
        while self.running:
            self.actValue = self.actValue + random.uniform(-0.5, 0.5) # Simulate small difference of measurement
            if self.actValue < self.min_Val:
                self.actValue = self.min_Val
            elif self.actValue > self.max_Val:
                self.actValue = self.max_Val
            
            # Save data to database
            if self.app:
                with self.app.app_context():
                    data = SensorData(
                        sensor_name=self.name,
                        sensor_type=self.sensor_type,
                        value=self.actValue,
                        unit=self.unit
                    )
                    db.session.add(data)
                    db.session.commit()
            
            print(f"{self.name} Measurement: {self.actValue:.1f} {self.unit}") # Print current measurement in Terminal
            sleep(5) # task cyfle 5 second
    
    def stop_measurement(self):
        self.running = False


