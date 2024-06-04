#Home systen
import network
import socket

from time import sleep
from ahtx0 import AHT10
from machine import Pin, I2C
from hcsr04 import HCSR04
from ahtx0 import AHT10
from umqtt.simple import MQTTClient

import random
import wificonnect

led = Pin(18, Pin.OUT)
pir_pin = Pin(13, Pin.IN)
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = AHT10(i2c)
distance_sensor = HCSR04(trigger_pin=2, echo_pin=3)
led_red = Pin(16, Pin.OUT)
led_green = Pin(17, Pin.OUT)
button = Pin(12, Pin.IN, Pin.PULL_DOWN)

led_red.value(0)
led_green.value(0)


mqtt_server = 'io.adafruit.com'
mqtt_port = 1883 # non-SSL port
mqtt_user = 'Matutozi' #Adafruit ID
mqtt_password = '' # Under Keys
mqtt_topic = 'Matutozi/feeds/temperature' # Under "Feed info"
mqtt_client_id = str(random.randint(10000,999999)) #must have a unique ID - good enough for now

wlan = network.WLAN(network.STA_IF)

sleep(1)
print(" HOME SYSTEM ")

correct_password = "12345"
key_inserted = False

def request_password():
    print("Please enter the password:")
    entered_password = input()
    return entered_password
def mqtt_connect():
    client = MQTTClient(client_id=mqtt_client_id, server=mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

while True:
    if pir_pin.value():
        print("Motion detected")
        sleep(0.1)
        led.on()
        print(f"Temperature of the room is {sensor.temperature:.1f}°C")
        sleep(1)
        distance = distance_sensor.distance_cm()
        print('Distance:', distance, 'cm')
        
        if wlan.isconnected():
            client.publish(mqtt_topic, str(sensor.temperature))
            #client.publish(mqtt_topic, str("Intruder alert"))

        else:
            reconnect()
        sleep(20)
        if distance < 40 and not key_inserted:
            entered_password = request_password()
            if entered_password == correct_password:
                print("Insert Key")
                print("-----------------")
                print("Welcome Home")
                key_inserted = True
            else:
                print("Incorrect password, INTRUDER.")
                if wlan.isconnected():
                    client.publish(mqtt_topic, str("INTRUDER AT THE DOOR"))
                else:
                    reconnect()
                sleep(20)
                
        
        if sensor.temperature <= 24:
            print("Room is too cold, turn on heater")thhomee
            led_red.toggle()
            if button.value():
                led_red.off()
                print("reasonable explanation like during cooking")
            sleep(.8)
            
        if sensor.temperature >=24 and sensor.temperature <= 29:
            print("Room is at optimum temperature")
            led_green.on()
            if wlan.isconnected():
                client.publish(mqtt_topic, str("OPTIMUM TEMPERATURE"))
            else:
                reconnect()
            
            sleep(20)
            sleep(1)
            
        if sensor.temperature > 40:
            print("Danger, Too Hot")
            led_red.toggle()
            if wlan.isconnected():
                client.publish(mqtt_topic, str("DANGER TEMP TOO HIGH"))
            else:
                reconnect()
            
            sleep(20)
            sleep(.1)           
        
    else:
        led.off()
        key_inserted = False



