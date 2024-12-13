# Posture Pal Hardware

Welcome to the **Posture Pal Hardware** repository, the core of the hardware components powering the Posture Pal system. This project integrates sensors, actuators, and microcontrollers to create a smart device that monitors and provides real-time feedback on user posture, enhancing ergonomics and boosting confidence.

---

## <img src="https://emojigraph.org/media/microsoft/woman-technologist_1f469-200d-1f4bb.png" alt="Technologies" width="40"> Technologies Used

<code><a href="https://www.raspberrypi.com/" target="_blank"> <img height="100" src="https://www.vectorlogo.zone/logos/raspberrypi/raspberrypi-ar21.svg"></a></code>
<code><a href="https://www.python.org/" target="_blank"> <img height="100" src="https://www.vectorlogo.zone/logos/python/python-ar21.svg"></a></code>
<code><a href="https://pubnub.com/" target="_blank"> <img height="100" src="https://getvectorlogo.com/wp-content/uploads/2020/03/pubnub-vector-logo.png"></a></code>

---

## Features
- **Integrated Sensors**: Includes the BNO055 orientation sensor for posture detection and the DHT22 sensor for monitoring environmental conditions.
- **Real-Time Feedback**: Delivers posture alerts via vibrations and sound.
- **Actuators**: Features a vibration motor for haptic feedback and a piezo buzzer for audible alerts.
- **Raspberry Pi 4 Model B**: Serves as the central system for processing and communication.

---

## Architecture
### Hardware Components
- **BNO055 Orientation Sensor**: Tracks posture and orientation with precision.
- **DHT22 Sensor**: Monitors temperature and humidity inside the device.
- **Piezo Buzzer**: Emits sound alerts for poor posture.
- **Vibration Motor**: Provides haptic feedback when slouching is detected.
- **ESP8266 Microcontroller**: Processes sensor data and communicates with the central server.
- **Raspberry Pi 4 Model B**: Acts as a backup system for processing and communication.

### Software Components
Initially, the hardware system was built using an **ESP8266 Microcontroller** for processing sensor data and communication. However, as the ESP8266 stopped working the system was shifted to use the **Raspberry Pi 4 Model B** as the primary processing unit. The Raspberry Pi enables enhanced processing power and better integration with sensors and communication protocols.

- **Python Scripts**: Manages sensor control and processing on the Raspberry Pi.
- **PubNub**: Enables real-time communication between hardware and the central application.
- **Arduino C++ was initially used**: Programs the ESP8266 to handle sensor data.
---

## Installation
### Prerequisites
- Python: Installed on the Raspberry Pi (3.7.3 or later).
- PubNub Account: For real-time communication setup.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Posture-Pal/Hardware.git
   cd Hardware
   ```

2. **Setup Raspberry Pi**:
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the `sensors.py` script:
     ```bash
     python sensors.py
     ```

3. **Configure PubNub**:
   - Update PubNub credentials in the `.env` file.
   - Ensure proper channel configuration for real-time communication.

---

## Usage
1. Connect the sensors to the Raspberry Pi.
2. Power on the device and ensure it is connected to Wi-Fi.
3. Calibrate the sensors using the `calibrate()` function in the code.
4. Use the device to monitor posture in real-time.
5. Check data and alerts on the central Posture Pal application.

---

## Acknowledgments
1. **Adafruit Libraries**: For sensor integration and control.
2. **PubNub**: For seamless real-time communication.
3. **Raspberry Pi Foundation**: For providing a robust platform for processing and communication.

---

Feel free to reach out for support or open an issue in the GitHub repository. Thank you for using Posture Pal Hardware!
