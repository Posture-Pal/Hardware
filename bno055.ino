#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

// Create the BNO055 object
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup() {
  Serial.begin(115200);
  
  // Initialize the BNO055 sensor
  if (!bno.begin()) {
    Serial.println("No BNO055 detected, check wiring!");
    while (1);
  }
  
  // Use external crystal for better precision
  bno.setExtCrystalUse(true);
}

void loop() {
  sensors_event_t event;
  bno.getEvent(&event);

  // Print Euler angles (orientation)
  Serial.print("Orientation: ");
  Serial.print(event.orientation.x);  // X-axis
  Serial.print(" ");
  Serial.print(event.orientation.y);  // Y-axis
  Serial.print(" ");
  Serial.println(event.orientation.z); // Z-axis

  delay(1000);  // Delay for 1 second
}