import cv2
import numpy as np
import sqlite3

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);  #0 is for camera

def insertorupdate(Id,Name,age): #sqlite
    conn=sqlite3.connect("database")
    cmd="SELECT * FROM STUDENTS WHERE ID=" + str(Id);
    cursor=conn.execute(cmd);
    isRecordExist=0;
    for row in cursor:
        isRecordExist=1;
    if(isRecordExist==1):
        conn.execute("UPDATE STUDENTS SET Name=? WHERE Id=?", (Name, Id,))
        conn.execute("UPDATE STUDENTS SET age=? WHERE Id=?", (age, Id,))
    else:
        conn.execute("INSERT INTO STUDENTS (Id, Name, age) values(?,?,?)", (Id,Name,age))

    conn.commit()
    conn.close()