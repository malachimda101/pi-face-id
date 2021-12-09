import cv2
import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
base_path = "/home/pi/Documents/idea_final/trained_faces/"

time.sleep(0.1)


def next_label(path):
    curr_labels = [-1]
    for dirs in os.listdir(path):
        for img in os.listdir(path + dirs):
            num, ext = (os.path.splitext(img))
            curr_labels.append(int(num))
    return max(curr_labels) + 1

def detect_face(gray):
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    return False if len(faces) == 0 else True

def capture_image(img_name):
    with PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, format="bgr")
            output.truncate(0)
            image = output.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if detect_face(gray):
                n_lab = next_label(base_path)
                name_d = base_path + img_name
                img_path = name_d + "/" + str(n_lab) +  '.jpg'
                try:
                    os.mkdir(name_d)
                except FileExistsError:
                    pass
                cv2.imwrite(img_path, gray)
                return image
            

def take_images(num=5):
    img_name = str(input("Please enter your name:"))
    for i in range(3 , 0, -1):
        print("Imgages taking in",i,"second(s).")
        time.sleep(1)
    for i in range(num):
        if capture_image(img_name) is not None:
            print("Face detected.")
            time.sleep(1.5)
        else:
            print("No face detected.")
    return img_name


def get_test_img():
    for i in range(3, 0, -1):
        print("Taking image in", i,"second(s).")
        time.sleep(1)
    print("Taking image.")
    with PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, format="bgr")
            image = output.array
            cv2.destroyAllWindows()
            return image