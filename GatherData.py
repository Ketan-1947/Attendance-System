import cv2 as cv
import dlib
import numpy as np
import os
from tkinter import *
from tkinter import messagebox

class Video():

    def GatherData(self , name , enrollment):
        self.gather = False
        self.count = 0

        self.cap = cv.VideoCapture(0)
        
        self.face_detector = dlib.get_frontal_face_detector()
        
        FaceData = []
        EnrollmentNums = []

        Students = dict()
        
        while True:
            self.ret, self.frame = self.cap.read()
            self.frame  = cv.flip(self.frame, 1)
        
            faces = self.face_detector(self.frame)
            if len(faces) != 0:
                face = faces[0]
                x1 = face.left()
                y1 = face.top()-70
                x2 = face.right()
                y2 = face.bottom()
                faceFrame = self.frame[y1:y2,x1:x2]
                try:
                    faceFrame = cv.resize(faceFrame,(200,200))
                    grayFace = cv.cvtColor(faceFrame, cv.COLOR_BGR2GRAY)
                    grayFace = grayFace.flatten()
                except Exception as e:
                    continue
            
            if self.gather and self.count<100:
                grayFace = np.array(grayFace).flatten()
                FaceData.append(grayFace)
                EnrollmentNums.append([enrollment])
                self.count += 1
                if self.count == 100:
                    self.gather = False
                    self.count = 0
                    messagebox.showinfo("Data Gathered", "Data Gathered Successfully")
                    break


            if self.ret:
                cv.imshow('frame', self.frame)
                cv.imshow('face', faceFrame)
            
            key = cv.waitKey(1) 
            if key == ord('q'):
                self.DataWindow()
                break
            
            if key == ord('c'):
                self.gather = True
                Students[enrollment] = name


        ## adding face data to file
        
        X = np.array(FaceData)
        y = np.array(EnrollmentNums)
        
        FaceData = np.hstack([X, y])
        
        if os.path.exists('FaceData.npy'):
            old_data = np.load('FaceData.npy')
            FaceData = np.vstack([old_data, FaceData])
        np.save('FaceData.npy', FaceData)
        
        #saving student data in npy file
        if os.path.exists('Students.npy'):
            old_data = np.load('Students.npy' , allow_pickle=True).item()
            Students = {**old_data, **Students}
        np.save('Students.npy', Students)

        self.cap.release()
        cv.destroyAllWindows()
            
# Vid = Video()
# Vid.GatherData("Ketan","01318011622")