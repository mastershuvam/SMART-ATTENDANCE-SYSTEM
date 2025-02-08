from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(str1):
    engine.say(str1)
    engine.runAndWait()

# Load the face detection model
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load the labels and face data
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Initialize the KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Load the background image
background_img = cv2.imread('/Users/shuvamghosh/Desktop/Smart Attendance/background.png')

# Resize the background image to fit the display window
background_img = cv2.resize(background_img, (1280, 720))

# Create or open the attendance CSV file
date = datetime.now().strftime('%Y-%m-%d')
attendance_file = f'Attendance/Attendance_{date}.csv'
COL_NAMES = ['Name', 'Time']

if not os.path.exists('Attendance'):
    os.makedirs('Attendance')

if not os.path.exists(attendance_file):
    with open(attendance_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(COL_NAMES)

attendance = []
recorded_names = set()

while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        resized_img_flatten = resized_img.flatten().reshape(1, -1)
        label = knn.predict(resized_img_flatten)
        name = label[0]

        if name not in recorded_names:
            speak(f"Hello {name}")
            recorded_names.add(name)
            attendance.append([name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

        # Draw green rectangle around the face and display the name above it
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Resize the frame to fit into the background
    resized_frame = cv2.resize(frame, (640, 480))
    img_with_frame = background_img.copy()
    img_with_frame[120:120 + 480, 320:320 + 640] = resized_frame

    cv2.imshow("Frame", img_with_frame)
    k = cv2.waitKey(1)
    if k == ord('o'):
        speak("Attendance Taken..")
        time.sleep(5)
        if os.path.exists(attendance_file):
            with open(attendance_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(attendance)
        else:
            with open(attendance_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerows(attendance)
        attendance = []  # Clear the attendance list after writing to the file
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()