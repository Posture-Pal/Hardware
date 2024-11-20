import time
import board
import adafruit_dht
import adafruit_bno055
import json
import RPi.GPIO as GPIO  

# Initialize sensors
dht_sensor = adafruit_dht.DHT22(board.D4)
i2c = board.I2C()
bno = adafruit_bno055.BNO055_I2C(i2c)

#TODO Will set these value when user calibrate
# Hardcoded thresholds
TEMP_OVERHEAT = 37.5  # Celsius
TEMP_COLD = 15.0      # Celsius
HUMID_HIGH = 70.0     # Percent
HUMID_LOW = 30.0      # Percent
PITCH_THRESHOLD = 20.0  # Degrees
GRAVITY_THRESHOLD = [0, 0, 1]  # Expected gravity vector

def check_thresholds(temperature, humidity, pitch, gravity_vector):
    # Determine temperature status
    if temperature > TEMP_OVERHEAT:
        temperature_status = "hot"
    elif temperature < TEMP_COLD:
        temperature_status = "cold"
    else:
        temperature_status = "normal"

    # Determine humidity status
    if humidity > HUMID_HIGH:
        humidity_status = "high"
    elif humidity < HUMID_LOW:
        humidity_status = "low"
    else:
        humidity_status = "normal"

    # Determine slouch status
    slouch_detected = abs(pitch) > PITCH_THRESHOLD

    return {
        "slouch": slouch_detected,
        "temperature_status": temperature_status,
        "temperature": temperature,
        "humidity_status": humidity_status,
        "humidity": humidity
    }

def main():
    try:
        while True:
            try:
                # Read sensor data
                temperature = dht_sensor.temperature
                humidity = dht_sensor.humidity
                pitch = bno.euler[1] if bno.euler else None
                gravity_vector = bno.gravity

                # Validate data
                if temperature is not None and humidity is not None and pitch is not None:
                    results = check_thresholds(temperature, humidity, pitch, gravity_vector)

                    # Print JSON only when slouch or abnormal conditions detected
                    if results["slouch"] or results["temperature_status"] != "normal":
                        print(json.dumps(results))

            except RuntimeError as error:
                print(f"RuntimeError: {error.args[0]}")

            time.sleep(0.5)

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
