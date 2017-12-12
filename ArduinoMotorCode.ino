#include <Servo.h> //include is used to access libraries outside of the sketch
#include <Stepper.h>
Servo myservo; //assigns 'myservo' and 'myservo2' as servos
Servo myservo2;

//saves all variables as integer values
int stepsPerRevolution = 10; //the steps the stepper motor will take. Is low as this will take a shorter length of time to run. 
int serValue; 
int led = 3; //assigning pin values
int led2 = 2; //assigning pin values
int pos = 0; //assigning pin values
int servoPin = 4; //assigning pin values
int servoPin2 = 5; //assigning pin values

Stepper myStepper(stepsPerRevolution, 6, 7, 8, 9); // assignes 'myStepper' as a Stepper motor to the pins 6, 7, 8 and 9
Stepper myStepper2(stepsPerRevolution, 10, 11, 12, 13); // assignes 'myStepper2' as a Stepper motor to the pins 10, 11, 12 and 13

void setup() { //this code runs once on turning on to set up the arduino.
  Serial.begin(9600); //Sets data rate in bits per second for serial data transmission. 9600 was chosen as ??
  pinMode(led,OUTPUT); //Configures the pin led (3) and led2 (2) pin to behave as outputs.
  pinMode(led2, OUTPUT); 
  myservo.attach(servoPin); //Attach the Servo 'myservo' and 'myservo2' variables to pins servoPin (4) and servoPin2 (5)
  myservo2.attach(servoPin2);
  myStepper.setSpeed(2000); //Sets the motor speed for 'myStepper' and 'myStepper2' in rotations per minute. When step() is called, the speed is set at 2000 RPM.
  myStepper2.setSpeed(2000);
}

void loop() { // the main code is placed into the void loop, to run repeatedly. 
  bool discoLight = false; //booleans holds either true or false. All these variables are initially set as boolean false. 
  bool discoMotor = false;
  bool steppoOne = false;
  bool steppoTwo = false;
  bool reset = false;
  digitalWrite(led, LOW); //This gives LOW 0V value to the two LED pins.
  digitalWrite(led2, LOW);
  //Serial.println("voidLoopEntered");

  while (reset == false) { //the while loop will run as long as 'reset' is set as false.
    if( Serial.available()) { //If data is coming through the serial port
      //Serial.println("Reading serial");
      serValue = Serial.read(); //this reads incoming serial data, which will be what is sent from the pi (0, 1, 2, 3 or 4)

      //Serial.print(serValue); 

      switch(serValue) //Compares the value of serValue to the values specified each case statements.
      {
        case '0': //When case equals 0 (serValue = 0), discoLight boolian becomes true.
        discoLight = true;
        //Serial.println("serial = 0");
        break; //exits the switch statement so the rest of the code can be run.
        case '1':
        discoMotor = true;
        //Serial.println("serial = 1");
        break;
        case '2':
        steppoOne = true;
        //Serial.println("serial = 2");
        break;
        case '3':
        steppoTwo = true;
        //Serial.println("serial = 3");
        break;
        case '4':
        reset = true;
        break;
        //Serial.println("serial = 4");
        default:
        break;
      }
    
    }
    if (discoLight == true and discoMotor == false and steppoOne == false and steppoTwo == false) {
      //when discoLight is the only true boolian, the LED's turn on
      //Serial.println("Disco light was true");

      digitalWrite(led, HIGH);
      digitalWrite(led2, HIGH);
      //Serial.print(serValue);
    }
      
    if (discoLight == true and discoMotor == true and steppoOne == false and steppoTwo == false) {
      //Serial.println("Disco light was true");
      //when discoLight and discoMotor are the only true boolians, the code turns on the LED's and rotates the discoballs through the two servo motors.
      digitalWrite(led, HIGH);
      digitalWrite(led2, HIGH);
      //Serial.print(serValue);
        //Serial.println("discoMotor was true");
        for (pos = 0; pos <= 180; pos += 6  ) { //from position 0 degrees to anything under or equal to 180 (??), on each repetition of the for loop, the position is increased by 6 degrees
          myservo.write(pos); //writes a value to the servo to the angle of the shaft between 0 and 180 degrees.
          myservo2.write(pos);
          delay(20); //20ms delay. made the delay double to try to slow the servo so this if statement and the one below are the same speeds
        }
        for (pos = 180; pos >= 0; pos -= 6) { //goes from 180 degrees to 0 degrees in steps of -6 degrees
          myservo.write(pos);
          myservo2.write(pos);
          delay(20);
        }
    }

    if (discoLight == true and discoMotor == true and steppoOne == true and steppoTwo == false) {
      //Serial.println("Disco light was true");
    //when variables discoLight, discoMotor and steppoOne are all true, the lights come on, the discoball rotates on servos and the stepper motor rotates the first cam
      digitalWrite(led, HIGH);
      digitalWrite(led2, HIGH);
      //Serial.print(serValue);
        //Serial.println("discoMotor was true");
        for (pos = 0; pos <= 180; pos += 6) {
          myservo.write(pos);
          myservo2.write(pos);
          delay(10); //halved the delay as due to the line myStepper.step(), the for loop runs slower than the for loop in the previous if statement.
          //to speed this servo up to approximately what it was previously, the delay between repeats has been halved.
          //Serial.println("SeppoONe was true");
          myStepper.step(stepsPerRevolution); //this turns the stepper motor a specific number of steps at a speed of 2000 RPM as defined above. 
          //This function is blocking, meaning it will wait till the motor has stopped moving before moving to the next line of code, causing the servo speed to slow. 
        }
        for (pos = 180; pos >= 0; pos -= 6) {
          myservo.write(pos);
          myservo2.write(pos);
          delay(10);
          //Serial.println("SeppoONe was true");
          myStepper.step(stepsPerRevolution);
        }
     }

    if (discoLight == true and discoMotor == true and steppoOne == true and steppoTwo == true) {
      //Serial.println("Disco light was true");
      //when all four variables are true, the LED's are on, the discoballs are rotating on servos, and both stepper motors are each turning a cam. 
      digitalWrite(led, HIGH);
      digitalWrite(led2, HIGH);
      //Serial.print(serValue);
        //Serial.println("discoMotor was true");
        for (pos = 0; pos <= 180; pos += 6) {
          myservo.write(pos);
          myservo2.write(pos);
          delay(2.5); //reduced the delay again, as this for statement has two stepper motors running. 
       //Serial.println("SeppoONe was true");
          myStepper.step(stepsPerRevolution);
     
     //Serial.println("SeppoTwo was true");
     myStepper2.step(stepsPerRevolution);
        }
        for (pos = 180; pos >= 0; pos -= 6) {
          myservo.write(pos);
          myservo2.write(pos);
          delay(2.5);
     //Serial.println("SeppoONe was true");
          myStepper.step(stepsPerRevolution);
     
     //Serial.println("SeppoTwo was true");
         myStepper2.step(stepsPerRevolution);
        }
}
}
}
