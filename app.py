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

        self.canva= Canvas(self.MainScreen, width= 1200, height= 800)
        self.canva.pack()
        self.img= ImageTk.PhotoImage(Image.open("images\\mainbg.png"))
        self.canva.create_image(0,0,anchor=NW,image=self.img) 

        #creating buttons
        self.TakeAttendanceButton = Button(self.MainScreen , text="TAKE\nATTENDANCE" ,command = lambda: (self.GetClass()) , bg = "#FFFFFF" , activebackground="#f0f0ff" , fg="#524646" , font=("Arial", 12 , "bold"))
        self.DataButton = Button(self.MainScreen , text="ADD\nSTUDENTS", command=lambda:(self.DataWindow()) , bg = "#FFFFFF", activebackground="#ffeef8" , fg="#524646", font=("Arial", 12 , "bold"))
        self.AddClassButton = Button(self.MainScreen , text="ADD\nCLASS", command=lambda: (self.AddClassWindow() ) , bg = "#FFFFFF", activebackground="#ffeef8" , fg="#524646", font=("Arial", 12 , "bold"))
        self.SeeAttendanceButton = Button(self.MainScreen , text="SEE\nATTENDANCE", command=lambda: (self.SeeAttendance() ) , bg = "#FFFFFF", activebackground="#f0f0ff" , fg="#524646", font=("Arial", 12 , "bold") )

        #placing buttons
        self.TakeAttendanceButton.place(x=77, y=150 , height=136 , width=164)
        self.DataButton.place(x=288, y=150 , height=136 , width=164)
        self.AddClassButton.place(x=77, y=339 , height=136 , width=164)
        self.SeeAttendanceButton.place(x=288, y=340 , height=136 , width=164)
    
    def destruction(self , screen):
        screen.destroy()
        self.__init__()

    def DataWindow(self):
        #setting up add data screen
        self.MainScreen.destroy()

        screen = Tk()
        screen.geometry("500x600")
        screen.resizable(0,0)
        screen.title("Add Data")
        
        canva= Canvas(screen)
        canva.place(x=0,y=0,width=500,height=600)
        screen.img= ImageTk.PhotoImage(Image.open("images\\addstudentbg.png"))
        canva.create_image(0,0,anchor=NW,image=screen.img)

        nameLabel = Label(screen , text="Name" , font=("Arial", 14 , "bold") , bg="#c9d4e5")
        EnrollmentLabel = Label(screen , text="Enrollment" , font=("Arial", 14 , "bold") , bg="#c9d4e5")

        nameLabel.place(x=40 , y=294 , width=55 , height=20)
        EnrollmentLabel.place(x=284 , y=294 , width=100 , height=20)

        NameEntry = Entry(screen , bg="#C9D4E5" , borderwidth=1 ,font=("Arial", 14 , "bold") , border=0)
        EnrollmentEntry = Entry(screen , bg="#C9D4E5" , borderwidth=1 , font=("Arial", 14 , "bold") , border=0)

        NameEntry.place(x=40 , y=317 , width=178 , height=54) 
        EnrollmentEntry.place(x=284 , y=317 , width=178 , height=54)

        #creating buttons
        backButton = Button(screen , text="<-" , command=lambda: (self.destruction(screen)) , bg="#ffffff" , activebackground="#ffffff" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        AddButton = Button(screen , text="ADD" ,font= ("Arial" , 17, "bold"),command=lambda: (GatherDataInstance.GatherData(NameEntry.get(), EnrollmentEntry.get() ), screen.destroy()) , bg = "#C9D4E5" , activebackground="#C9D4E5" , borderwidth=0)

        #placing buttons
        backButton.place(x=5 , y=5 , width=25 , height=20)
        AddButton.place(x=202, y=440 , height=103 , width=91) 

    def GetClass(self):
        self.MainScreen.destroy()
        screen = Tk()
        screen.geometry("500x600")
        screen.resizable(0,0)
        screen.title("Class")

        canva= Canvas(screen)
        canva.place(x=0,y=0,width=500,height=600)
        screen.img= ImageTk.PhotoImage(Image.open("images\\takeattendancebg.png"))
        canva.create_image(0,0,anchor=NW,image=screen.img)

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

        backButton = Button(screen , text="<-" , command=lambda: (self.destruction(screen)) , bg="#ffffff" , activebackground="#ffffff" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        backButton.place(x=5 , y=5 , width=25 , height=20)

    def AddClassWindow(self ):
        
        self.MainScreen.destroy()

        #setting up Add Class screen
        ClassScreen = Tk()
        ClassScreen.geometry("500x600")
        ClassScreen.resizable(0,0)
        canva= Canvas(ClassScreen)
        canva.place(x=0,y=0,width=500,height=600)
        ClassScreen.img= ImageTk.PhotoImage(Image.open("images\\addclassbg.png"))
        canva.create_image(0,0,anchor=NW,image=ClassScreen.img)

        #creating entry
        entry = Entry(ClassScreen , borderwidth=0 , font=("Arial", 14 , "bold") , bg="#c9d4e5" , border=0)

        #adding buttons
        def query():
            try:
                psqlcur.execute("CREATE TABLE {}(enrollment VARCHAR(11), name VARCHAR(30) , day DATE , present BOOLEAN);".format(entry.get()))
                psqlcon.commit()
                messagebox.showinfo("Success","Class Added")
            except Exception as e:
                psqlcur.execute("ROLLBACK")
                psqlcon.commit()
                messagebox.showerror("Error","Error in Values")
                return
        backButton = Button(ClassScreen , text="<-" , command=lambda: (self.destruction(ClassScreen)) , bg="#ffffff" , activebackground="#ffffff" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        AddButoon = Button(ClassScreen , text="ADD" , command = lambda:(query()) , borderwidth=0 , bg="#c9d4e5" , activebackground="#c9d4e5" , fg="#524646" , font=("Arial", 12 , "bold") )
        #placing buttons

        AddButoon.place(x=201, y=440 , height=100 , width=98)
        entry.place(x=153 , y = 258 , height = 96 , width = 200)
        backButton.place(x=5 , y=5 , width=25 , height=20)
        ## This function will have multiple lables

    def SeeAttendance(self):
        self.MainScreen.destroy()

        screen = Tk()
        screen.geometry("800x600")
        screen.resizable(0,0)
        screen.title("Attendance")

        canva= Canvas(screen)
        canva.place(x=0,y=0,width=800,height=600)
        screen.img= ImageTk.PhotoImage(Image.open("images\\seeattendancebg.png"))
        canva.create_image(0,0,anchor=NW,image=screen.img)

        enrollment = Entry(screen , bg = "#c9d4e5" , borderwidth=1 , font=("Arial", 14 , "bold"))
        enrollment.place(x=45 , y=270 , width=200 , height=50)

        psqlcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
        classes = psqlcur.fetchall()
        classes = [x[0] for x in classes]

        #creating menu
        
        ClassOptions=StringVar(screen)
        ClassOptions.set("select Class")
        menu=OptionMenu(screen,ClassOptions,*classes)
        menu.place(x=45,y=340,height=50,width=200)

        menu.config(
            bg="#c9d4e5",  # background color
            fg="black",  # text color
            font=("Arial", 14 , "bold"),  # font and font size
            borderwidth=1,
            activebackground="#c9d4e5",  # background color when clicked
        )

        ClassOptions2=StringVar(screen)
        ClassOptions2.set("select Class")
        menu2=OptionMenu(screen,ClassOptions2,*classes)
        menu2.place(x=450,y=225,height=50,width=310)

        menu2.config(
            bg="#c9d4e5",  # background color
            fg="black",  # text color
            font=("Arial", 14 , "bold"),  # font and font size
            borderwidth=1,
            activebackground="#c9d4e5",  # background color when clicked
        )

        backButton = Button(screen , text="<-" , command=lambda: (self.destruction(screen)) , bg="#ffffff" , activebackground="#ffffff" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        backButton.place(x=5 , y=5 , width=25 , height=20)

        SubmitButton = Button(screen , text="Submit" , command=lambda: (self.ShowAttendance(enrollment.get(),ClassOptions.get() ,screen)) , bg="#c9d4e5" , activebackground="#c9d4e5" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        SubmitButton.place(x=90 , y=490 , width=200 , height=50)

        GetTotalAttendance = Button(screen , text = "GENERATE TOTAL" , command = lambda: self.GetTotalAttendance(ClassOptions2.get()), bg="#c9d4e5" , activebackground="#c9d4e5" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        GetTotalAttendance.place(x=450 , y=290, width=310 , height=250)

    def ShowAttendance(self,enrollment,Class ,screen):
        try:
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}' and present = 't';".format(Class,enrollment))
            present = psqlcur.fetchall()[0][0]
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}';".format(Class,enrollment))
            total = psqlcur.fetchall()[0][0]
        except Exception as e:
            messagebox.showerror("Error","Error in Values")
            return
        percentage = round((present/total)*100,2)

        NameLabel = Label(screen , text="Name: {}".format(np.load("Students.npy" , allow_pickle=True).item()[enrollment]) , bg="#c9d4e5" , font=("Arial", 10 , "bold"))
        AttendancePercentage = Label(screen , text="Attendance: {}".format(percentage) ,bg="#c9d4e5" , font=("Arial", 10 , "bold"))
        ClassesAttended = Label(screen , text="Classes Attended: {}".format(present) , bg="#c9d4e5" , font=("Arial", 10 , "bold"))
        TotalClasses = Label(screen , text="Total Classes: {}".format(total) , bg="#c9d4e5" , font=("Arial", 10 , "bold"))

        NameLabel.place(x=45 , y=410 , width=145 , height=35)
        AttendancePercentage.place(x=200 , y=410 , width=145 , height=35)
        ClassesAttended.place(x=45 , y=460 , width=145 , height=35)
        TotalClasses.place(x=200 , y=460 , width=145 , height=35)

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