// Include the imports for the libraries
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>

// Define the DHT sensor type and the pin it's connected to
#define DHTPIN 14        // DHT22 data pin connected to pin 14
#define DHTTYPE DHT22    // Define the sensor type as DHT22


// Create the DHT objects
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Initialize the DHT22 sensor
  Serial.begin(115200);
  dht.begin();
  delay(2000);
}

void loop() {
    // Read data from the DHT22 sensor
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

  delay(2000);  // Delay for 2 second
}
