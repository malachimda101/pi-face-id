import cv2
import os
import numpy as np


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
base_path = "/home/pi/Documents/idea_final/trained_faces/"
subjects = {}
faces = []
labels = []


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if len(faces) == 0:
        return None, None

    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def prepare_data(path):
    dir_list = os.listdir(path)
    for dirs in dir_list:
        name = dirs
        for img in os.listdir(path + dirs):
            num, ext = (os.path.splitext(img))
            image = cv2.imread(path+dirs+"/"+img)
            if int(num) not in subjects:
                face, rect = detect_face(image)
                if face is not None:
                    subjects[int(num)] = name
                    faces.append(face)
                    labels.append(int(num))
    cv2.destroyAllWindows()
    return faces, labels, subjects

def predict(test_img, subjects):
    if test_img is not None:
        img = test_img.copy()
        face, rect = detect_face(img)
        if face is None:
            return None, None
        label = face_recognizer.predict(face)[0]
        label_text = subjects[label]
        return img, label_text

os.system("clear")
print("Booting up...")
# faces, labels, subjects = prepare_data('/home/pi/Documents/idea_final/trained_faces/')

def train_recognizer():
    faces, labels, subjects = prepare_data('/home/pi/Documents/idea_final/trained_faces/')
    face_recognizer.train(faces, np.array(labels))


def run_prediction(img):
    predicted_img1, name = predict(img, subjects)
    if predicted_img1 is not None:
        cv2.destroyAllWindows()
        return True, name
    else:
        return  False, None
