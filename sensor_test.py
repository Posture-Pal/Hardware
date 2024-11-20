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

                # Read orientation data from BNO055
                roll, pitch, yaw = bno.euler

                # Check for valid data
                if temperature is None or humidity is None:
                    print("Failed to read from DHT sensor!")
                else:
                    print(f"Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %")

                if roll is None or pitch is None or yaw is None:
                    print("Failed to read from BNO055 sensor!")
                else:
                    print(f"Orientation - Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}")

                message = json.dumps({
                    "temperature": temperature,
                    "humidity": humidity,
                    "roll": roll,
                    "pitch": pitch,
                    "yaw": yaw
                })

                print(message)


            except RuntimeError as error:
                print(error.args[0])

            time.sleep(0.5)

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()