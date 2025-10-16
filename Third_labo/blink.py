from machine import Pin,I2C
from utime import sleep
from lcd1602 import LCD1602
from dht11 import *

dht=DHT(18)
temp=dht.readTemperature()
humid=dht.readTemperature()
print(temp)


