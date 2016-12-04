import time
import RPi.GPIO as GPIO
import threading
from time import sleep
from functools import partial

class Encoder(object):
    global LockRotary, rotary_interrupt, vprev

    Rotary_counter = 0
    Current_A = 1
    Current_B = 1
    PrevTime = 0

    velocity = 0
    prevCount = 0

    pin1 = 0
    pin2 = 0

    LockRotary = threading.Lock()
    rotary_interrupt = 0



    
    def __init__(self, pin1, pin2):

        self.pin1 = pin1
        self.pin2 = pin2

        self.count = 0
        self.velocity = 0
        self.vprev = 0
        
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)               # Use BCM mode

        GPIO.setup(pin1, GPIO.IN)
        GPIO.setup(pin2, GPIO.IN)

        GPIO.add_event_detect(pin1, GPIO.RISING, lambda *a: rotary_interrupt(self, pin1))             # NO bouncetimeEncoderTest
        GPIO.add_event_detect(pin2, GPIO.RISING, lambda *a: rotary_interrupt(self, pin2))

        #GPIO.add_event_detect(pin1, GPIO.RISING, partial(rotary_interrupt, pin1))             # NO bouncetimeEncoderTest
        #GPIO.add_event_detect(pin2, GPIO.RISING, partial(rotary_interrupt, pin2))

        self.Current_A = 1
        self.Current_B = 1

        self.PrevTime = time.time()


    def rotary_interrupt(self,A_or_B):

        Switch_A = GPIO.input(self.pin1)
        Switch_B = GPIO.input(self.pin2)

        if self.Current_A == Switch_A and self.Current_B == Switch_B:      # Same interrupt as before (Bouncing)?
            return                            

        self.Current_A = Switch_A                        # remember new state
        self.Current_B = Switch_B                        # for next bouncing check



        if (Switch_A and Switch_B):                  # Both ones active? Yes -> end of sequence
            LockRotary.acquire()                

            T = time.time()-self.PrevTime
            
            if(T != 0):
                self.velocity = 0.05 * 3.14159 / (400*T)
            else:
                self.velocity = 0

            if A_or_B == self.pin1:                     # Turning direction depends on
                self.count += 1                  # which input gave last interrupt
            else:                              # so depending on direction either
                self.count -= 1                  # increase or decrease counter
                self.velocity = self.velocity * -1

            LockRotary.release()                  # and release lock
            self.PrevTime = time.time()

        return                                 


    def sample(self):
        
        LockRotary.acquire()
        NewCounter = self.count

        if self.prevCount == NewCounter:
            V = 0
        else:
            V = self.velocity
            
        LockRotary.release()
        self.prevCount = NewCounter
        
        return NewCounter,V
