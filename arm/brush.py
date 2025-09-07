#import all libraries
import paho.mqtt.client as mqtt  # pip install paho-mqtt
import time
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
Motor1A = 24 #IN1
Motor1B = 23 #IN2
Motor1E = 25 #EN1

#all pins as output
GPIO.setup(Motor1A, GPIO.OUT) 
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

# MQTT details
port = 1883
#mqttBroker = "10.26.30.33" #dalam
mqttBroker = "103.53.35.135" #luar
client = mqtt.Client("Brush")
client.username_pw_set(username="umpfk", password='ump%fkiot4335')
client.keep_alive_interval = 60  # Keep connection alive for 60 seconds

#mqtt topic
MQTT_control = "servo/brush"
MQTT_status = "servo/brushStat"

# Create MQTT connection to broker
client.connect(mqttBroker, port)

# Subscribe to the control topic
client.subscribe(MQTT_control, 1)

# CALLBACK FUNCTIONS
def on_connect(client, userdata, flags, rc):
    """Callback for successful connection to the MQTT broker."""
    if rc == 0:
        print("Connected successfully.")
    else:
        print(f"Connection failed with code {rc}.")

def on_publish(client, userdata, mid):
    """Callback for successful publish to an MQTT topic."""
    print(f"Message with mid {mid} published.")

def on_message(client, userdata, msg):
    """Callback for receiving a message from the subscribed MQTT topic."""
    print(f"Message received on topic {msg.topic} with QoS {msg.qos} and payload {msg.payload}")
    try:
        dataValue = int(msg.payload.decode('UTF-8'))
        print(f"Flex value: {dataValue}")

        #move motor based on input (0=stop, 1=start)
        if (dataValue == 1): #turn motor on
            GPIO.output(Motor1A, GPIO.HIGH)
            GPIO.output(Motor1B, GPIO.LOW)
            GPIO.output(Motor1E, GPIO.HIGH)
            client.publish(MQTT_status,1, 0, retain = True) #publish status    
        else: #turn motor off
            GPIO.output(Motor1A, GPIO.LOW)
            GPIO.output(Motor1B, GPIO.LOW)
            GPIO.output(Motor1E, GPIO.LOW) 
            client.publish(MQTT_status,0, 0, retain = True) #publish status 

    except ValueError:
        print("Invalid payload format, not an integer.")


def on_disconnect(client, userdata, rc):
    """Callback for handling disconnection from the MQTT broker."""
    if rc != 0:
        print(f"Unexpected disconnection. Reconnecting... (rc={rc})")
        time.sleep(1)
        client.reconnect()

# Assign event callbacks
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.on_disconnect = on_disconnect

# Main loop
try:
    print("Listening for messages...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Program stopped.")
finally:
    # Clean up GPIO and disconnect the MQTT client
    print("stop")
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.cleanup()
    client.disconnect()
    print("GPIO and MQTT resources cleaned up.")

