#include <Arduino.h>
#include <Servo.h>

int receivedCommand = -1; // Variable to store received command

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

//Servo Direction (May need fine tuning)
int leftFront = 40;
int leftBack = 35;

int straightFront = 100;
int straightBack = 95;

int rightFront = 160;
int rightBack = 155;

//----------------Boat Setup END--------------------------------

void setup() {
  
  Serial.begin(115200);

  // Set the minimum pulse width to 500 microseconds
  // Set the maximum pulse width to 2500 microseconds
  frontServo.attach(FrontServoPin, 500, 2500);
  backServo.attach(BackServoPin, 500, 2500);

  frontMotorESC.attach(MotorThrustPin); //Both motors are connected to this one pin for now.
  //backMotorESC.attach(MotorThrustPin);

  pinMode(LED_BUILTIN, OUTPUT);
}


void loop() {
  if (Serial.available() > 0) {
    // Read the incoming integer
    receivedCommand = Serial.parseInt();

    // Check for the command received
    switch (receivedCommand) {
      case 1: // Motor ON
        // Code to turn motor on
        Serial.println("Motor is ON");
        frontMotorESC.writeMicroseconds(idleThrust); //Turn both motors on to idle thrust
        backMotorESC.writeMicroseconds(idleThrust);
        digitalWrite(LED_BUILTIN, HIGH); //Turn ON on-board LED to represent motor on.
        break;

      case 2: // Motor OFF
        // Code to turn motor off
        Serial.println("Motor is OFF");
        frontMotorESC.writeMicroseconds(noThrust); //Turn both motors off
        backMotorESC.writeMicroseconds(noThrust);
        digitalWrite(LED_BUILTIN, LOW); //Turn OFF on-board LED to represent motor off.
        break;

      case 3: // Steer LEFT
        // Code to steer left
        Serial.println("Steering LEFT");
        frontServo.write(leftFront); //Turn both servos left
        backServo.write(leftBack);
        break;

      case 4: // Steer STRAIGHT
        // Code to steer straight
        Serial.println("Steering STRAIGHT");
        frontServo.write(straightFront); //Turn both servos straight
        backServo.write(straightBack);
        break;

      case 5: // Steer RIGHT
        // Code to steer right
        Serial.println("Steering RIGHT");
        frontServo.write(rightFront); //Turn both servos to the right
        backServo.write(rightBack);
        break;
    }
    // Clear any additional serial data
    while(Serial.available() > 0) Serial.read();
  }
}
