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
                    y1 = face.top()-70
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
                    enrollment = self.PredictFace([GrayFace])
                    
                    if enrollment != "not recognized":
                        cv.putText(frame,enrollment,(x1,y1),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                        if enrollment[0] not in self.presentStudents:
                            self.presentStudents[enrollment] = self.counter
                    else:
                        cv.putText(frame,enrollment,(x1,y1),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    
                else:
                    cv.putText(frame,"No face detected",(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                cv.imshow("frame",frame)
                
            key = cv.waitKey(100)
            if key == ord('q'):
                cap.release()
                cv.destroyAllWindows()
                self.TakeAttendance(Class)
                break
        

    def PredictFace(self,face):
        distances ,items= self.model.kneighbors(face)
        if distances[0][0] > 9000:
            return "not recognized"
        return self.model.predict(face)[0]
        

    # def TakeAttendance(self, Class):
    #     students = np.load("Students.npy" , allow_pickle=True).item()
    #     for i in students:
    #         try:
    #             if self.presentStudents[i]:
    #                 psqlcur.execute("select present from {} where day = CURRENT_DATE and enrollment = '{}';".format(Class,i))
    #                 marked = psqlcur.fetchone()
    #                 if marked == None:
    #                     psqlcur.execute("insert into {} values('{}','{}',CURRENT_DATE,'{}');".format(Class,i,students[i],True))
    #                 elif (marked[0] == False):
    #                     psqlcur.execute("update {} set present = True where enrollment = '{}' and day = CURRENT_DATE;".format(Class,i))
    #             psqlcon.commit()
    #         except KeyError:
    #             psqlcur.execute("insert into {} values('{}','{}',CURRENT_DATE,'{}');".format(Class,i,students[i],False))
            
    #     psqlcon.commit()

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
            

# vid = Video()
# vid.capture("fml")
