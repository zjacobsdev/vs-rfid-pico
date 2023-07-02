import time 
import machine
import network
import urequests
import os
# from machine import Pin
# import ntptime #sync time to local time over wifi

post_data = {
    "mail_lid_open": "false"
}


ssid = 'GL-MT300N-V2-731'
password = 'goodlife'

# Set up variables
check_interval_sec = 0.3
lid_sensor = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

#Status LEDs
led_red = machine.Pin(3,machine.Pin.OUT)
led_green = machine.Pin(4,machine.Pin.OUT)
led_blue = machine.Pin(5,machine.Pin.OUT)

#For Clearing out Common Anode RBG LED 
led_red.value(1)
led_green.value(1)
led_blue.value(1)


def wlan_connection():
        led_blue.off()
        time.sleep(.2)
        led_blue.on()
        time.sleep(.2)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
# if wlan.isconnected():
#     wlan_connection()
# else:
#     raise RuntimeError('failed to connect to lan')
print(wlan.isconnected())

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    wlan_connection()
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    led_blue.off()
    status = wlan.ifconfig()
    print('ip = ' + status[0])

# send_mail_status = urequests.get(
#     "http://192.168.8.188:8080/mailbox-status").json()
# print(send_mail_status)

# dt = time.localtime()
# timestamp = time.timestamp(dt)
# print(int(timestamp))


    


#Set pins with pulse width modulation
# pwm_blue = machine.PWM(led_blue,1000)

def blink_wifi_disconnected():
    led_blue.off()
    time.sleep(.2)
    led_blue.on()
    time.sleep(.2)

# def blick_wifi_connecting():
#         led_blue.off()
#         time.sleep(5)
#         led_blue.on()
#         time.sleep(5)














# Initial value for the sensor
sensor_value = None

# Main loop
while True:
    old_value = sensor_value
    sensor_value = lid_sensor.value()
    # print(lid_sensor.value)

    # Mailbox  is open.
    if sensor_value == 1:
        if old_value != sensor_value:
            # send_mail_status = urequests.post("http://192.168.8.188:8080/mailbox-status")
            # res = urequests.post( url, headers={
            #                      'content-type': 'application/json'}, json = post_data)
            # led_out.value(1)
            print('Mail box lid is open.')
            # led_out.value(0)
            # print(res.json())

        led_green.on()

    # Mailbox  is closed.
    elif sensor_value == 0:
        if old_value != sensor_value:
            #  res = urequests.post(url, headers={
            #  'content-type': 'application/json'}, json=post_data)
            print('Mail box lid is close.')
            #  print(res.json())
        led_green.off()

    time.sleep(check_interval_sec)

# from machine import Pin, Timer

# led = Pin("LED", Pin.OUT)
# tim = Timer()
# def tick(timer):
#     global led
#     led.toggle()

# tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)


# This example shows how to read the voltage from a LiPo battery connected to a Raspberry Pi Pico via our Pico Lipo SHIM
# and uses this reading to calculate how much charge is left in the battery.
# It then displays the info on the screen of Pico Display.
# Remember to save this code as main.py on your Pico if you want it to run automatically!

# from machine import ADC, Pin
# import time

# # change to DISPLAY_PICO_DISPLAY_2 for Pico Display 2.0
# from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
# display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)

# display.set_backlight(0.8)

# vsys = ADC(29)                      # reads the system input voltage
# charging = Pin(24, Pin.IN)          # reading GP24 tells us whether or not USB power is connected
# conversion_factor = 3 * 3.3 / 65535

# full_battery = 4.2                  # these are our reference voltages for a full/empty battery, in volts
# empty_battery = 2.8                 # the values could vary by battery size/manufacturer so you might need to adjust them

# # Create some pen colours for drawing with
# BLACK = display.create_pen(0, 0, 0)
# GREY = display.create_pen(190, 190, 190)
# GREEN = display.create_pen(0, 255, 0)
# RED = display.create_pen(255, 0, 0)

# while True:
#     # convert the raw ADC read into a voltage, and then a percentage
#     voltage = vsys.read_u16() * conversion_factor
#     percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
#     if percentage > 100:
#         percentage = 100.00

#     # draw the battery outline
#     display.set_pen(BLACK)
#     display.clear()
#     display.set_pen(GREY)
#     display.rectangle(0, 0, 220, 135)
#     display.rectangle(220, 40, 20, 55)
#     display.set_pen(GREEN)
#     display.rectangle(3, 3, 214, 129)

#     # draw a green box for the battery level
#     display.set_pen(GREEN)
#     display.rectangle(5, 5, round(210 / 100 * percentage), 125)

#     # add text
#     display.set_pen(RED)
#     if charging.value() == 1:         # if it's plugged into USB power...
#         display.text("Charging!", 15, 55, 240, 4)
#     else:                             # if not, display the battery stats
#         display.text('{:.2f}'.format(voltage) + "v", 15, 10, 240, 5)
#         display.text('{:.0f}%'.format(percentage), 15, 50, 240, 5)

#     display.update()
#     time.sleep(0.5)
