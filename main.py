from mqtt import MQTTClient
import time
import ujson
import machine
import config
import time
import pycom
from pycoproc_2 import Pycoproc
import machine


from SI7006A20 import SI7006A20         #library for humidity and temperature
from LTR329ALS01 import LTR329ALS01     #library for light sensor


pycom.heartbeat(False)                  #disabling the heartbeat flash light


def sub_cb(topic, msg):
   print(msg)

# Setting up MQTT client
client = MQTTClient(config.SERIAL_NUMBER,
                    config.MQTT_BROKER,
                    user=config.TOKEN,
                    password=config.TOKEN,
                    port=config.PORT)
client.set_callback(sub_cb)
client.connect()
print('connected to Datacake MQTT broker')

# The MQTT topic that the data is published to
topic_temp =  config.TOPIC_temp          #MQQT topic for temperature
topic_humid = config.TOPIC_humid         #MQQT topic for humidity
topic_illum = config.TOPIC_illum         #MQQT topic for illuminance

py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:    #ensuring that connected board is pysense
    raise Exception('Not a Pysense')

#measuring and publishing the data to the Datacake
while True:
    #Continuous sensing of temperature, humidity and illumination
    print("Measuring the Crib Temperature, Humidity and Illuminance")
    si = SI7006A20(py)
    lt = LTR329ALS01(py)
    temp = si.temperature()
    humid = si.humidity()
    print("Temperature: " + str(temp)+ " deg C")
    print("Humidity: " + str(humid))
    Lux = lt.lux()
    print("Illuminance: " + str(Lux))

    # Publishing to MQQT broker on given topics
    client.publish(topic=topic_temp, msg=str(temp))
    client.publish(topic=topic_humid, msg=str(humid))
    client.publish(topic=topic_illum, msg=str(Lux))
    client.check_msg()
    print("Data Sent to Data cake, sleeping for 2 minutes...")
    time.sleep(120) # Wait 2 minutes (120 seconds)
