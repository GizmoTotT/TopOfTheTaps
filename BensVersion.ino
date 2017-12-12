//Code that moves LEDS down strips in time with the music actuated by digital inputs from the pi as digital is faster than serial
#include <FastLED.h> //Arduino library for manipulating the strips
  // Assigning pins logically to strips
  #define LED_PIN0 9 
  #define LED_PIN1 10
  #define LED_PIN2 11
  #define LED_PIN3 12
  //Assignign key variables for use with arduino library
  #define NUM_LEDS 12
  #define NUM_STRIPS 4

  CRGB leds[NUM_STRIPS][NUM_LEDS]; //Arduino library variable creating an array structure of strips and leds to understand which leds on which strip is being used

  int _maxLength = NUM_LEDS; //variable defined to understand the end of strip value
  int _maxLeds = 6; //chosen value to limit the number of LEDS on strip at a time

  // An array that is used to determine where on the strip the LEDS are, the values represent how far down, with 230 being the null value due to unusual occurrence with the specific strip at lower values
  // the four represents which strip and each of the 6 values is one of the LEDs that can fit onto the strip ie (creating an empty queue which can be filled with potential LEDs to move down the strip.
  int listOfLedPositions[4][6] ={{230,230,230,230,230,230},{230,230,230,230,230,230},{230,230,230,230,230,230},{230,230,230,230,230,230}};
  //Defining times for calculating how long the arduino should be scanning
  int startTime;
  int elapsedTime;

  //defining Values for input pins from the pin 
  int stripZeroDigital = 2;
  int stripOneDigital = 3;
  int stripTwoDigital = 4;
  int stripThreeDigital = 5;

  bool work;


void setup() {
  Serial.begin(9600); //code for starting the debugger
  //code for assiging arduino libraries correctly using the arrays CRGB arrays  number of leds to the specific pins
  FastLED.addLeds<NEOPIXEL, LED_PIN0>(leds[0], NUM_LEDS);
  FastLED.addLeds<NEOPIXEL, LED_PIN1>(leds[1], NUM_LEDS);
  FastLED.addLeds<NEOPIXEL, LED_PIN2>(leds[2], NUM_LEDS);
  FastLED.addLeds<NEOPIXEL, LED_PIN3>(leds[3], NUM_LEDS);
  //Assigning pinValues to pins as inputs to use digitalRead() function
  pinMode(stripZeroDigital, INPUT);
  pinMode(stripOneDigital, INPUT);
  pinMode(stripTwoDigital, INPUT);
  pinMode(stripThreeDigital, INPUT);
}
//Function that changes a value in the array to a 0 so that it becomes recognised as an LED that should move
//down the strip using moveAllLeds() function. Takes value of strip as an input aswell as array and return null
void createLed(int listOfLedPositions[4][6],int stripValue, bool work) {
  for (int i=0; i < _maxLeds; i++) { //This loop iterates between number of Leds that can fit on strip which is equal to number of values in array that need checking to see if value can be placed
    if (listOfLedPositions[stripValue][i] == 230){ //check each element of queue to see if an LED dot is assigned
      listOfLedPositions[stripValue][i] = 0; //if not assigned sets its value to 0 which is how the library refers to first value of strip where x = 0 in leds[j][x]
      work = true;
      break; //break out of loop 
    }
      //if strip queue is "full"(all values are null/230) it does nothing
  }
}
// function that move all Leds in all strips down one place
void moveAllLeds(int listOfLedPositions[4][6])
{
  for (int j=0; j < 4; j++){ // loop to iterate between all four strips
    for (int i=0; i < _maxLeds; i++){ //loop to check all LEDS already placed in LED strip
      if (listOfLedPositions[j][i] != 230){ //checks if the queue position has an LED
        if (listOfLedPositions[j][i]+1 < _maxLength)  { // checks if adding one is a valid position on strip
          listOfLedPositions[j][i] = listOfLedPositions[j][i]+1; // adds one if it can
          }
        else {
          leds[j][listOfLedPositions[j][i]] = CRGB(0,0,0); //turns it white 
          listOfLedPositions[j][i] = 230; //sets it back to a null value so new led can be created
        }
      }
    }
  }
  FastLED.show(); //show clear LEDs that were removed
}
//function to set colour that takes colour and strip number as input
void setColour(int _redValue, int _greenValue, int _blueValue, int listOfLedPositions[4][6],int stripNumber){
    for (int i=0; i < _maxLeds; i++){ //loop between each value in in queue
      leds[stripNumber][listOfLedPositions[stripNumber][i]] = CRGB(_redValue, _greenValue, _blueValue); //for that value in queue for that strip set the colour
    }
}
//function to clear all LEDS that are illuminated
void clearLeds(int listOfLedPositions[4][6]){ //iterates through all values in listOfLedPositions and sets to black
  for (int j=0; j < 4; j++){ 
    for (int i=0; i < _maxLeds; i++){
      leds[j][listOfLedPositions[j][i]] = CRGB(0,0,0);
    }
  }
  FastLED.show(); //show black LEDS
}
void loop() {
    //Serial.println("broke incorrect");
    //booleans used to make sure only oneLED is created by creating  a variable that can be assigned true if one created then set as false before coming back to this point in loop
    bool zeroBool = false;
    bool oneBool = false;
    bool twoBool = false;
    bool threeBool = false;
    //setting starting Times for this loop and elapsed times back to 0
    startTime = millis();
    elapsedTime = millis() - startTime;
    while (elapsedTime < 200){ // repeat this section until elapsed time exceeds set value, keeps checking for digital inputs over and over again and if an led should be created, create one and only one
      //Serial.print(elapsedTime);
      elapsedTime = millis()- startTime; //readjust elapsed time using startTime as constant
      //check for high or low inputs from digital read
      int stripStateZero = digitalRead(stripZeroDigital);
      int stripStateOne = digitalRead(stripOneDigital);
      int stripStateTwo = digitalRead(stripTwoDigital);
      int stripStateThree = digitalRead(stripThreeDigital);
      //each if function below checks if high and if strip already had a led created in set interval of while loop
      if(stripStateZero == HIGH and zeroBool == false){
        Serial.print(stripStateZero);
        createLed(listOfLedPositions,0,work); // it now creates an LED using function above
        if(work == true){
        Serial.println("correct");
        delay(100);
        work = false; 
        }
        zeroBool = true; //assigns bool to true for this loop so it doesnt create another LED
      }
      if(stripStateOne == HIGH and oneBool == false){
        Serial.print(stripStateOne);
        createLed(listOfLedPositions,1,work);
        if(work == true){
        Serial.println("correct");
        delay(100);
        work = false;
        }        
        oneBool = true;
      }
      if(stripStateTwo == HIGH and twoBool == false){
        Serial.print(stripStateTwo);
        createLed(listOfLedPositions,2,work);
        if(work == true){
          delay(100);
        Serial.println("correct");
        work = false;
        }
        twoBool = true;
      }
      if(stripStateThree == HIGH and threeBool == false){
        Serial.print(stripStateThree);
        createLed(listOfLedPositions,3,work);
        if(work == true){
        Serial.println("correct");
        delay(100);
        work = false;
        }
        threeBool = true;
      }
    }
    //end of while Loop
    clearLeds(listOfLedPositions); //turn LEDS off
    moveAllLeds(listOfLedPositions);
    if (listOfLedPositions[0][0] != 230|| listOfLedPositions[0][1] != 230|| listOfLedPositions[0][2] != 230 || listOfLedPositions[0][3] != 230|| listOfLedPositions[0][4] != 230|| listOfLedPositions[0][5] != 230 ||
        listOfLedPositions[1][0] != 230|| listOfLedPositions[1][1] != 230|| listOfLedPositions[1][2] != 230 || listOfLedPositions[1][3] != 230|| listOfLedPositions[1][4] != 230|| listOfLedPositions[1][5] != 230 ||
        listOfLedPositions[2][0] != 230|| listOfLedPositions[2][1] != 230|| listOfLedPositions[2][2] != 230 || listOfLedPositions[2][3] != 230|| listOfLedPositions[2][4] != 230|| listOfLedPositions[2][5] != 230 ||
        listOfLedPositions[3][0] != 230|| listOfLedPositions[3][1] != 230|| listOfLedPositions[3][2] != 230 || listOfLedPositions[3][3] != 230|| listOfLedPositions[3][4] != 230|| listOfLedPositions[3][5] != 230) {
          setColour(128,0,128,listOfLedPositions,0);
          setColour(0,255,0,listOfLedPositions,1);
          setColour(255,0,0,listOfLedPositions,2);
          setColour(0,0,255,listOfLedPositions,3);
          FastLED.show();
          
      }
}

