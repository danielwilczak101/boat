#include <Arduino.h>
#include <Servo.h>

int receivedCommand = -1; // Variable to store received command
int receivedAngle = 0;    // Variable to store received angle for the servo motor
int receivedThrottle = 1500; // Variable to store received throttle value for the motor

//----------------Boat Setup START------------------------------
//Motor and Servo Pins 
#define FrontServoPin 5 //Connected to GP5
#define BackServoPin 4 //Connected to GP4
#define MotorThrustPin 15 //Connected to GP15

//Set up servo objects 
Servo frontServo;
Servo backServo;
Servo frontMotorESC;
Servo backMotorESC;

//Motor thrust idle and no thrust values
int idleThrust = 1540; 
int noThrust = 1500;

void setup() {
  Serial.begin(115200);

  // Set the minimum and maximum pulse width for servos
  frontServo.attach(FrontServoPin, 500, 2500);
  backServo.attach(BackServoPin, 500, 2500);

  // Attach the motor ESCs
  frontMotorESC.attach(MotorThrustPin); //Both motors are connected to this one pin for now.
  //backMotorESC.attach(MotorThrustPin); // Commented out as it seems not used currently

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Process each available command in the buffer
  while (Serial.available() > 0) {
    receivedCommand = Serial.parseInt();

    switch (receivedCommand) {
      case 1: // Motor ON
        if (Serial.available() > 0) {
          receivedThrottle = Serial.parseInt();
          // Ensure throttle value is within the expected range
          receivedThrottle = constrain(receivedThrottle, 1300, 1500);
        }
        frontMotorESC.writeMicroseconds(receivedThrottle); // Apply throttle value to motor
        // backMotorESC.writeMicroseconds(receivedThrottle); // Uncomment if using a separate back motor control
        digitalWrite(LED_BUILTIN, HIGH); // Turn ON on-board LED to represent motor on.
        break;

      case 2: // Motor OFF
        frontMotorESC.writeMicroseconds(noThrust); // Turn both motors off
        // backMotorESC.writeMicroseconds(noThrust); // Uncomment if using a separate back motor control
        digitalWrite(LED_BUILTIN, LOW); // Turn OFF on-board LED to represent motor off.
        break;

      case 3: // Set Servo Angle
        if (Serial.available() > 0) {
          receivedAngle = Serial.parseInt();
          if(receivedAngle >= 0 && receivedAngle <= 180) {
            frontServo.write(receivedAngle); // Set the angle of both servos
            backServo.write(receivedAngle);
          }
        }
        break;
    }
  }
}
