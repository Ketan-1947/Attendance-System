#import modules
from dlib import get_frontal_face_detector
import cv2 as cv
import numpy as np
from tkinter import *
from sklearn.neighbors import KNeighborsClassifier
import psycopg2 as psql

#connecting to database
try:
    psqlcon = psql.connect(host="localhost",user="postgres",password="zp17dmtijm",database="test")
except (Exception, psql.DatabaseError) as error:
    print("Failed to connect to postgres")

#creating cursor
psqlcur = psqlcon.cursor()

#capturing video
class Video():
    def __init__(self):
        self.FaceData = np.load("FaceData.npy")
        self.face = self.FaceData[: , :-1].astype(int)
        self.enrollment = self.FaceData[: , -1]
        self.model = KNeighborsClassifier()
        self.model.fit(self.face ,self.enrollment)
        self.presentStudents = dict()
        self.counter = 1
        
    def capture(self,Class):
        cap = cv.VideoCapture(0)
        while True:
            ret,frame = cap.read()
            frame = cv.flip(frame,1)
            
            if ret:
                cv.imshow("frame",frame)

            key = cv.waitKey(100)
            if key == ord('q'):
                cap.release()
                cv.destroyAllWindows()
                self.TakeAttendance(Class)
                break
            
            if key == ord('c'):
                self.PredictFaces(frame);
        

    def PredictFaces(self,frame):
        detector = get_frontal_face_detector()
        faces = detector(frame)
        for face in faces:
            x1 = face.left()
            y1 = face.top()-70
            x2 = face.right()
            y2 = face.bottom()

            face = frame[y1:y2 , x1:x2]
            face = cv.resize(face , (200,200))
            face = cv.cvtColor(face,cv.COLOR_BGR2GRAY)
            face = face.reshape(1,-1)
            print(face.shape)
            enrollment = self.model.predict(face)
            distance, index = self.model.kneighbors(face)
            if distance[0][0] < 9000:
                self.presentStudents[enrollment[0]] = True
                cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv.putText(frame,enrollment[0],(x1,y1),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        
        while True:
            cv.imshow("frame",frame)
            cv.putText(frame,"Press 'c' to close",(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            key = cv.waitKey(100)

            if key == ord('c'):
                break



    def TakeAttendance(self,Class):
        students = np.load("Students.npy" , allow_pickle=True).item()
        for i in students:
            psqlcur.execute("select present from {} where day = CURRENT_DATE and enrollment = '{}';".format(Class,i))
            marked = psqlcur.fetchone()
            if marked == None:
                try:
                   if self.presentStudents[i]:
                       psqlcur.execute("insert into {} values('{}','{}',CURRENT_DATE,'{}');".format(Class,i,students[i],True))
                except Exception as e:
                    psqlcur.execute("insert into {} values('{}','{}',CURRENT_DATE,'{}');".format(Class,i,students[i],False))
            elif marked[0] == False:
                try:                                        
                    if self.presentStudents[i]:
                        psqlcur.execute("update {} set present = True where enrollment = '{}' and day = CURRENT_DATE;".format(Class,i)) 
                except Exception as e:
                    continue

        psqlcon.commit()
            

vid = Video()
vid.capture("fml")
