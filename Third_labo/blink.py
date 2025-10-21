#<----------------------------------->
#Importation of the different librairies
from machine import Pin, I2C, ADC
from utime import sleep
from lcd1602 import LCD1602
from dht20 import DHT20
import machine,utime
#<////////////////////////////////////>
    
#<----------------------------------->
#Configuration of the different sensors, display and other, ...
I2c = I2C(1)
dht20 = DHT20(I2c)
temperature = dht20.dht20_temperature()
Rotary_sensor = machine.ADC(2)  
i2c = I2C(0,scl=Pin(9), sda=Pin(8), freq=400000)
display = LCD1602(i2c, 2, 16)
display.display()
buzzer = machine.PWM(machine.Pin(16))
LED = machine.PWM(machine.Pin(18))
LED.freq(1000)  # PWM rapide et stable
buzzer.freq(1046)
#<////////////////////////////////////>

#<----------------------------------->
#Initialization of the different set times
last_time = utime.ticks_ms()
last_time_delete = last_time
last_time_temp = last_time
last_time_led = last_time
#<////////////////////////////////////>

#<----------------------------------->
#Initialization of the datas which will be incremented or changed
diviseur=1
etat = True
index_alarm = 0
efface = True
index_alarm_position = 0
affiche = True
#<////////////////////////////////////>


#<----------------------------------->
#Utilisation of the different sensors and transformation of the data
def sensors():
    new_time = utime.ticks_ms()
    resistance = Rotary_sensor.read_u16()
    temp=int(resistance/3120.761905)+15
    ref_duty = int(0.9*resistance+6535)
    return new_time,temp,resistance, ref_duty
#<////////////////////////////////////>

#<----------------------------------->
#Function which subtracted the inital time and the currently time
def difference_time(new_time,last_time):
    return new_time-last_time
#<////////////////////////////////////>

def display_clear(new_time, last_time_delete, efface):
    if 500 < (difference_time(new_time,last_time_delete)):
        display.clear()
        last_time_delete = new_time
        efface = True
        affiche = True
    else :
        affiche = False

    return last_time_delete, efface, affiche

def take_temperature(last_time_temp, temperature, new_time):
     # peut importe l'affichage 
    temperature = dht20.dht20_temperature()
    last_time_temp = new_time
    return temperature, last_time_temp

def Display(affiche, temperature, display):
    if affiche:
        display.setCursor(0,0)
        display.print("Ambient:"+"{:.1f}".format(temperature))

def Led(etat,ref_duty, new_time, last_time_led):
    if etat:

        LED.duty_u16(0)        # LED éteinte
        etat = False
    else:
        LED.duty_u16(ref_duty) # LED allumée avec luminosité
        etat = True
    last_time_led = new_time
    return last_time_led, etat

def display_alarm_set(temperature, temp, efface, display, buzzer, index_alarm_position, index_alarm, resistance, diviseur):
    if temperature >=  int(resistance/3120.761905)+3+15:
        
        buzzer.duty_u16(12000)
        diviseur = 4
        if efface:
            efface = False
                
            if index_alarm_position%2==0 :
                display.setCursor(index_alarm,1)
                display.print("ALARM")
                    
            else :
                index_alarm+=1
            if index_alarm ==11:
                index_alarm=0
                index_alarm_position+=1
    else :
        buzzer.duty_u16(0) 
        display.setCursor(0,1)
        display.print("SET:"+"{:.1f}".format(temp))
        diviseur = 1
    return index_alarm_position, diviseur, efface


while True:
    
    new_time,temp,resistance, ref_duty = sensors()

        
    last_time_delete, efface, affiche = display_clear(new_time, last_time_delete, efface)


    if 1000 < (difference_time(new_time,last_time_temp)):
        temperature, last_time_temp = take_temperature(last_time_temp, temperature, new_time)
   
 
    Display(affiche, temperature, display)
 
    index_alarm_position, diviseur, efface = display_alarm_set(temperature, temp, efface, display,buzzer, index_alarm_position, index_alarm, resistance, diviseur)
       
    if 250/diviseur< difference_time(new_time,last_time_led ) :  # toutes les 500 ms
        last_time_led, etat=Led(etat,ref_duty, new_time, last_time_led)
