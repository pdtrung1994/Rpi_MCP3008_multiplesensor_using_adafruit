import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class MultiGasSensor:
    def __init__(self):
        """
        Initialize SPI connection and MCP3008 chip.
        """
        # 1. Initialize SPI bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        
        # 2. Initialize Chip Select (CS) - Using CE0 (GPIO 8)
        cs = digitalio.DigitalInOut(board.D8)
        
        # 3. Create MCP3008 object
        self.mcp = MCP.MCP3008(spi, cs)
        
        # 4. Map sensors to specific channels (P0 - P5)
        self.sensors = {
            'MQ2':   AnalogIn(self.mcp, MCP.P0), # Slot 1
            'MQ3':   AnalogIn(self.mcp, MCP.P1), # Slot 2
            'MQ5':   AnalogIn(self.mcp, MCP.P2), # Slot 3
            'MQ7':   AnalogIn(self.mcp, MCP.P3), # Slot 4
            'MQ8':   AnalogIn(self.mcp, MCP.P4), # Slot 5
            'MQ135': AnalogIn(self.mcp, MCP.P5)  # Slot 6
        }

    def read_voltages(self):
        """
        Read all sensors and return a list of voltages.
        Order: [MQ2, MQ3, MQ5, MQ7, MQ8, MQ135]
        """
        try:
            return [
                self.sensors['MQ2'].voltage,
                self.sensors['MQ3'].voltage,
                self.sensors['MQ5'].voltage,
                self.sensors['MQ7'].voltage,
                self.sensors['MQ8'].voltage,
                self.sensors['MQ135'].voltage
            ]
        except Exception as e:
            print(f"MCP3008 Read Error: {e}")
            # Return a list of zeros to prevent crash
            return [0.0] * 6