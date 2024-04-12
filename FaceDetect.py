#import modules
from dlib import get_frontal_face_detector
import cv2 as cv
import numpy as np
from tkinter import *
import mysql.connector as sql
from sklearn.neighbors import KNeighborsClassifier


#connecting to database
mycon = sql.connect(host="localhost",user="root",password="zp17dmtijm",database="attendance")

#checking connection
if mycon.is_connected():
    print("Connected to database")
else:
    print("Failed to connect")

#creating cursor
myc = mycon.cursor()


#capturing video
class Video():
    def __init__(self):
        self.FaceData = np.load("FaceData.npy")
        self.name = self.FaceData[: , 0]
        self.face = self.FaceData[: , 1:].astype(int)
        self.model = KNeighborsClassifier()
        self.model.fit(self.face ,self.name)
        
    def capture(self,Class):
        detector = get_frontal_face_detector()
        cap = cv.VideoCapture(0)
        while True:
            ret,frame = cap.read()
            frame = cv.flip(frame,1)
            if ret:
                faces = detector(frame)
                if len(faces) != 0:
                    face = faces[0]
                    x1 = face.left()
                    y1 = face.top()
                    x2 = face.right()
                    y2 = face.bottom()
                    faceFrame = frame[y1:y2,x1:x2]
                    faceFrame = cv.resize(faceFrame,(200,200))
                    cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,255),2)

                    #making face gray
                    GrayFace = cv.cvtColor(faceFrame , cv.COLOR_BGR2GRAY)
                    cv.imshow("face",GrayFace)
                    GrayFace = np.array(GrayFace).flatten()
                    
                    #predicting face
                    name = self.PredictFace([GrayFace])
                    self.TakeAttendance(Class , name)
                cv.imshow("frame",frame)
                
            key = cv.waitKey(10)
            if key == ord('q'):
                cap.release()
                cv.destroyAllWindows()
                break
        
    def GetClass(self):
        screen = Tk()
        screen.geometry("500x500")
        screen.resizable(0,0)
        screen.title("Class")

        entry = Entry(screen)
        entry.place(x=160 , y=200 , width=200 , height=50)

        button = Button(screen , text="Submit" , command=lambda: (self.capture(entry.get()),screen.destroy()))
        button.place(x=160 , y=300 , width=200 , height=50)

    def PredictFace(self,face):
        return self.model.predict(face)[0]

    def TakeAttendance(self, Class,name):
        print(Class,name)

# vid = Video()
# vid.capture("ML")
