#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

#define DHTPIN 14       
#define DHTTYPE DHT22

// Create the DHT and BNO055 sensor objects
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup() {
  // Starting serial communication
  Serial.begin(115200);

  // Initializing the DHT22 sensor
  dht.begin();
  delay(2000);
  
  // Initialize the BNO055 sensor
  if (!bno.begin()) {
    Serial.println("No BNO055 detected, check wiring!");
    while (1);
  }
  
  // Using external crystal for better precision
  bno.setExtCrystalUse(true);
}

void loop() {
  // Read data from the temperature sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if the DHT22 data is valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, ");
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }

  // Read data from the BNO055 sensor
  sensors_event_t event;
  bno.getEvent(&event);

  // Print Euler angles (orientation)
  Serial.print("Orientation: ");
  Serial.print("Roll: ");
  Serial.print(event.orientation.x);  // X-axis 
  Serial.print(", Pitch: ");
  Serial.print(event.orientation.y);  // Y-axis 
  Serial.print(", Yaw: ");
  Serial.println(event.orientation.z); // Z-axis
  
  float pitch = event.orientation.y;
  if (pitch > 40) {
    Serial.println("Warning: Bad posture detected! Please sit upright.");
  }

  delay(2000);
}
