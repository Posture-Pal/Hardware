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

VIBRATION_PIN = 23
BUZZER_PIN = 24

#TODO Will set these value when user calibrate
# Default thresholds
DEFAULT_TEMP_OVERHEAT = 37.5  # Celsius
DEFAULT_TEMP_COLD = 15.0      # Celsius
DEFAULT_HUMID_HIGH = 80.0     # Percent
DEFAULT_HUMID_LOW = 20.0      # Percent
DEFAULT_PITCH = 0.0           # Degrees (upright posture)
DEFAULT_GRAVITY = [0, 0, 1]   # Default gravity vector (upright)

thresholds = {
    "temp_overheat": DEFAULT_TEMP_OVERHEAT,
    "temp_cold": DEFAULT_TEMP_COLD,
    "humid_high": DEFAULT_HUMID_HIGH,
    "humid_low": DEFAULT_HUMID_LOW,
    "pitch": DEFAULT_PITCH,
    "gravity": DEFAULT_GRAVITY
}

# Modes (default to True)
sound_mode = True
vibration_mode = True

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(VIBRATION_PIN, GPIO.OUT)

def beep(repeat):
    for _ in range(repeat):
        for _ in range(60): 
            GPIO.output(BUZZER_PIN, True)
            time.sleep(0.001) 
            GPIO.output(BUZZER_PIN, False)
            time.sleep(0.001)
        time.sleep(0.02)  

def turn_on_buzzer():
    beep(4)

def turn_off_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def turn_on_vibration():
    GPIO.output(VIBRATION_PIN, GPIO.HIGH)

def turn_off_vibration():
    GPIO.output(VIBRATION_PIN, GPIO.LOW)

def get_user_modes():
    global sound_mode, vibration_mode

    # Prompt user for modes, defaulting to True if they input nothing
    sound_input = input("Do you want to enable sound? (yes/no): ").strip().lower()
    if sound_input == "yes":
        sound_mode = True
    elif sound_input == "no":
        sound_mode = False

    vibration_input = input("Do you want to enable vibration? (yes/no): ").strip().lower()
    if vibration_input == "yes":
        vibration_mode = True
    elif vibration_input == "no":
        vibration_mode = False

    print(f"Sound Mode: {sound_mode}, Vibration Mode: {vibration_mode}")

def calibrate_posture():
    print("Calibrating upright posture...")
    pitch = bno.euler[1] if bno.euler else None
    gravity_vector = bno.gravity

    if pitch is None or gravity_vector is None:
        print("Failed to calibrate: Sensor data not available!")
        return

    thresholds["pitch"] = pitch
    thresholds["gravity"] = gravity_vector

    print("Calibration complete. Sending threshold data:")
    print(json.dumps(thresholds, indent=2))

def check_slouch(pitch, gravity_vector):
    pitch_diff = abs(pitch - thresholds["pitch"])
    gravity_diff = sum(abs(g - t) for g, t in zip(gravity_vector, thresholds["gravity"]))

    return pitch_diff > 20 or gravity_diff > 0.2

def check_environment_status(temperature, humidity):
    # Determine temperature status
    if temperature > thresholds["temp_overheat"]:
        temperature_status = "hot"
    elif temperature < thresholds["temp_cold"]:
        temperature_status = "cold"
    else:
        temperature_status = "normal"

    # Determine humidity status
    if humidity > thresholds["humid_high"]:
        humidity_status = "high"
    elif humidity < thresholds["humid_low"]:
        humidity_status = "low"
    else:
        humidity_status = "normal"

    return temperature_status, humidity_status

def monitor_posture():
    try:
        while True:
            temperature = dht_sensor.temperature
            humidity = dht_sensor.humidity
            pitch = bno.euler[1] if bno.euler else None
            gravity_vector = bno.gravity

            if temperature is None or humidity is None or pitch is None or gravity_vector is None:
                print("Sensor data not available!")
                continue

            temperature_status, humidity_status = check_environment_status(temperature, humidity)
            slouch_detected = check_slouch(pitch, gravity_vector)

            # Controlling buzzer and vibration motor based on slouch detection and modes
            if slouch_detected:
                if sound_mode:
                    turn_on_buzzer()
                if vibration_mode:
                    turn_on_vibration()
            else:
                turn_off_buzzer()
                turn_off_vibration()

            if slouch_detected or temperature_status != "normal" or humidity_status != "normal":
                result = {
                    "slouch": slouch_detected,
                    "temperature_status": temperature_status,
                    "temperature": temperature,
                    "humidity_status": humidity_status,
                    "humidity": humidity
                }
                print(json.dumps(result, indent=2))
            time.sleep(0.5)
    except RuntimeError as error:
        print(f"RuntimeError: {error.args[0]}")
    finally:
        GPIO.cleanup()


#TODO : will change it to get data from pubnub channel
def main():
    print("Do you want to calibrate your upright posture? (yes/no)")
    response = input().strip().lower()

    if response == "yes":
        calibrate_posture()
    else:
        print("Using default thresholds.")

    get_user_modes()
    print("Starting posture and environment monitoring...")
    monitor_posture()

if __name__ == "__main__":
    setup_gpio()
    main()
