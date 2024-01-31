#include <Arduino.h>
#include <Servo.h>

int receivedCommand = -1; // Variable to store received command
int receivedAngle = 0;    // Variable to store received angle for the servo motor

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

//1100 us is Full Throttle Reverse 
//1500 us is Stopped
//1900 us is Full Throttle Forward

//Motor thrust idle value (May need fine tuning)
int idleThrust = 1540; 
int noThrust = 1500;

void setup() {
  Serial.begin(115200);

  // Set the minimum and maximum pulse width for servos
  frontServo.attach(FrontServoPin, 500, 2500);
  backServo.attach(BackServoPin, 500, 2500);

  // Attach the motor ESCs
  frontMotorESC.attach(MotorThrustPin); //Both motors are connected to this one pin for now.
  //backMotorESC.attach(MotorThrustPin);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Process each available command in the buffer
  while (Serial.available() > 0) {
    receivedCommand = Serial.parseInt();

    switch (receivedCommand) {
      case 1: // Motor ON
        frontMotorESC.writeMicroseconds(idleThrust); //Turn both motors on to idle thrust
        backMotorESC.writeMicroseconds(idleThrust);
        digitalWrite(LED_BUILTIN, HIGH); //Turn ON on-board LED to represent motor on.
        break;

      case 2: // Motor OFF
        frontMotorESC.writeMicroseconds(noThrust); //Turn both motors off
        backMotorESC.writeMicroseconds(noThrust);
        digitalWrite(LED_BUILTIN, LOW); //Turn OFF on-board LED to represent motor off.
        break;

      case 3: // Set Servo Angle
        if (Serial.available() > 0) {
          receivedAngle = Serial.parseInt();
          if(receivedAngle >= 0 && receivedAngle <= 180) {
            frontServo.write(receivedAngle); //Set the angle of both servos
            backServo.write(receivedAngle);
          }
        }
        break;
    }
  }
}
