#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Motor pins (Wemos D1 Mini uses specific GPIO numbers for D pins)
#define MOTOR1_A_PIN 14 // D5
#define MOTOR1_B_PIN 12 // D6
#define MOTOR2_A_PIN 13 // D7
#define MOTOR2_B_PIN 15 // D8

// WiFi setting
//const char *ssid = "LAB_IOT_2.4";
//const char *password = "abc12345";
//wifi laptop
const char *ssid = "NKMTYT";
const char *password = "onlyforTEST!";

// MQTT Broker setting
//const char *mqtt_broker = "10.26.30.33"; // internal MQTT broker
const char *mqtt_broker = "103.53.35.135"; // External MQTT broker
const char *mqtt_username = "umpfk";
const char *mqtt_password = "ump%fkiot4335";
const int mqtt_port = 1883;
String clientName = "rover";

// MQTT Topics
const char *topicCommand = "rover/status";
const char *topicConfirm = "rover/received";

// Initialisation
WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(115200);

  // Configure motor pins as outputs
  pinMode(MOTOR1_A_PIN, OUTPUT);
  pinMode(MOTOR1_B_PIN, OUTPUT);
  pinMode(MOTOR2_A_PIN, OUTPUT);
  pinMode(MOTOR2_B_PIN, OUTPUT);

  // Stop motors initially
  stopMotors();

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
      client.subscribe(topicCommand);
      Serial.print("Subscribed to topic: ");
      Serial.println(topicCommand);
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

  if (String(topic) == topicCommand) {
    if (message == "1") {
      Serial.println("Command: Move Forward");
      moveForward();
    } 
    else if (message == "2") {
      Serial.println("Command: Move Backward");
      moveBackward();
    } 
    else if (message == "3") {
      Serial.println("Command: Turn Right");
      turnRight();
    } 
    else if (message == "4") {
      Serial.println("Command: Turn Left");
      turnLeft();
    } 
    else {
      Serial.println("Command: Stop");
      stopMotors();
    }
    stopMotors();

    // Send confirmation back
    client.publish(topicConfirm, message.c_str());
    Serial.print("Confirmation sent: ");
    Serial.println(message);
  }
}

// Movement functions
void moveForward() {
  digitalWrite(MOTOR1_A_PIN, HIGH);
  digitalWrite(MOTOR1_B_PIN, LOW);
  digitalWrite(MOTOR2_A_PIN, LOW);
  digitalWrite(MOTOR2_B_PIN, HIGH);
  Serial.println("Motors moving forward.");
  delay(1000);
}

void moveBackward() {
  digitalWrite(MOTOR1_A_PIN, LOW);
  digitalWrite(MOTOR1_B_PIN, HIGH);
  digitalWrite(MOTOR2_A_PIN, HIGH);
  digitalWrite(MOTOR2_B_PIN, LOW);
  Serial.println("Motors moving backward.");
  delay(1000);
}

void turnRight() {
  digitalWrite(MOTOR1_A_PIN, LOW);
  digitalWrite(MOTOR1_B_PIN, HIGH);
  digitalWrite(MOTOR2_A_PIN, LOW);
  digitalWrite(MOTOR2_B_PIN, HIGH);
  Serial.println("Motors turning right.");
  delay(1000);
}

void turnLeft() {
  digitalWrite(MOTOR1_A_PIN, HIGH);
  digitalWrite(MOTOR1_B_PIN, LOW);
  digitalWrite(MOTOR2_A_PIN, HIGH);
  digitalWrite(MOTOR2_B_PIN, LOW);
  Serial.println("Motors turning left.");
  delay(1000);
}

void stopMotors() {
  digitalWrite(MOTOR1_A_PIN, LOW);
  digitalWrite(MOTOR1_B_PIN, LOW);
  digitalWrite(MOTOR2_A_PIN, LOW);
  digitalWrite(MOTOR2_B_PIN, LOW);
  Serial.println("Motors stopped.");
}
