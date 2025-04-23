#importing necessary libraries
import cv2
import numpy as np
import sqlite3

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