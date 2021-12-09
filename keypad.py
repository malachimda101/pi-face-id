import RPi.GPIO as GPIO
import time
master_code = "3333"

def read_passwords():
	passwords = {}
	f = open("passwords.txt", "r")
	lines = (f.readlines())
	for line in lines:
		pass_list = line.split()
		code = pass_list[0]
		name = pass_list[1]
		passwords[code] = name
	f.close()
	return passwords

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_char(line, characters):
	GPIO.output(line, GPIO.HIGH)
	if(GPIO.input(C1) == 1):
		return (characters[0])
	if(GPIO.input(C2) == 1):
		return (characters[1])
	if(GPIO.input(C3) == 1):
		return (characters[2])
	if(GPIO.input(C4) == 1):
		return (characters[3])
	GPIO.output(line, GPIO.LOW)
	return None

def validate_code():
	time.sleep(0.75)
	passwords = read_passwords()
	code = ""
	while len(code) < 4:
		l1 = read_char(L1, ["1","2","3","A"])
		l2 =  read_char(L2, ["4","5","6","B"])
		l3 = read_char(L3, ["7","8","9","C"])
		l4 =  read_char(L4, ["*","0","#","D"])
		if l1: code += l1
		elif l2: code += l2
		elif l3: code += l3
		elif l4: code += l4
		time.sleep(0.175)
	print(code)
	return passwords[code] if code in passwords else None

def create_password():
	time.sleep(0.75)
	passwords = read_passwords()
	print("Please enter a 4 digit passcode.")
	code = ""
	while True:
		l1 = read_char(L1, ["1","2","3","A"])
		l2 =  read_char(L2, ["4","5","6","B"])
		l3 = read_char(L3, ["7","8","9","C"])
		l4 =  read_char(L4, ["*","0","#","D"])
		if l1: code += l1
		elif l2: code += l2
		elif l3: code += l3
		elif l4: code += l4
		if code in passwords or code==master_code:
			code = ""
			print("That password is already taken. Please choose another.")
		if len(code) == 4 and code not in passwords:
			print("Thank you. Your password is", code + ".")
			return code
		time.sleep(0.175)

def make_choice():
	time.sleep(0.75)
	while True:
		code = ""
		l1 = read_char(L1, ["1","2","3","A"])
		l2 =  read_char(L2, ["4","5","6","B"])
		l3 = read_char(L3, ["7","8","9","C"])
		l4 =  read_char(L4, ["*","0","#","D"])
		if l1: code += l1
		elif l2: code += l2
		elif l3: code += l3
		elif l4: code += l4
		if code == "*" or code == "#":
			return code

def enable_signup():
	time.sleep(0.75)
	code = ""
	while len(code) < 4:
		l1 = read_char(L1, ["1","2","3","A"])
		l2 =  read_char(L2, ["4","5","6","B"])
		l3 = read_char(L3, ["7","8","9","C"])
		l4 =  read_char(L4, ["*","0","#","D"])
		if l1: code += l1
		elif l2: code += l2
		elif l3: code += l3
		elif l4: code += l4
		time.sleep(0.175)
	print(code)
	return code == master_code