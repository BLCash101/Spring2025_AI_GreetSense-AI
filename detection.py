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

while(True):
    ret,img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3,5)
    print("Recognizer ready:", recognizer.getLabelsByString(''))
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        id,conf = recognizer.predict(gray[y:y+h,x:x+h])
        profile=getProfile(id)
        print(profile)
        if(profile != None):
            cv2.putText(img, "Name:" + str(profile[1]), (x,y+h,+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,127), 2)
            engine.say(f"Hello {profile[1]}")
            engine.runAndWait()
            last_spoken_time = time.time()

    cv2.imshow("FACE", img)
    if(cv2.waitKey(1)==ord('q')):
        break

engine.say("Goodbye, closing the program")
engine.runAndWait()
camera.release()
cv2.destroyAllWindows()