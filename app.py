from tkinter import *
from tkinter import messagebox
import psycopg2 as psql
import FaceDetect
import GatherData
import numpy as np
import pandas as pd

#creating instance of FaceDetect class
FaceDetectInstance = FaceDetect.Video()
GatherDataInstance = GatherData.Video()

#setting up connection
try:
    psqlcon = psql.connect(host="localhost",user="postgres",password="zp17dmtijm",database="test")

except (Exception, psql.DatabaseError) as error:
    print("Failed to connect to postgres")

#creating cursor
psqlcur = psqlcon.cursor()

class App():
    def MainWindow(self):
        #setting up main screen
        MainScreen = Tk()
        MainScreen.geometry("500x600")
        MainScreen.resizable(0,0)
        MainScreen.title("Attendance System")
        
        canvas = Canvas(MainScreen , background="blue")
        canvas.place(x=0 , y=0, width=500 , height=600)

        #creating buttons
        CaptureButton = Button(MainScreen , text="Capture" ,command = lambda: (self.CaptureWindow()))
        DataButton = Button(MainScreen , text="Add Students", command=lambda:(self.DataWindow() , MainScreen.destroy()))
        AddClassButton = Button(MainScreen , text="Add Class", command=lambda: (self.AddClassWindow() , MainScreen.destroy()))
        SeeAttendanceButton = Button(MainScreen , text="See Attendance", command=lambda: (self.SeeAttendance() , MainScreen.destroy()))

        #placing buttons
        CaptureButton.place(x=160, y=70 , height=50 , width=200)
        DataButton.place(x=160, y=200 , height=50 , width=200)
        AddClassButton.place(x=160, y=330 , height=50 , width=200)
        SeeAttendanceButton.place(x=160, y=460 , height=50 , width=200)

    def CaptureWindow(self):
        #setting up capture screen
        CaptureScreen = Tk()
        CaptureScreen.geometry("500x500")
        CaptureScreen.resizable(0,0)
        CaptureScreen.title("Capture")
        
        canvas = Canvas(CaptureScreen , background="red")
        canvas.place(x=0 , y=0, width=500 , height=600)

        #creating buttons
        CaptureButton = Button(CaptureScreen , text="Capture" , command=lambda:(FaceDetectInstance.GetClass(),CaptureScreen.destroy()))
        BackButton = Button(CaptureScreen , text="<-" , command=lambda: (self.MainWindow(),CaptureScreen.destroy()))

        #placing buttons
        CaptureButton.place(x=160, y=150 , height=50 , width=200)
        BackButton.place(x=10, y=10 , height=30 , width=40)

    def DataWindow(self):
        #setting up add data screen
        DataScreen = Tk()
        DataScreen.geometry("500x500")
        DataScreen.resizable(0,0)
        DataScreen.title("Add Data")
        
        canvas = Canvas(DataScreen , background="green")
        canvas.place(x=0 , y=0, width=500 , height=600)

        #creating buttons
        AddButton = Button(DataScreen , text="Add" , command=lambda: GatherDataInstance.GatherData())
        BackButton = Button(DataScreen , text="<-" , command=lambda: (self.MainWindow(),DataScreen.destroy()))

        #placing buttons
        AddButton.place(x=160, y=150 , height=50 , width=200)
        BackButton.place(x=10, y=10 , height=30 , width=40)

    def AddClassWindow(self ):
        #setting up Add Class screen
        ClassScreen = Tk()
        ClassScreen.geometry("900x700")

        #creating entry
        entry = Entry(ClassScreen)

        #adding buttons
        BackButton = Button(ClassScreen , text="<-" , command=lambda: (self.MainWindow(),ClassScreen.destroy()))
        AddButoon = Button(ClassScreen , text="ADD" , command = lambda:(psqlcur.execute("CREATE TABLE {}(enrollment VARCHAR(11), name VARCHAR(30) , day DATE , present BOOLEAN);".format(entry.get())) , psqlcon.commit()))
        #placing buttons
        BackButton.place(x=10, y=10 , height=30 , width=40)
        AddButoon.place(x=160, y=150 , height=50 , width=200)
        entry.place(x=160 , y = 120 , height = 50 , width = 200)
        ## This function will have multiple lables

    def SeeAttendance(self):
        screen = Tk()
        screen.geometry("700x800")
        screen.resizable(0,0)
        screen.title("Attendance")

        canvas = Canvas(screen , background="yellow")
        canvas.place(x=0 , y=0, width=700 , height=800)

        enrollment = Entry(screen)
        enrollment.place(x=160 , y=100 , width=200 , height=50)

        psqlcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
        classes = psqlcur.fetchall()
        classes = [x[0] for x in classes]

        #creating menu
        
        ClassOptions=StringVar(screen)
        ClassOptions.set("select Class")
        menu=OptionMenu(screen,ClassOptions,*classes)
        menu.place(x=70,y=200,height=50,width=200)

        SubmitButton = Button(screen , text="Submit" , command=lambda: (self.ShowAttendance(enrollment.get(),ClassOptions.get() ,screen)))
        SubmitButton.place(x=160 , y=300 , width=200 , height=50)

        GetTotalAttendance = Button(screen , text = "total attendance" , command = lambda: self.GetTotalAttendance(ClassOptions.get()))
        GetTotalAttendance.place(x=360 , y=400 , width=200 , height=50)

        BackButton = Button(screen , text="<-" , command=lambda: (self.MainWindow(),screen.destroy()))
        BackButton.place(x=10, y=10 , height=30 , width=40)

    def ShowAttendance(self,enrollment,Class ,screen):
        try:
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}' and present = 't';".format(Class,enrollment))
            present = psqlcur.fetchall()[0][0]
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}';".format(Class,enrollment))
            total = psqlcur.fetchall()[0][0]
        except Exception as e:
            messagebox.showerror("Error","Error in Values")
            return
        print("Present: {} Total: {}".format(present,total))
        percentage = (present/total)*100

        AttendancePercentage = Label(screen , text="Attendance: {}%".format(percentage))
        ClassesAttended = Label(screen , text="Classes Attended: {}".format(present))
        TotalClasses = Label(screen , text="Total Classes: {}".format(total))

        AttendancePercentage.place(x=160 , y=400 , width=200 , height=50)
        ClassesAttended.place(x=160 , y=500 , width=200 , height=50)
        TotalClasses.place(x=160 , y=600 , width=200 , height=50)

    def GetTotalAttendance(self ,Class):
        if Class == '':
            messagebox.showerror("Error","Enter Class")
            return
        Students = np.load("Students.npy" , allow_pickle=True).item()
        
        enrollment = []
        name = []
        attendance = []

        for i in Students:
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}' and present = 't';".format(Class,i))
            present = psqlcur.fetchall()[0][0]
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}';".format(Class,i))
            total = psqlcur.fetchall()[0][0]
            enrollment.append(i)
            name.append(Students[i])
            attendance.append((present/total)*100)
        
        data = {
            "Enrollment":enrollment,
            "Name":name,
            "Attendance":attendance
        }

        data = pd.DataFrame(data)
        data.to_csv("Attendance.csv")
        
        

#vid = FaceDetect.video.capture()
App = App()
App.MainWindow()
mainloop()