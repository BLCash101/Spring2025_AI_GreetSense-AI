import cv2
import sqlite3
from datetime import datetime

# Initialize face recognizer and load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

# Connect to database
def get_student_name(student_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students WHERE id=?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def log_event(student_id, event_type="entry"):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs (student_id, timestamp, event_type) VALUES (?, ?, ?)", (student_id, timestamp, event_type))
    conn.commit()
    conn.close()

# Start webcam
cam = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        student_id, confidence = recognizer.predict(face_roi)

        if confidence < 70:  # Confidence threshold (lower is better)
            name = get_student_name(student_id)
            if name:
                cv2.putText(img, f"{name}", (x, y-10), font, 1, (0,255,0), 2)
                log_event(student_id, event_type="entry")
            else:
                cv2.putText(img, "Unknown", (x, y-10), font, 1, (0,0,255), 2)
        else:
            cv2.putText(img, "Unknown", (x, y-10), font, 1, (0,0,255), 2)

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Recognizing and Logging', img)

    # Press q to quit
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
