import time
import board
import adafruit_dht
import adafruit_bno055
import json
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import uuid
import RPi.GPIO as GPIO  # For GPIO control

# GPIO Pin Setup
BUZZER_PIN = 24
VIBRATION_MOTOR_PIN = 23

# GPIO Initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(VIBRATION_MOTOR_PIN, GPIO.OUT)

# Initialize the DHT22 sensor
dht_sensor = adafruit_dht.DHT22(board.D4)

# Initialize the BNO055 sensor (I2C)
i2c = board.I2C()
bno = adafruit_bno055.BNO055_I2C(i2c)

# PubNub Configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-90478427-a073-49bc-b402-ba4903894284"
pnconfig.publish_key = "pub-c-ef699d1a-d6bd-415f-bb21-a5942c7afc1a"
pnconfig.ssl = False
pnconfig.uuid = str(uuid.uuid4())
pubnub = PubNub(pnconfig)
channel = "Posture-Pal"

def beep(repeat):
    for i in range(repeat):
        for pulse in range(60):
            GPIO.output(BUZZER_PIN, True)
            time.sleep(0.001)
            GPIO.output(BUZZER_PIN, False)
            time.sleep(0.001)
        time.sleep(0.05)

def activate_actuators(duration=5):
    """
    Turn on the buzzer and vibration motor for a specified duration.
    """
    print(f"Activating actuators for {duration} seconds...")
#    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    #beep(5)
    GPIO.output(VIBRATION_MOTOR_PIN, GPIO.HIGH)
    time.sleep(duration)
   # GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(VIBRATION_MOTOR_PIN, GPIO.LOW)
    print("Actuators deactivated.")

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

                # Publish data to PubNub
                envelope = pubnub.publish().channel(channel).message(message).sync()
                #print(f"Published to PubNub: {message}")

                # Example condition to activate actuators
                #if roll > 30 or pitch > 30:  # Replace with your actual condition
                    #activate_actuators()

            except RuntimeError as error:
                print(error.args[0])

            time.sleep(.5)

    finally:
        GPIO.cleanup()  # Ensure GPIO is cleaned up on exit

if __name__ == "__main__":
    main()