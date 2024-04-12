import cv2 as cv
import dlib
import numpy as np
import os

class Video():
    def GatherData(self):
        self.cap = cv.VideoCapture(0)
        
        self.face_detector = dlib.get_frontal_face_detector()
        
        FaceData = []
        names = []
        
        name=input('enter name: ')
        
        while True:
            self.ret, self.frame = self.cap.read()
            self.frame  = cv.flip(self.frame, 1)
        
            faces = self.face_detector(self.frame)
            if len(faces) != 0:
                face = faces[0]
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()
                faceFrame = self.frame[y1:y2,x1:x2]
                faceFrame = cv.resize(faceFrame,(200,200))
                grayFace = cv.cvtColor(faceFrame, cv.COLOR_BGR2GRAY)
                grayFace = grayFace.flatten()
            
            if self.ret:
                cv.imshow('frame', self.frame)
                cv.imshow('face', faceFrame)
            
            key = cv.waitKey(1) 
            if key == ord('q'):
                break
            
            if key == ord('c'):
                grayFace = np.array(grayFace).flatten()
                FaceData.append(grayFace)
                names.append([name])
        
            if key == ord('n'):
                name = input('enter name: ')
        
        
        ## adding face data to file
        
        X=np.array(names)
        y=np.array(FaceData)
        
        FaceData = np.hstack([X,y])
        
        if os.path.exists('FaceData.npy'):
            old_data = np.load('FaceData.npy')
            FaceData = np.vstack([old_data, FaceData])
        np.save('FaceData.npy', FaceData)
        
        self.cap.release()
        cv.destroyAllWindows()
            