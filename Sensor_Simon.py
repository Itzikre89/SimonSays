
import RPi.GPIO as gpio
import time
import random
import wiringpi
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

lights_arr = [4, 17, 27,22] #yellow, blue, red, green
sensors_arr = [0, 1, 2, 3] #light, Michrophone, fire, Motion

sound_gpiopin = 19
wiringpi.wiringPiSetupGpio()
gpio.setmode(gpio.BCM)

def make_sound(color, pin):
    wiringpi.softToneCreate(sound_gpiopin)
    freq = 0
    if color == 4:
        freq = 659
    elif color == 17:
        freq = 440
    elif color == 27:
        freq = 784
    elif color == 22:
        freq = 523
    elif color == 0:
        freq = 900
    wiringpi.softToneWrite(pin, freq)
    time.sleep(0.5)
    wiringpi.softToneStop(sound_gpiopin)

def make_rand_arr(size, arr):
    rand_arr = []
    for i in range(0,size):
        rand_arr.append(random.choice(arr))
    return rand_arr

def lights_off():
  for i in range(len(lights_arr)):
    gpio.output(lights_arr[i], 0)


def sensor_input():
  while True:
    time.sleep(0.01)
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)

    # light
    if values[0] > 35:
      print("light")
      return 0
    # Sound
    elif values[1] < 450:
      print("Sound")
      return 1
    elif values[2] < 400:
      print("fire")
      return 2
    elif values[3] < 400:
      print("motion")
      return 3
  return -1


for i in range(len(lights_arr)):
    gpio.setup(lights_arr[i], gpio.OUT)
    gpio.setup(sensors_arr[i], gpio.IN, pull_yup_down=gpio.PUD_DOWN)


lights_off()
sequence_size = 1
sequence_arr = make_rand_arr(sequence_size,lights_arr)

game_on = True


while game_on:
        print(len(sequence_arr))
        for i in range(len(sequence_arr)):
            time.sleep(1)
            gpio.output(sequence_arr[i], 1)
            make_sound(sequence_arr[i], sound_gpiopin)
            gpio.output(sequence_arr[i], 0)

        for i in range(len(sequence_arr)):
            input = sensor_input()
            gpio.output(lights_arr[input], 1)
            time.sleep(0.5)
            gpio.output(sequence_arr[i], 0)
            if (lights_arr[input] == sequence_arr[i]):
                print("good")
                make_sound(sequence_arr[i], sound_gpiopin)
            else:
                print("Bad")
                make_sound(0, sound_gpiopin)
                answer = raw_input("game over do you want play again? y/n\n")
                lights_off()
                if answer == 'y':
                    sequence_size = 0
                    break
                else:
                     game_on = False
                     print("GoodBye!!")
                     break
        sequence_size = sequence_size + 1
        sequence_arr = make_rand_arr(sequence_size, lights_arr)
    


