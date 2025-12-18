import time
import adafruit_dht

class DHT22Sensor:
    def __init__(self, pin):
        """
        Initialize the DHT22 sensor.
        :param pin: The GPIO pin object (e.g., board.D23)
        """
        self.sensor = adafruit_dht.DHT22(pin)
        self.temperature = 0.0
        self.humidity = 0.0

    def read(self):
        """
        Blocking read function.
        It keeps trying to read from the sensor until valid data is received.
        """
        while True:
            try:
                # Attempt to read temperature and humidity
                t = self.sensor.temperature
                h = self.sensor.humidity
                
                # Check if data is valid (not None)
                if t is not None and h is not None:
                    self.temperature = t
                    self.humidity = h
                    return # Data received, exit the function
            except RuntimeError:
                # Standard DHT errors (Checksum, Timeout). Wait and retry.
                time.sleep(1.0)
                continue
            except Exception as e:
                # Critical errors (e.g., hardware disconnection)
                self.sensor.exit()
                raise e

    def close(self):
        """Clean up resources."""
        self.sensor.exit()