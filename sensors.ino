#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <PubNub.h> 
#include <ESP8266WiFi.h>
#include "config.h"

#define DHTPIN 14      
#define DHTTYPE DHT22    

// create the DHT and BNO055 sensor objects
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BNO055 bno = Adafruit_BNO055(55);


void setup() {
  Serial.begin(115200);

    // connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to Wi-Fi");

  // initialize PubNub
  PubNub.begin(PUBKEY, SUBKEY);

  // initialize the DHT22 sensor
  dht.begin();
  delay(2000);
  
  // initialize the BNO055 sensor
  if (!bno.begin()) {
    Serial.println("No BNO055 detected, check wiring!");
    while (1);
  }
  
  // for better precision
  bno.setExtCrystalUse(true);
}

void loop() {
  // read data from the temperature sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // check if the temperature data is valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" Â°C, ");
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }

  // read data from the orientation sensor
  sensors_event_t event;
  bno.getEvent(&event);

  // get orientation angles
  float roll = event.orientation.x;  // X-axis 
  float pitch = event.orientation.y; // Y-axis 
  float yaw = event.orientation.z;   // Z-axis 

  // print Euler angles
  Serial.print("Orientation: ");
  Serial.print("Roll: ");
  Serial.print(roll);
  Serial.print(", Pitch: ");
  Serial.print(pitch);
  Serial.print(", Yaw: ");
  Serial.println(yaw);


  // format the message as a JSON object
  String message = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + ",\"roll\":" + String(roll) + ",\"pitch\":" + String(pitch) + ",\"yaw\":" + String(yaw) + "}";

  // publish the message to PubNub
  auto result = PubNub.publish(CHANNEL_NAME, message.c_str());
  
  if (!result) {
    Serial.println("Failed to publish to PubNub.");
  } else {
    Serial.println("Published to PubNub: " + message);
  }

  delay(2000); 
}