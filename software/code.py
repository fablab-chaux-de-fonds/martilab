# import libraries
import time
import alarm
import board
import busio
import digitalio
import adafruit_ds1307
from DFPlayer import DFPlayer

# set time after changing the battery.
# Uncomment the following line and set the current time
# rtc.datetime = time.struct_time((2024, 2, 8, 18, 29, 0, 0, -1, -1))

# initialize DFPlayer
df_player_pin = digitalio.DigitalInOut(board.GP15)
df_player_pin.direction = digitalio.Direction.OUTPUT
df_player_pin.value = False

time.sleep(2)

dfplayer = DFPlayer(volume=60)

# initialize RTC
# Set bus io. More info:
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/pinouts
i2c = busio.I2C(scl=board.GP13, sda=board.GP12)

# Initialise rtc
rtc = adafruit_ds1307.DS1307(i2c)

while True:
    print(rtc.datetime)
    
    print('Turn on dfplayer')
    df_player_pin.direction = digitalio.Direction.OUTPUT
    time.sleep(1)
    dfplayer.play()
    time.sleep(5)
    
    print('Turn off dfplayer')
    df_player_pin.direction = digitalio.Direction.INPUT
    time.sleep(2)

#time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 5)
#print("start sleep")
#alarm.exit_and_deep_sleep_until_alarms(time_alarm)
#print(rtc.datetime)

# if rtc.datetime.tm_sec%10 == 0:
    #dfplayer.set_standby(on=True)
# elif rtc.datetime.tm_sec%10 == 5:
#     pass
    #dfplayer.set_standby()

#
