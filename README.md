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
