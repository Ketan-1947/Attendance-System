#import modules
from dlib import get_frontal_face_detector
import cv2 as cv
import numpy as np
from tkinter import *
from sklearn.neighbors import KNeighborsClassifier
import psycopg2 as psql
import json

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
        self.students = np.load("Students.npy",allow_pickle=True).item()
        self.face = self.FaceData[: , :-1].astype(int)
        self.enrollment = self.FaceData[: , -1]
        self.model = KNeighborsClassifier()
        self.model.fit(self.face ,self.enrollment)
        self.presentStudents = dict()
        self.counter = 1
        self.presentStudents = dict()
        
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
                self.show_student_presence(Class)
                break
            
            if key == ord('c'):
                self.PredictFaces(frame);
        

    def PredictFaces(self,frame):
        detector = get_frontal_face_detector()
        faces = detector(frame)
        for face in faces:
            if face is None:
                continue
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
                cv.putText(frame,self.students[enrollment[0]],(x1,y1),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                self.presentStudents[enrollment[0]] = True
                
        while True:
            cv.imshow("frame",frame)
            cv.putText(frame,"Press 'c' to close",(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            key = cv.waitKey(100)

            if key == ord('c'):
                break

    def add_student(self):
        student_name = entry.get()
        if student_name in self.students:
            self.presentStudents[student_name] = True
            self.update_display()

    def remove_student(self):
        student_name = entry.get()
        if student_name in self.presentStudents:
            self.presentStudents[student_name] = False
            self.update_display()
        else:
            print("Student not found")

    def update_display(self):
        # Clear the inner frame
        for widget in inner_frame.winfo_children():
            widget.destroy()

        # Iterate through all students
        try:
            for student in self.students:
                label_text = self.students[student] + ": "
                if student in self.presentStudents:
                    if self.presentStudents[student]:
                        label_text += "Present"
                    else:
                        label_text += "Absent"
                else:
                    label_text += "Absent"

                # Create a label for each student
                label =  Label(inner_frame, text=label_text)
                label.pack(anchor= W)

        except Exception as e:
            print(2)
    def show_student_presence(self,Class):
        
        print(self.students , self.presentStudents)
        # Create a Tkinter window
        window =  Tk()
        window.title("Student Presence")

        # Set window size to mobile phone ratio with height 800px
        window.geometry("400x500")

        # Create a frame to contain the labels
        frame =  Frame(window)
        frame.pack(fill= BOTH, expand=True)

        # Create a canvas for the frame
        canvas =  Canvas(frame)
        canvas.pack(side= LEFT, fill= BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar =  Scrollbar(frame, orient= VERTICAL, command=canvas.yview)
        scrollbar.pack(side= RIGHT, fill= Y)

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create another frame to contain the labels inside the canvas
        global inner_frame
        inner_frame =  Frame(canvas)

        # Add the inner frame to the canvas
        canvas.create_window((0, 0), window=inner_frame, anchor= NW)

        # Function to update canvas scrolling region
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_frame_configure)

        #labeling all the students 
        for student in self.students:
            label_text = self.students[student] + ": "
            if student in self.presentStudents:
                if self.presentStudents[student]:
                    label_text += "Present"
                else:
                    label_text += "Absent"
            else:
                label_text += "Absent"

            # Create a label for each student
            label =  Label(inner_frame, text=label_text)
            label.pack(anchor= W)

        # Entry field for adding or removing names
        global entry
        entry =  Entry(window)
        entry.place(x=250,y=50)

        # Buttons for adding and removing names
        add_button =  Button(window, text="Mark P", command=lambda: self.add_student())
        add_button.place(x=250,y=100)
        remove_button =  Button(window, text="Mark A", command=lambda: self.remove_student())
        remove_button.place(x=250,y=150)
        done_button =  Button(window, text="Done", command=lambda: self.TakeAttendance(Class))  
        done_button.place(x=250,y=200)
        # Run the Tkinter event loop
        window.mainloop()

    def TakeAttendance(self,Class):
        for i in self.students:
            psqlcur.execute("select present from {} where day = CURRENT_DATE and enrollment = '{}';".format(Class,i))
            marked = psqlcur.fetchone()
            if marked == None:
                try:
                   if self.presentStudents[i]:
                       psqlcur.execute("insert into {} values('{}','{}',CURRENT_DATE,'{}');".format(Class,i,self.students[i],True))
                except Exception as e:
                    psqlcur.execute("insert into {} values('{}','{}',CURRENT_DATE,'{}');".format(Class,i,self.students[i],False))
            elif marked[0] == False:
                try:                                        
                    if self.presentStudents[i]:
                        psqlcur.execute("update {} set present = True where enrollment = '{}' and day = CURRENT_DATE;".format(Class,i)) 
                except Exception as e:
                    continue

        psqlcon.commit()
            

# vid = Video()
# vid.capture("fml")
