import time
import os
import csv
import board
from datetime import datetime

# --- IMPORT CUSTOM CLASSES ---
from DHT22 import DHT22Sensor
from MCP3008 import MultiGasSensor

# --- CONFIGURATION ---
# Change filepath here
# "~" Example Home (VD: /home/azure)
LOG_DIR = os.path.expanduser("~/FTP/data")  

INTERVAL_SEC = 5            # Data logging interval (seconds)
FILE_DURATION_SEC = 15 * 60 # Duration per file (15 minutes)

# Check folder ~/FTP/data 
if not os.path.exists(LOG_DIR):
    try:
        os.makedirs(LOG_DIR)
        print(f"Directory created: {LOG_DIR}")
    except OSError as e:
        print(f"Error creating directory {LOG_DIR}: {e}")
        # Prevent crash
        LOG_DIR = "logs" 
        os.makedirs(LOG_DIR, exist_ok=True)

def get_new_filename():
    """Generate a filename based on the current timestamp."""
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Saved file with /home/azure/FTP/data/data_2023-xx-xx.csv
    return os.path.join(LOG_DIR, f"data_{now_str}.csv")

def main():
    print(f"System initializing... Data will be saved to: {LOG_DIR}")

    # 1. Initialize Hardware
    try:
        dht = DHT22Sensor(board.D23)
        gas = MultiGasSensor()
        print(">> Hardware ready!")
    except Exception as e:
        print(f"Hardware Initialization Error: {e}")
        return

    # CSV Column Headers
    csv_header = [
        "Timestamp", 
        "Temp(C)", "Hum(%)", 
        "MQ2(V)", "MQ3(V)", "MQ5(V)", "MQ7(V)", "MQ8(V)", "MQ135(V)"
    ]

    current_filename = None
    start_time_file = 0

    print("Starting data logging... (Press CTRL+C to stop)")

    try:
        while True:
            # --- FILE ROTATION LOGIC ---
            if current_filename is None or (time.time() - start_time_file >= FILE_DURATION_SEC):
                current_filename = get_new_filename()
                start_time_file = time.time()
                
                with open(current_filename, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(csv_header)
                print(f"\n[NEW FILE] Logging to: {current_filename}")

            # --- DATA ACQUISITION ---
            dht.read()
            gas_values = gas.read_voltages()
            
            # --- DATA FORMATTING ---
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [timestamp, f"{dht.temperature:.1f}", f"{dht.humidity:.1f}"]
            row.extend([f"{v:.2f}" for v in gas_values])

            # --- SAVE TO FILE ---
            with open(current_filename, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)

            print(f"Saved: {row}")

            time.sleep(INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        dht.close()

if __name__ == "__main__":
    main()