class Motor(object):
    global Frequency, DC
    Frequency = 50
    MinF = 0
    MinR = 0
    pin = 0
    pi = 0
    SpeedRange = 0
    speed = 0 # range: [-100,100]
    

    def __init__(self, MinF, MinR, SpeedRange, pin, pi):

        self.MinF = MinF
        self.MinR = MinR
        self.SpeedRange = SpeedRange
        self.pin = pin
        self.pi = pi

        self.speed = Frequency*0.15
        pi.hardware_PWM(pin, Frequency, Frequency*0.15*10000) #Neutral Speed
        

     
    def setSpeed(self, speed):
        self.speed = speed
        DC = self.calcDutyCycle(speed)
        self.pi.hardware_PWM(self.pin, Frequency, DC)

    def calcDutyCycle(self, spd):  #Max Duty Cycle is 1 Million
        MinF = self.MinF
        MinR = self.MinR

        if(spd == 0):
            return Frequency*0.15*10000

        elif(spd>0):
            return (MinF + self.SpeedRange*spd/100)*10000

        elif(spd<0):
            return (MinR + self.SpeedRange*spd/100)*10000
            
        
