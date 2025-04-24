#importing necessary libraries
import cv2
import numpy as np
import sqlite3

#grabs the correct section of opencv
faceDetect=cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

#starts camera recognition
cam=cv2.VideoCapture(0)

#deals with updating the dataset
def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("faceDatabase.db")
    cmd="SELECT * FROM Peoples WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0

    for row in cursor:
        isRecordExist=1

    if(isRecordExist==1):
        # cmd="UPDATE Peoples SET Name="+str(Name)+"WHERE id="+str(Id)
        conn.execute("UPDATE Peoples SET Name=? WHERE id=?", (Name,Id,))
    else:
        
        # cmd="INSERT INTO Peoples(id,Name) Values("+str(Id)+","+str(Name))"
        conn.execute("INSERT INTO Peoples(id,Name) Values(?,?,?,?)", (Id, Name))


    conn.commit()
    conn.close()

    
#allowing input
Id=input('Enter User Id:')
name=input('Enter User Name:')

insertOrUpdate(Id,name)
sampleNum=0

while(True):

    #placing a box around face to show recognition
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:

        #placing user information on screen
        sampleNum=sampleNum+1
        cv2.imwrite("dataSet/User."+str(Id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(400)
    
    cv2.imshow("Face",img)
    cv2.waitKey(1)
    if(sampleNum>20):
        break
cam.release()
cv2.destroyAllWindows()