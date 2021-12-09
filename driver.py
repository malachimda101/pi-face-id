from create_data import take_images, get_test_img
from face_recognize import run_prediction, train_recognizer
from keypad import validate_code, read_passwords, create_password, make_choice, enable_signup
import os
import time
import RPi.GPIO as GPIO
# test_img1 = cv2.imread("/home/pi/Documents/idea_final/trained_faces/Daniel/6.jpg")

solenoid = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid, GPIO.OUT)
passwords = read_passwords()

def run_project():
    print("Training on images...")
    train_recognizer()
    GPIO.output(solenoid, GPIO.LOW)
    print("System setup complete.")
    while True:
        time.sleep(3)
        os.system("clear")
        print("Welcome to SM Security.")
        print("Press '*' on keypad to login or '#' on keypad to signup.")
        logsign = make_choice()
        os.system('clear')
        if logsign == '#':
            print("Press '*' on keypad to enable signup with face id or '#' on keypad to enable signup with master code.")
            sign_check = make_choice()
            if sign_check == "#":
                print("Please enter master code to signup.")
                singup_enabled = enable_signup()
                if singup_enabled:
                    signup()
                else:
                    print("Signup unavailable.")
            elif sign_check == "*":
                signup_img = get_test_img()
                print("Making prediction...")
                prediction, name = run_prediction(signup_img)
                time.sleep(1.5)
                if prediction:
                    signup()
                else:
                    print("Signup unavailable.")
        elif logsign == '*':
            login()


def signup():
    time.sleep(3)
    os.system("clear")
    print("Signup access granted.")
    time.sleep(0.1)
    name = take_images()
    print("Images have been taken.")
    code = create_password()
    passwords[code] = name
    f = open("passwords.txt", "w")
    for key in passwords:
        f.write(key + " " + passwords[key] + "\n")
    f.close()
    train_recognizer()
    print("Signup complete.")


def login():
    print("How would you like to login? Press '*' on keyapd for face identification, '#' on keypad for keypad entry.")
    mode = make_choice()
    os.system("clear")
    if mode == "*":
        test_img1 = get_test_img()
        os.system("clear")
        print("Making prediction...")
        prediction, name = run_prediction(test_img1)
        time.sleep(1.5)
        if prediction:
            GPIO.output(solenoid, GPIO.HIGH)
            print("Access granted by face identification. Welcome", name + ".")
            time.sleep(10)
            GPIO.output(solenoid, GPIO.LOW)
        else:
            print("Access denied by face id. Press '#' on keypad to login with keypad or '*' to exti.")
            keypad = make_choice()
            os.system("clear")
            if keypad == '#':
                print("Please enter passcode:")
                name = validate_code()
                if name != None:
                    GPIO.output(solenoid, GPIO.HIGH)
                    print("Access granted by keypad. Welcome",name + ".")
                    time.sleep(10)
                    GPIO.output(solenoid, GPIO.LOW)
                else:
                    print("Access denied.")
            else:
                print("Access denied.")
    elif mode == "#":
        print("Please enter passcode:")
        name = validate_code()
        if name != None:
            GPIO.output(solenoid, GPIO.HIGH)
            print("Access granted by keypad. Welcome",name + ".")
            time.sleep(10)
            GPIO.output(solenoid, GPIO.LOW)
        else:
            print("Access denied.")
    time.sleep(3)
    os.system("clear")


if __name__ == "__main__":
    run_project()
