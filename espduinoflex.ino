#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Pin connected to the flex sensor
const int flexPin = A0; //espduino pin 36

// WiFi setting
//const char *ssid = "LAB_IOT_2.4";
//const char *password = "abc12345";
const char *ssid = "NKMTYT";
const char *password = "onlyforTEST!";

// MQTT Broker setting
//const char *mqtt_broker = "10.26.30.33"; // internal MQTT broker 
const char *mqtt_broker = "103.53.35.135"; // external MQTT broker 
const char *mqtt_password = "ump%fkiot4335";
const char *mqtt_username = "umpfk";
const int mqtt_port = 1883;
String clientName = "flexSensor";

// MQTT Topics
const char *topicCommand = "flex/command";   // Command topic
const char *topicSensor = "flex/sensor";    // Flex sensor data topic

// Initialisation
WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(115200);

  // Initialize Wi-Fi and MQTT
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  reconnect();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Read flex sensor value
  int sensorValue = analogRead(flexPin); // Read analog value (0-4095 for 12-bit ADC)
  Serial.print("Flex Sensor Value: ");
  Serial.println(sensorValue);

  // Publish sensor value to MQTT
  String sensorData = String(sensorValue);
  client.publish(topicSensor, sensorData.c_str());
  Serial.println("Sensor data published to MQTT.");

  delay(1000); // Publish data every second
}

// Function to connect to Wi-Fi and MQTT Broker
void reconnect() {
  // Connect to Wi-Fi
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to Wi-Fi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nWi-Fi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  }

  // Connect to MQTT broker
  while (!client.connected()) {
    Serial.print("Connecting to MQTT broker...");
    if (client.connect(clientName.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT broker!");
      
    } else {
      Serial.print("MQTT connection failed, rc=");
      Serial.print(client.state());
      Serial.println(". Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

// Callback function for MQTT messages
void callback(char *topic, byte *payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Received message on topic '");
  Serial.print(topic);
  Serial.print("': ");
  Serial.println(message);

}
