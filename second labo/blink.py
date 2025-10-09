import machine  
import utime
 
Rotary_sensor = machine.ADC(0)
buzzer = machine.PWM(machine.Pin(16))
score = {"DO":[1046, 0.25],"MI" :[1318, 0.25], "FA" :[1397, 0.25],
        "RE":[1175,0.25], "SOL" : [1568, 0.5], "LA" :[1760, 0.125],
        "SI":[1967, 0.5] }
star_wars_theme_simplifie = [
    "SOL", "SOL", "SOL", "MI",
    "SI", "SOL", "MI", "SI", "SOL",
    "RE", "RE", "RE", "MI", "SI", "FA", "MI", "SI", "SOL"
]
 
def music_notes(score, notes) :
    resistance = Rotary_sensor.read_u16()
    instensity = int(resistance *0.23)
    buzzer.freq(score[notes][0])
    buzzer.duty_u16(instensity)
    utime.sleep(score[notes][1])
 
while True:
    #print(Rotary_sensor.read_u16())
    # divide in 16 states of reading by 4096 8192 12288 16384 20480 24576 28672 32768 38864 40960 45056 49152 53248 57344 61440 last
    for i in range (len(star_wars_theme_simplifie)):
        Note = star_wars_theme_simplifie[i]
        music_notes(score, Note)
        
