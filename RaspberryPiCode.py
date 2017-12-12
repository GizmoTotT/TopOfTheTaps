''' Python code running on the RaspberryPi which combines all of the gizmo
elements and ensures synchronisation between them. The Pi board is connected to
four buttons (each of which is made of an LED and a switch) through GPIO pins,
to one Arduino board through four GPIO pins and to a second Arduino board through
the serial port. The code also uses the audio jack output.

The first step is the preparation of the Pi board, defining all input and outputs
pins and importing required libraries.'''

#importing the libraries needed to control the RaspberryPi inputs and outputs:
import serial
from gpiozero import LED, Button
import RPi.GPIO as GPIO

import time #importing time for synchronisation
import pygame #importing pygame library which allows to implement and work with music files
from multiprocessing import Process, Value #the multiprocessing library allows to control seperate processes and interactions between them

GPIO.setmode(GPIO.BCM) #setting GPIO to BCM values rather than physical pin values
GPIO.setwarnings(False) #turning off warnings about the pins that come up when running the code

#setting pins 13, 5, 25 and 4 as outputs, these will communicate with the Arduino board triggering the LED strips
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

#defining pins 6, 22, 27 and 17, that correspond to the LEDs in each of the four buttons
ledbutton0 = LED(6)
ledbutton1 = LED(22)
ledbutton2 = LED(27)
ledbutton3 = LED(17)

#setting pins 12, 24, 23, 18 as inputs for the switches (all pins have been chosen in a way that makes the setup process easier,
#so most left pins connect to most left button etc.)
pressbutton0 = Button(12)
pressbutton1 = Button(24)
pressbutton2 = Button(23)
pressbutton3 = Button(18)

''' The next step is creating time stamp libraries in the form of 5 seperate dictionaries. These
time stamps correspond to specific points in the music that were chosen as characteristic points
for the users to interact with.'''

#Defining the times at which the first button lights up and is to be pressed by the player:
times0 = {
1 : (4.00),
2 : (7.397),
3 : (14.534),
4 : (15.629),
5 : (22.26),
6 : (26.713),
7 : (32.424),
8 : (33.873),
9 : (36.308),
10 : (38.236),
11 : (39.68),
12 : (41.614),
13 : (43.554),
14 : (45.493),
15 : (47.448),
16 : (49.367),
17 : (51.747),
18 : (58.078),
19 : (67.263),
20 : (70.167),
21 : (71.618),
22 : (73.069),
23 : (75.014),
24 : (76.945),
25 : (78.398),
26 : (81.303),
27 : (82.751),
28 : (84.2),
29 : (88.17),
30 : (93.592),
31 : (95.517),
32 : (97.941),
33 : (99.38),
34 : (101.805),
35 : (103.739),
36 : (104.698),
37 : (106.157),
38 : (108.085),
39 : (111.881),
40 : (114.279),
41 : (116.456),
42 : (120.161)
}

#Defining the times at which the second button lights up and is to be pressed by the player:
times1 = {
1 : (4.354),
2 : (7.628),
3 : (11.758),
4 : (15.143),
5 : (19.843),
6 : (22.604),
7 : (26.483),
8 : (31.941),
9 : (32.904),
10 : (34.355),
11 : (35.525),
12 : (37.744),
13 : (39.199),
14 : (40.657),
15 : (42.117),
16 : (45.003),
17 : (48.41),
18 : (50.346),
19 : (53.187),
20 : (62.801),
21 : (68.232),
22 : (70.646),
23 : (72.585),
24 : (74.038),
25 : (75.969),
26 : (77.91),
27 : (79.844),
28 : (81.789),
29 : (83.722),
30 : (86.792),
31 : (92.547),
32 : (94.554),
33 : (96.986),
34 : (98.898),
35 : (100.833),
36 : (102.771),
37 : (105.665),
38 : (107.595),
39 : (110.425),
40 : (113.812),
41 : (116.113),
42 : (118.216)
}

#Defining the times at which the third button lights up and is to be pressed by the player:
times2 = {
1 : (7.137),
2 : (14.885),
3 : (19.37),
4 : (23.096),
5 : (31.451),
6 : (33.393),
7 : (35.81),
8 : (37.529),
9 : (40.17),
10 : (42.591),
11 : (43.053),
12 : (45.975),
13 : (49.854),
14 : (59.463),
15 : (66.775),
16 : (68.717),
17 : (72.097),
18 : (74.517),
19 : (76.452),
20 : (78.877),
21 : (80.323),
22 : (82.27),
23 : (84.691),
24 : (90.628),
25 : (93),
26 : (95.049),
27 : (96.007),
28 : (98.415),
29 : (100.35),
30 : (102.28),
31 : (105.184),
32 : (107.12),
33 : (108.587),
34 : (112.246),
35 : (115.592),
36 : (117.191)
}

#Defining the times at which the fourth button lights up and is to be pressed by the player:
times3 = {
1 : (6.781),
2 : (7.878),
3 : (12.11),
4 : (15.35),
5 : (22.876),
6 : (26.199),
7 : (30.968),
8 : (34.839),
9 : (36.778),
10 : (38.713),
11 : (41.146),
12 : (43.078),
13 : (44.516),
14 : (46.938),
15 : (47.913),
16 : (48.89),
17 : (51.336),
18 : (55.985),
19 : (65.821),
20 : (67.749),
21 : (69.205),
22 : (71.133),
23 : (73.552),
24 : (75.487),
25 : (77.424),
26 : (79.355),
27 : (80.824),
28 : (83.226),
29 : (85.185),
30 : (92.039),
31 : (94.084),
32 : (96.493),
33 : (97.458),
34 : (99.884),
35 : (101.325),
36 : (103.248),
37 : (104.215),
38 : (106.638),
39 : (109.929),
40 : (115.138),
41 : (116.274),
42 : (117.675),
43 : (122.11),
44 : (124.047)
}

#Defining the times at which the Pi boards sends information to the Arduino. At those
#times, the Arduino triggers one of the four LED strips. These times are 2.4 seconds
#before the actual buttons light up, as that is the time taken by a single light to travel
#down an LED strip. The first entry of the dictionary corresponds to the time that the
#infromation is to be sent, and the second one to the LED strip that it is sent to.
timea = {
1 : (1.6, 0),
2 : (1.954, 1),
3 : (4.381, 3),
4 : (4.737, 2),
5 : (4.997, 0),
6 : (5.228, 1),
7 : (5.478, 3),
8 : (9.358, 1),
9 : (9.71, 3),
10 : (12.134, 0),
11 : (12.485, 2),
12 : (12.743, 1),
13 : (12.95, 3),
14 : (13.229, 0),
15 : (16.97, 2),
16 : (17.443, 1),
17 : (19.86, 0),
18 : (20.204, 1),
19 : (20.476, 3),
20 : (20.696, 2),
21 : (23.799, 3),
22 : (24.083, 1),
23 : (24.313, 0),
24 : (28.568, 3),
25 : (29.051, 2),
26 : (29.541, 1),
27 : (30.024, 0),
28 : (30.504, 1),
29 : (30.993, 2),
30 : (31.473, 0),
31 : (31.955, 1),
32 : (32.439, 3),
33 : (33.125, 1),
34 : (33.41, 2),
35 : (33.908, 0),
36 : (34.378, 3),
37 : (35.129, 2),
38 : (35.344, 1),
39 : (35.836, 0),
40 : (36.313, 3),
41 : (36.799, 1),
42 : (37.28, 0),
43 : (37.77, 2),
44 : (38.257, 1),
45 : (38.746, 3),
46 : (39.214, 0),
47 : (39.717, 1),
48 : (40.191, 2),
49 : (40.653, 2),
50 : (40.678, 3),
51 : (41.154, 0),
52 : (42.116, 3),
53 : (42.603, 1),
54 : (43.093, 0),
55 : (43.575, 2),
56 : (44.538, 3),
57 : (45.048, 0),
58 : (45.513, 3),
59 : (46.01, 1),
60 : (46.49, 3),
61 : (46.967, 0),
62 : (47.454, 2),
63 : (47.946, 1),
64 : (48.936, 3),
65 : (49.347, 0),
66 : (50.787, 1),
67 : (53.585, 3),
68 : (55.678, 0),
69 : (57.063, 2),
70 : (60.401, 1),
71 : (63.421, 3),
72 : (64.375, 2),
73 : (64.863, 0),
74 : (65.349, 3),
75 : (65.832, 1),
76 : (66.317, 2),
77 : (66.805, 3),
78 : (67.767, 0),
79 : (68.246, 1),
80 : (68.733, 3),
81 : (69.218, 0),
82 : (69.697, 2),
83 : (70.185, 1),
84 : (70.669, 0),
85 : (71.152, 3),
86 : (71.638, 1),
87 : (72.117, 2),
88 : (72.614, 0),
89 : (73.087, 3),
90 : (73.569, 1),
91 : (74.052, 2),
92 : (74.545, 0),
93 : (75.024, 3),
94 : (75.51, 1),
95 : (75.998, 0),
96 : (76.477, 2),
97 : (76.955, 3),
98 : (77.444, 1),
99 : (77.923, 2),
100 : (78.424, 3),
101 : (78.903, 0),
102 : (79.389, 1),
103 : (79.87, 2),
104 : (80.351, 0),
105 : (80.826, 3),
106	: (81.322, 1),
107	: (81.8, 0),
108	: (82.291, 2),
109	: (82.785, 3),
110	: (84.392, 1),
111	: (85.77, 0),
112	: (88.228, 2),
113	: (89.639, 3),
114	: (90.147, 1),
115	: (90.6, 2),
116	: (91.192, 0),
117	: (91.684, 3),
118	: (92.154, 1),
119	: (92.649, 2),
120	: (93.117, 0),
121	: (93.607, 2),
122	: (94.093, 3),
123	: (94.586, 1),
124	: (95.058, 3),
125	: (95.541, 0),
126	: (96.015, 2),
127	: (96.498, 1),
128	: (96.98, 0),
129	: (97.484, 3),
130	: (97.95, 2),
131	: (98.433, 1),
132	: (98.925, 3),
133	: (99.405, 0),
134	: (99.88, 2),
135	: (100.371, 1),
136	: (100.848, 3),
137	: (101.339, 0),
138	: (101.815, 3),
139	: (102.298, 0),
140	: (102.784, 2),
141	: (103.265, 1),
142	: (103.757, 0),
143	: (104.238, 3),
144	: (104.72, 2),
145	: (105.195, 1),
146	: (105.685, 0),
147	: (106.187, 2),
148	: (107.529, 3),
149	: (108.025, 1),
150	: (109.481, 0),
151	: (109.846, 2),
152	: (111.412, 1),
153	: (111.879, 0),
154	: (112.738, 3),
155	: (113.192, 2),
156	: (113.713, 1),
157	: (113.874, 3),
158	: (114.056, 0),
159	: (114.791,	2),
160	: (115.275, 3),
161	: (115.816, 1),
162	: (117.761, 0),
163	: (119.71, 3),
164	: (121.647, 3)
}

'''The third step is defining all the functions that will later be called by the code.'''

#Function stripPin allows the control of the pins that connect to the Arduino board
#and which correspond to a specific LED strip.
#the variable n defines which LED strip we want to communicate with
#while the variable m sets the pin communicating with that LED strip to high or low
#as an example: stripPin(2,1) will set the pin 25 to high, and that will be communicated to LED strip 2.
def stripPin(n, m):
    if n == 0:
		if m == 0:
			return GPIO.output(13, 0) #pin 13 corresponds to LED strip 0
		if m == 1:
			return GPIO.output(13, 1)
    if n == 1:
        if m == 0:
            return GPIO.output(5, 0) #pin 5 corresponds to LED strip 1
        if m == 1:
            return GPIO.output(5, 1)
    if n == 2:
        if m == 0:
            return GPIO.output(25, 0) #pin 25 corresponds to LED strip 2
        if m == 1:
            return GPIO.output(25, 1)
    if n == 3:
        if m == 0:
            return GPIO.output(4, 0) #pin 4 corresponds to LED strip 3
        if m == 1:
            return GPIO.output(4, 1)

#The following four functions control the four buttons, both the LEDs and the switches,
#the button lights up in time with the music and thats when it waits for the button press
#to see if the player hits it in time, if so, the player will be awarded a point for
#every correct hit.
def button0(s): #function for the first button

    while pygame.mixer.music.get_busy(): #means while the music is playing, a command from the pygame library

        for i in range(1,42): #for i in range of the corresponding time dictionary, iterating through the entire dictionary

            check0 = True #setting a variable to True, that will be used later in the function

            ledbutton0.off() #by default turning the corresponding LED off

            interval = 0.5 #setting the interval around the actual time during which we want the LED to light up, so if the interval is 0.5 the LED will be on for half a second
            late = 0.75 #variable late set to 0.85 as that is the time it takes the arduino to start playing the music after it starts counting time, this ensures proper synchronisation

            addtime = interval/2 + late #the time added (or substracted) to the time moment in order to create the wanted interval
            minustime = interval/2 - late

            while time.time() - tm < times0[i] + addtime and time.time() - tm > times0[i] - minustime: #while current time minus tm (the time at the start of the program) is between the higher and lower boundaries of the interval

                ledbutton0.on() #turn on the LED to indicate the moment the button is supposed to be pressed

                if pressbutton0.is_pressed and check0 == True: #if the button is pressed in that time interval

                    with s.get_lock(): #lock the shared variable s (allows to change its values), this has to be done as the same variable is accessed from different processes, otherwise the value would be seperate for each process
                        s.value += 1 #add 1 to the current value of s (s is the current score of the player)

                    print("button 0 pressed") #printing feedback that allows the control of the players situation in the game
                    print("current score is:") #these printing functions are not needed in the actual interaction with the pixel as they don't affect it in any way
                    print(s.value) #they're only visible by the person controlling the code

                    check0 = False #change the variable to False, thanks to this only one point will be awarded for every appropriate press


def button1(s): #repeating the same function for button 2

    while pygame.mixer.music.get_busy():

        for i in range(1,42):

            check1 = True

            ledbutton1.off()

            interval = 0.5
            late = 0.75

            addtime = interval/2 + late
            minustime = interval/2 - late

            while time.time() - tm < times1[i] + addtime and time.time() - tm > times1[i] - minustime:

                ledbutton1.on()

                if pressbutton1.is_pressed and check1 == True:

                    with s.get_lock():
                        s.value += 1

                    print("button 1 pressed")
                    print("current score is:")
                    print(s.value)

                    check1 = False


def button2(s): #repeating the same function for button 3

    while pygame.mixer.music.get_busy():

        for i in range(1,36):

            check2 = True

            ledbutton2.off()

            interval = 0.5
            late = 0.75

            addtime = interval/2 + late
            minustime = interval/2 - late

            while time.time() - tm < times2[i] + addtime and time.time() - tm > times2[i] - minustime:

                ledbutton2.on()

                if pressbutton2.is_pressed and check2 == True:

                    with s.get_lock():
                        s.value += 1

                    print("button 2 pressed")
                    print("current score is:")
                    print(s.value)

                    check2 = False


def button3(s): #repeating the same function for button 4

    while pygame.mixer.music.get_busy():

        for i in range(1,44):

            check3 = True

            ledbutton3.off()

            interval = 0.5
            late = 0.75

            addtime = interval/2 + late
            minustime = interval/2 - late

            while time.time() - tm < times3[i] + addtime and time.time() - tm > times3[i] - minustime:

                ledbutton3.on()

                if pressbutton3.is_pressed and check3 == True:

                    with s.get_lock():
                        s.value += 1

                    print("button 3 pressed")
                    print("current score is:")
                    print(s.value)
                    check3 = False


#function controlling the signals sent to the Arduino that controls the LED strips:
def arduino(interval = 0.07, late = 0.75): #setting interval and late as variables, they work in the same way as in the button functions, the interval is set to 0.35 as this is enough time for the Arduino to read the digital input from the Pi

    while pygame.mixer.music.get_busy(): #while music is playing

        for i in range(1,164): #iterating through all entries in the Arduino time dictionary

            addtime = interval/2 + late #same as in the button functions
            minustime = interval/2 - late
            checkard = True #setting a variable to True, this will be used later
            na = timea[i][1] #na defines the strip number corresponding to the specific time point as defined in the Arduino time dictionary

            while time.time()-tm < timea[i][0]+ addtime and time.time()-tm > timea[i][0] - minustime and checkard == True: #while in the time interval
                stripPin(na, 1) #setting the appropriate pin to high (the function stripPin is explained above - line 399)
                stripPin(na, 0) #immediately setting the pin back to low, the signal is long enough for it to be read as one by the Arduino and not too long, which would cause it to be read as multiple signals
                checkard = False #setting the variable to False which ensures that only one signal is sent to the Arduino per time interval

pygame.init() #initialise the pygame controls
pygame.mixer.init() #initialise the pygame.mixer which allows to control music
pygame.mixer.music.load('pump.ogg') #load the music file so that it's ready to be used in the program code

''' Last step is putting everything together and specifying all needed elements in the __main__ file, this is the actual program running on the Pi board'''

if __name__ == '__main__':

    ser = serial.Serial('/dev/ttyACM0',9600) #defining ser as the communication with the second Arduino that is connected to the ACM0 serial port
    #ser = serial.Serial('/dev/ttyACM1', 9600)

    while True: #while True loop allows for the infinite use of the gizmo

        if pressbutton0.is_pressed or pressbutton1.is_pressed or pressbutton2.is_pressed or pressbutton3.is_pressed: #pressing any of the four buttons triggers the main code

            score = Value('i', 0) #defining score as a value accessible from all processes, 'i' sets the value type as integer, and 0 sets the starting value to zero; this variable will store the

            #ensuring that all digital pins are set to zero as default, so no unwanted signals are sent to the first Arduino board:
            GPIO.output(4, 0)
            GPIO.output(25, 0)
            GPIO.output(5, 0)
            GPIO.output(13, 0)

            #all boolean variables that will be used in this part of the code are set to True, this will be used later on
            checka = True
            checkb = True
            checkc = True
            checkd = True

            ser.write(str(4)) #writing 4 to the second Arduino, on it, this value means stopping all the mechanisms, this ensures that everything is zeroed before running the program

            #calling the 5 operating functions as processes, this means that all of them can run simultaneously, the four button functions use the variable score as their argument
            button0p = Process(target=button0, args=(score,))
            button1p = Process(target=button1, args=(score,))
            button2p = Process(target=button2, args=(score,))
            button3p = Process(target=button3, args=(score,))
            arduinop = Process(target=arduino)

            #starting the main timer that will be the guideline for all synchronisation of processes
            tm = time.time()

            print(tm) #printing the current time just for a reference information
            pygame.mixer.music.play() #start playing the loaded audio file

            #start all the processes:
            button0p.start()
            button1p.start()
            button2p.start()
            button3p.start()
            arduinop.start()

            while pygame.mixer.music.get_busy(): #while the music is playing

                if score.value > 5 and checka == True: #if the total score of the player is higher than 5, the first "reward" is started
                    print("win1")
                    ser.write(str(0)) #serial code sent to the second Arduino - disco ball LEDs light up
                    checka = False #boolean expression ensures that only one signal is sent to the Arduino at a time
                if score.value > 15 and checkb == True: #if the total score of the player is higher than 15, the second "reward" is started
                    print("win2")
                    ser.write(str(1)) #serial code sent to the second Arduino - disco balls start rotating
                    checkb = False
                if score.value > 30 and checkc == True: #if the total score of the player is higher than 30, the third "reward" is started
                    print("win3")
                    ser.write(str(2)) #serial code sent to the second Arduino - first stepper motor controlling the movement of the dancing man starts rotating
                    checkc = False
                if score.value > 50 and checkd == True: #if the total score of the player is higher than 50, the fourth "reward" is started
                    print("win4")
                    ser.write(str(3)) #serial code sent to the second Arduino - second stepper motor controlling the movement of the dancing man starts rotating, all mechanical components are working
                    checkd = False

            if pygame.mixer.music.get_busy() == False: #if the music stops playing
                ser.write(str(4)) #send a serial 4 - all mechanical components will be stopped, the code will be waiting for a button press that will start it again
