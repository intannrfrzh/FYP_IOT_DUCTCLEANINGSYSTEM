#import all libraries
import paho.mqtt.client as mqtt  # pip install paho-mqtt
import time
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
#motor for brush
Motor1A = 24 #IN1
Motor1B = 23 #IN2
Motor1E = 25 #EN1
#servomotor
servo_pin = 17

#all pins as output
GPIO.setup(Motor1A, GPIO.OUT) 
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)

# Set up PWM for controlling the servo
servo = GPIO.PWM(servo_pin, 50)  # 50Hz (standard for servos)
servo.start(0)  # Initialize the servo at position 0

# MQTT details
port = 1883
#mqttBroker = "10.26.30.33" #dalam
mqttBroker = "103.53.35.135" #luar
client = mqtt.Client("Servo")
client.username_pw_set(username="umpfk", password='ump%fkiot4335')
client.keep_alive_interval = 60  # Keep connection alive for 60 seconds

#mqtt topic
MQTT_brushcontrol = "servo/brush"
MQTT_status = "servo/brushStat"
MQTT_servocontrol = "flex/command"

# Create MQTT connection to broker
client.connect(mqttBroker, port)

# Subscribe to brush control and servo control topic
client.subscribe(MQTT_brushcontrol, 1)
client.subscribe(MQTT_servocontrol, 1)

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
    print(f"Message received on topic {msg.topic} with QoS {msg.qos} and value {msg.payload}")
    try:
        dataValue = int(msg.payload.decode('UTF-8'))
        print(f"received value: {dataValue}")

        # Control brush motor based on input (0=stop, 1=start)
        if msg.topic == MQTT_brushcontrol:
            if dataValue == 1:  # Turn motor on
                GPIO.output(Motor1A, GPIO.HIGH)
                GPIO.output(Motor1B, GPIO.LOW)
                GPIO.output(Motor1E, GPIO.HIGH)
                client.publish(MQTT_status, 1, 0, retain=True)  # Publish status
                print("Brush motor ON")
            else:  # Turn motor off
                GPIO.output(Motor1A, GPIO.LOW)
                GPIO.output(Motor1B, GPIO.LOW)
                GPIO.output(Motor1E, GPIO.LOW)
                client.publish(MQTT_status, 0, 0, retain=True)  # Publish status
                print("Brush motor OFF")
        
        # Control the servo motor (map flex value to servo angle)
        elif msg.topic == MQTT_servocontrol:
            # Map the flex value (10 to 40) to servo angle (0 to 140)
            in_min, in_max = 20, 37
            out_min, out_max = 0, 140
            servo_angle = out_min + (float(dataValue - in_min) / float(in_max - in_min) * (out_max - out_min))
            print(f"Mapped servo angle: {servo_angle}")
            dutyCycle = (servo_angle / 18) + 2  # Map angle (0-140) to duty cycle (2-12)
            servo.ChangeDutyCycle(dutyCycle)  # Move the servo
            print(f"Moving servo to {servo_angle} degrees")
        
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

