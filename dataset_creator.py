import cv2
import numpy as np
import sqlite3

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);  #0 is for camera

def insertorupdate(Id,Name): #sqlite
    conn=sqlite3.connect("database.db")
    cmd="SELECT * FROM STUDENTS WHERE ID=" + str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if isRecordExist==1:
        conn.execute("UPDATE STUDENTS SET Name=? WHERE Id=?", (Name, Id,))
    else:
        conn.execute("INSERT INTO STUDENTS (Id, Name) values(?,?)", (Id,Name))

    conn.commit()
    conn.close()

    # Get user details
id = input('Enter user ID: ')
name = input('Enter user name: ')


insertorupdate(id, name)

sampleNum = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        sampleNum += 1
        cv2.imwrite(f"dataset/User.{id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.waitKey(100)

    cv2.imshow('Face', img)
    cv2.waitKey(1)

    if sampleNum > 20:  # capture 20 samples then stop
        break

cam.release()
cv2.destroyAllWindows()