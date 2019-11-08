'''
v2

Master of embedded cyber-physical systems
ECPS 295  |  Sensors actuators and networks
Billy Chen & Judit Giro Benet
6th november 2019

===================================================================
===============  WELCOME TO THE ReahHub PROJECT !  ================
===================================================================

Sent messages from RPi to ESP32:
---------------------------------------
    TO TURN LEDss ON/OFF:
    - "#10" --> means R LED is on & L LED is off

    TO COMUNICATED HOW MUCH TIME:
    - "***" can be:
        - "*00" --> No personal record
        - "*10" --> Right personal record
        - "*01" --> Left personal record
        - "*11" --> Right & Left personal record


Received messages from ESP32 to RPi:
---------------------------------------
    - "#......." --> if starts with "#" user touched some LED already
    - "#L......" --> if starts with "#L" user touched left LED already
    - "#R......" --> if starts with "#R" user touched right LED already
   
'''

import socket
import RPi.GPIO as GPIO
import time
import random
GPIO.setwarnings(False)

# ========================= VARIABLES =========================
LED=21 #20,16,12, 26
GPIO.setmode(GPIO.BCM) #BOARD)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,GPIO.LOW)  

TRs=[0]  #last time values for right LED
TLs=[0]  #last time values for left LED


# ========================= CONNECTIONS =========================
#RPi_IP = "192.168.2.2"  # --> RPi IP at home
#ESP_IP="192.168.0.103"  # --> ESP IP at home
RPi_IP="169.234.56.73" # --> RPi IP at uni
ESP_IP="169.234.1.228" # --> ESP IP at uni
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((RPi_IP, UDP_PORT))
sock.settimeout(10000.0)

i=1

file = open('dataLog.txt','w') 

# ========================= THE LOOP =========================
while True:

    # 1. Generate 2 rnd values for left (L) and right (R) LEDs. Send them to ESP
    statusR=random.randint(0,1)
    statusL=random.randint(0,1)
    #message="#",str(statusR),str(statusL)
    message="#"+str(statusR)+"1" #str(statusL)
    sock.sendto(message,(ESP_IP,UDP_PORT))
    print "\n============================================================"
    print "PLAYING @ ROUND ",i, "--> Message sent: ",message,"\n"
    i+=1
    #T0=time.time()
    #print "T0=",T0

    while True: #(time.time()-T0<10):
        data, addr = sock.recvfrom(1024)
        message="*0" #Will be sent later

        # IF RIGHT LED TOUCHED
        if(data[0]=="R"):
            TR=10*int(data[1])+int(data[2])
            print "Message received: ",data,"  <-- from: ",addr
            print ">> RIGHT LED WAS REACHED! \n User needed ",TR," sec to touch RIGHT LED"
            file.write("R,"+str(TR))
            TRs.append(TR)

            #IF personal record:
            message="*R0"
            if(TR==max(TRs)):
                print "*** New right personal record! *** \n"
                message="*R1"

        # IF LEFT LED TOUCHED
        if(data[0]=="L"):
            TL=10*int(data[1])+int(data[2])
            print "Message received: ",data,"  <-- from: ",addr
            print ">> LEFT LED WAS REACHED! \n User needed ",TL," sec to touch LEFT LED\n"
            file.write("L,"+str(TL))
            TLs.append(TL)

            #IF personal record:
            message="*L0"
            if(TL==max(TLs)):
                print "*** New left personal record! ***"
                message="*L1"

        sock.sendto(message,(ESP_IP,UDP_PORT))
        break;

    time.sleep(10)


GPIO.cleanup() 
file.close()