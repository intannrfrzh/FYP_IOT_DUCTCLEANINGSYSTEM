#import all libraries

import paho.mqtt.client as mqtt  # pip install paho-mqtt

import time

import RPi.GPIO as GPIO



# Setup GPIO

GPIO.setmode(GPIO.BCM)

servo_pin = 17

GPIO.setup(servo_pin, GPIO.OUT)



# Set up PWM for controlling the servo

servo = GPIO.PWM(servo_pin, 50)  # 50Hz (standard for servos)

servo.start(0)  # Initialize the servo at position 0



# MQTT details

port = 1883

mqttBroker = "10.26.30.33"

client = mqtt.Client("Servo")

client.username_pw_set(username="umpfk", password='ump%fkiot4335')

client.keep_alive_interval = 60  # Keep connection alive for 60 seconds



MQTT_control = "flex/command"



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



        # Map the flex value (10 to 40) to servo angle (0 to 140)

        in_min, in_max = 20, 37

        out_min, out_max = 0, 140



        # Control the servo motor with the calculated servo_angle

        servo_angle = out_min + (float(dataValue - in_min) / float(in_max - in_min) * (out_max- out_min))

        print(f"Mapped servo angle: {servo_angle}")

            

        # Convert the servo angle to PWM duty cycle

        dutyCycle = (servo_angle / 18) + 2  # Map angle (0-180) to duty cycle (2-12)

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

    servo.stop()

    GPIO.cleanup()

    client.disconnect()

    print("GPIO and MQTT resources cleaned up.")

