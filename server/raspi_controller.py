import RPi.GPIO as GPIO
import time

baterrys = [18, 12]
reds = [5,17, 23, 16]
greens = [6,27, 24, 20]
blues = [13,22, 25, 21]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def convertDict(arg1, arg2, arg3):
	d = {'arg1': arg1, 'arg2': arg2, 'arg3': arg3}
	return d

def switchLed(arg1, arg2, arg3):
	GPIO.output(arg1[0], arg1[1])
	GPIO.output(arg2[0], arg2[1])
	GPIO.output(arg3[0], arg3[1])

def batteryOn():
	for battery in baterrys:
		GPIO.setup(battery, GPIO.OUT)
		GPIO.output(battery, True)

def run():
	batteryOn()
	for i in range(1):
		print 'ON'
		for(red, green, blue) in zip (reds, greens, blues):
			GPIO.setup(red,GPIO.OUT)
			GPIO.setup(green,GPIO.OUT)
			GPIO.setup(blue,GPIO.OUT)
			ledOn = convertDict([red, False], [green, True], [blue, True])
			switchLed(**ledOn)
		time.sleep(1)

		for(red, green, blue) in zip (reds, greens, blues):
			ledOn = convertDict([red, True], [green, False], [blue, True])
			switchLed(**ledOn)
		time.sleep(1)

		for(red, green, blue) in zip (reds, greens, blues):
			ledOn = convertDict([red, True], [green, True], [blue, False])
			switchLed(**ledOn)
		time.sleep(1)

		for (red, green, blue) in zip(reds, greens, blues):
			ledOn = convertDict([red, False], [green, False], [blue, False])
			switchLed(**ledOn)
		time.sleep(1)

		for(red, green, blue) in zip (reds, greens, blues):
			ledOff = convertDict([red, True], [green, True], [blue, True])
			switchLed(**ledOff)


if __name__ == '__main__':
    run()
