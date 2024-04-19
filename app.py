from tkinter import *
from tkinter import messagebox
import psycopg2 as psql
import FaceDetect
import GatherData
import numpy as np
import pandas as pd
from PIL import Image, ImageTk

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
    def __init__(self):
        #setting up main screen
        self.MainScreen = Tk()
        self.MainScreen.geometry("500x600")
        self.MainScreen.resizable(0,0)
        self.MainScreen.title("Attendance System")
        
        self.canva= Canvas(self.MainScreen)
        self.canva.place(x=0,y=0,width=500,height=600)
        self.img= ImageTk.PhotoImage(Image.open("images\\mainbg.png"))
        self.canva.create_image(0,0,anchor=NW,image=self.img)

        #creating buttons
        self.TakeAttendanceButton = Button(self.MainScreen , text="TAKE\nATTENDANCE" ,command = lambda: (self.GetClass()) , bg = "#FFFFFF" , activebackground="#f0f0ff" , fg="#524646" , font=("Arial", 12 , "bold"))
        self.DataButton = Button(self.MainScreen , text="ADD\nSTUDENTS", command=lambda:(GatherDataInstance.DataWindow()) , bg = "#FFFFFF", activebackground="#ffeef8" , fg="#524646", font=("Arial", 12 , "bold"))
        self.AddClassButton = Button(self.MainScreen , text="ADD\nCLASS", command=lambda: (self.AddClassWindow() ) , bg = "#FFFFFF", activebackground="#ffeef8" , fg="#524646", font=("Arial", 12 , "bold"))
        self.SeeAttendanceButton = Button(self.MainScreen , text="SEE\nATTENDANCE", command=lambda: (self.SeeAttendance() ) , bg = "#FFFFFF", activebackground="#f0f0ff" , fg="#524646", font=("Arial", 12 , "bold") )

        #placing buttons
        self.TakeAttendanceButton.place(x=77, y=150 , height=136 , width=164)
        self.DataButton.place(x=288, y=150 , height=136 , width=164)
        self.AddClassButton.place(x=77, y=339 , height=136 , width=164)
        self.SeeAttendanceButton.place(x=288, y=340 , height=136 , width=164)

    def GetClass(self):
        self.MainScreen.withdraw()
        screen = Toplevel()
        screen.geometry("500x600")
        screen.resizable(0,0)
        screen.title("Class")

        try:
            self.img = PhotoImage(file="images\\takeattendancebg.png")
            label_bgImage = Label(screen,image=self.img)
            label_bgImage.place(x=0, y=0)
        except Exception as e:
            print(e)

        psqlcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
        classes = psqlcur.fetchall()
        classes = [x[0] for x in classes]

        #creating menu
        
        ClassOptions=StringVar(screen )
        ClassOptions.set("SELECT CLASS")
        Class=OptionMenu(screen,ClassOptions,*classes)
        Class.place(x=104,y=253,height=97,width=326)

        Class.config(
            bg="#ffffff",  # background color
            fg="black",  # text color
            font=("Arial", 14 , "bold"),  # font and font size
            bd = -1,
            activebackground="#ffffff",  # background color when clicked
            highlightbackground="#ffffff",  # background color when focused
        )


        button = Button(screen , text="Submit" , command=lambda: (FaceDetectInstance.capture(ClassOptions.get())) , bg="#dff5f6" , activebackground="#dff5f6" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        button.place(x=197 , y=418 , width=118 , height=120)


    def AddClassWindow(self ):
        #setting up Add Class screen
        ClassScreen = Tk()
        ClassScreen.geometry("900x700")

        #creating entry
        entry = Entry(ClassScreen)

        #adding buttons

        AddButoon = Button(ClassScreen , text="ADD" , command = lambda:(psqlcur.execute("CREATE TABLE {}(enrollment VARCHAR(11), name VARCHAR(30) , day DATE , present BOOLEAN);".format(entry.get())) , psqlcon.commit()))
        #placing buttons

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
mainloop()