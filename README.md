- _creator : INTAN NURFARIZAH RAMLI_
- _purpose : to upload my fyp's code for reference purpose. Not to be used until 3 years after the publication._
- _The system is built within one semester(6 months) where half of the semester dedicated for the brainstorming and researching while the remaining semester for building the prototype._

_**++file_name(microcontroller/microprocessor)||(language) : purpose++**_
1. arm(raspi)||(python): folder that contain all the code in raspi for arm(servo) and sensors;
2. PSM_Dashboard.json (node-red)||(java): online dashboard which helps the user to monitor, control the rover, see the output of the sensor, and to visualise the graphs based on output;
3. cleaningsystemdb(mysql)||(sql): system database which contain all data from the sensors, and also data for graph;
4. espduinoflex.ino(NODE-MCU ESP8266)||(java): for flex sensor to send input to move the servo on the rover;
5. mqtt.ino(WEMOS LOLIN D32 V2)||(java): for motor movement;
6. rpi_camtest.py(raspi)||(python): code to stream the camera from raspi to the online dashboard;

**Simple introduction:-**
This cleaning system is built for an air duct usage, which will serve as both monitoring and cleaning. The cleaning system consist of a rover with a cleaning arm attached ontop, a glove with flex sensor to command the cleaning arm and an online dashboard which powered/accessed through node-red. The system are built with Raspberry Pi 4(body and the one responsible for the connection between all of the system, db and dashboard), NODE-MCU ESP8266(attached to the back of the glove and flex sensor) and WEMOS LOLIN D32 V2(to move the 4 motors of the rover).

