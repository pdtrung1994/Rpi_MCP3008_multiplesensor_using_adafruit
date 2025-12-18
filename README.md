# Raspberry Pi Air Quality Monitoring System

A Python-based data logger for Raspberry Pi that monitors air quality using multiple **MQ-series gas sensors** (via MCP3008 ADC) and a **DHT22** temperature/humidity sensor.

Data is collected synchronously and logged into CSV files with automatic file rotation every 15 minutes.

## 🚀 Features

* **Multi-Sensor Support:** Reads 6 different gas sensors and 1 environmental sensor simultaneously.
* **ADC Integration:** Uses **MCP3008** (SPI) to convert analog gas sensor signals for the Raspberry Pi.
* **Robust Logging:**
    * Saves data to CSV format (Excel compatible).
    * **Auto-rotation:** Creates a new file every 15 minutes to prevent data loss.
    * **Crash-safe:** Uses append mode to ensure data is saved even if power is cut.
* **Modular Code:** Split into classes (`DHT22`, `MCP3008`, `Main`) for easy maintenance.
* **Error Handling:** Automatic retries for DHT sensor reading failures and hardware connection checks.

## 🛠 Hardware Requirements

1.  **Raspberry Pi** (3B, 4B, Zero W, or 5).
2.  **DHT22** (AM2302) Temperature & Humidity Sensor.
3.  **MCP3008** 8-Channel 10-bit ADC (Analog-to-Digital Converter).
4.  **MQ Gas Sensors** (Analog output):
    * MQ-2 (Smoke/LPG)
    * MQ-3 (Alcohol/Ethanol)
    * MQ-5 (Natural Gas/LPG)
    * MQ-7 (Carbon Monoxide)
    * MQ-8 (Hydrogen)
    * MQ-135 (Air Quality/NH3/Benzene)
5.  Breadboard and Jumper Wires.

## 🔌 Wiring Guide

### 1. DHT22 Sensor
| DHT Pin | Raspberry Pi Pin |
| :--- | :--- |
| VCC | 3.3V (Pin 1) |
| Data | **GPIO 23** (Pin 16) |
| GND | GND (Pin 6) |

*(Note: If using a raw DHT22 sensor without a module, add a 4.7kΩ - 10kΩ pull-up resistor between VCC and Data)*

### 2. MCP3008 (SPI Connection)
| MCP3008 Pin | Raspberry Pi Pin | Description |
| :--- | :--- | :--- |
| VDD | 3.3V | Power Supply |
| **VREF** | **3.3V** | **Crucial for Pi Safety** |
| AGND | GND | Analog Ground |
| CLK | GPIO 11 (SCLK) | SPI Clock |
| DOUT | GPIO 9 (MISO) | SPI MISO |
| DIN | GPIO 10 (MOSI) | SPI MOSI |
| CS/SHDN | GPIO 8 (CE0) | Chip Select |
| DGND | GND | Digital Ground |

### 3. MQ Sensors -> MCP3008
**Power Note:** MQ sensors require **5V** to heat up properly.
* **VCC:** Connect to Raspberry Pi **5V**.
* **GND:** Connect to Common GND.
* **A0 (Analog Out):** Connect to MCP3008 Channels as follows:

| Sensor | MCP3008 Channel | Pin Number |
| :--- | :--- | :--- |
| MQ-2 | CH 0 | Pin 1 |
| MQ-3 | CH 1 | Pin 2 |
| MQ-5 | CH 2 | Pin 3 |
| MQ-7 | CH 3 | Pin 4 |
| MQ-8 | CH 4 | Pin 5 |
| MQ-135 | CH 5 | Pin 6 |

---

## ⚙️ Installation & Setup

### 1. Enable SPI Interface
The MCP3008 requires the SPI interface to be enabled on the Raspberry Pi.

```bash
sudo raspi-config

```

* Go to **Interface Options** > **SPI** > **Yes**.
* **Reboot** the Pi: `sudo reboot`.
* Verify it is active: `ls /dev/spidev*` (You should see `/dev/spidev0.0`).

### 2. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y libgpiod2

```

### 3. Install Python Libraries

We use Adafruit's CircuitPython libraries.

```bash
# For standard Raspberry Pi OS:
pip3 install adafruit-circuitpython-dht adafruit-circuitpython-mcp3xxx

# For Raspberry Pi OS (Bookworm) with managed environment:
sudo pip3 install adafruit-circuitpython-dht adafruit-circuitpython-mcp3xxx --break-system-packages

```

### 4. Clone the Code

Ensure your project folder contains these 3 files:

1. `DHT22.py`
2. `MCP3008.py`
3. `read_mq_sensor.py`

## 🏃‍♂️ Usage

Run the main script using Python 3:

```bash
python3 read_mq_sensor.py

```

### Output location

By default, the code is configured to save data to:
`~/FTP/data/` (e.g., `/home/username/FTP/data/`)

You can change this path by editing the `LOG_DIR` variable in `read_mq_sensor.py`.

### CSV Format Example

The generated CSV file will look like this:

```csv
Timestamp,Temp(C),Hum(%),MQ2(V),MQ3(V),MQ5(V),MQ7(V),MQ8(V),MQ135(V)
2023-12-18 10:00:00,25.4,60.2,0.45,0.32,0.50,0.12,0.20,0.65
2023-12-18 10:00:05,25.4,60.1,0.46,0.31,0.51,0.11,0.21,0.64

```

## 🐛 Troubleshooting

**1. `Hardware Initialization Error: /dev/spidev0.0 does not exist**`

* **Cause:** SPI is disabled.
* **Fix:** Run `sudo raspi-config`, enable SPI, and reboot.

**2. `DHT Read Error` / `Temp: 0.0**`

* **Cause:** DHT sensors are slow.
* **Fix:** The code automatically retries. If it persists, check the wiring (GPIO 23) and ensure the pull-up resistor is present.

**3. MQ Sensor values are always 3.3V**

* **Cause:** The sensor output is higher than VREF (saturation).
* **Fix:** Adjust the sensitivity potentiometer (blue knob) on the back of the MQ module until the output voltage in clean air is around 0.5V - 1.0V.

## 📜 License

This project is open-source. Feel free to modify and distribute.

```

```
