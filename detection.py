import cv2
import numpy as np
import os
import sqlite3
import pyttsx3
import time

last_spoken_time = 0
engine = pyttsx3.init()


facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
camera = cv2.VideoCapture(0)
engine.say("Hello, starting face recognition")
engine.runAndWait()


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

def getProfile(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.execute("SELECT * FROM STUDENTS WHERE id=?", (id,))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

# Initialize start time and Set the duration for which the loop should run without detecting faces
start_time = time.time()
no_face_duration = 12
last_face_detected_time = time.time()

while(True):
    ret,img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3,5)
    # print("Recognizer ready:", recognizer.getLabelsByString(''))

    # Update the last detected time if faces are found
    if len(faces) > 0:
        last_face_detected_time = time.time()

    print(time.time() - last_face_detected_time)

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        id,conf = recognizer.predict(gray[y:y+h,x:x+h])
        profile=getProfile(id)
        print(profile)
        if(profile != None):
            cv2.putText(img, "Name:" + str(profile[1]), (x,y+h+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,127), 2)
            if time.time() -last_spoken_time > 5:
                engine.say(f"Hello {profile[1]}")
                engine.runAndWait()
                last_spoken_time = time.time()

    cv2.imshow("FACE", img)

    # Check if the elapsed time since the last face was detected exceeds the no_face_duration
    if time.time() - last_face_detected_time > no_face_duration:
        break

    if(cv2.waitKey(1)==ord('q')):
        break

engine.say("Goodbye, closing the program")
engine.runAndWait()
camera.release()
cv2.destroyAllWindows()