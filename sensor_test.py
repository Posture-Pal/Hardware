import time
import board
import adafruit_dht
import adafruit_bno055
import json
import RPi.GPIO as GPIO  

# Initialize the DHT22 sensor
dht_sensor = adafruit_dht.DHT22(board.D4)

# Initialize the BNO055 sensor (I2C)
i2c = board.I2C()
bno = adafruit_bno055.BNO055_I2C(i2c)

def main():
    try:
        while True:
            try:
                # Read temperature and humidity from DHT22
                temperature = dht_sensor.temperature
                humidity = dht_sensor.humidity

                # Read pitch and gravity vector from BNO055
                # Extract pitch
                pitch = bno.euler[1] if bno.euler else None  
                
                gravity_vector = bno.gravity

                # Check for valid data
                if temperature is not None and humidity is not None:
                    print(f"Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %")
                else:
                    print("Failed to read from DHT sensor!")

                if pitch is not None and gravity_vector is not None:
                    print(f"Pitch: {pitch:.2f}, Gravity Vector: {gravity_vector}")
                else:
                    print("Failed to read from BNO055 sensor!")

                # Create and print a JSON message
                message = json.dumps({
                    "temperature": temperature,
                    "humidity": humidity,
                    "pitch": pitch,
                    "gravity_vector": gravity_vector
                })
                print(message)

            except RuntimeError as error:
                print(f"RuntimeError: {error.args[0]}")

            time.sleep(0.5)

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
