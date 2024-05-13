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
        self.TakeAttendanceButton = Button(self.MainScreen , text="TAKE\nATTENDANCE" 
                                           ,command = lambda: (self.GetClass()) 
                                           , bg = "#FFFFFF"  
                                           , font=("Arial", 12 , "bold")
                                           , borderwidth=0)
        
        self.DataButton = Button(self.MainScreen , text="ADD\nSTUDENTS"
                                 , command=lambda:(self.DataWindow()) 
                                 , bg = "#FFFFFF"
                                 , font=("Arial", 12 , "bold")
                                 , borderwidth=0)
        
        self.AddClassButton = Button(self.MainScreen , text="ADD\nCLASS"
                                     , command=lambda: (self.AddClassWindow() ) 
                                     , bg = "#FFFFFF"
                                     , font=("Arial", 12 , "bold")
                                     , borderwidth=0)
        
        self.SeeAttendanceButton = Button(self.MainScreen , text="SEE\nATTENDANCE"
                                          , command=lambda: (self.SeeAttendance() ) 
                                          , bg = "#FFFFFF"
                                          , font=("Arial", 12 , "bold")
                                          , borderwidth=0)

        #placing buttons
        self.TakeAttendanceButton.place(x=60, y=310 , height=30 , width=128)
        self.DataButton.place(x=308, y=304 , height=35 , width=135)
        self.AddClassButton.place(x=60, y=510 , height=30 , width=128)
        self.SeeAttendanceButton.place(x=306, y=501 , height=36 , width=140)
    
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

        NameEntry = Entry(screen , bg="#CBCBCB" , borderwidth=1 ,font=("Arial", 14 , "bold") , border=0)
        EnrollmentEntry = Entry(screen , bg="#CBCBCB" , borderwidth=1 , font=("Arial", 14 , "bold") , border=0)

        NameEntry.place(x=311 , y=363 , width=150 , height=60) 
        EnrollmentEntry.place(x=60 , y=370 , width=160 , height=57)

        #creating buttons
        backButton = Button(screen , text="<-" , command=lambda: (self.destruction(screen)) , bg="#ffffff" , activebackground="#ffffff" , fg="#524646" , font=("Arial", 12 , "bold") , borderwidth=0)
        AddButton = Button(screen , text="ADD" ,font= ("Arial" , 17, "bold"),command=lambda: (GatherDataInstance.GatherData(NameEntry.get(), EnrollmentEntry.get() ), screen.destroy()) , fg = 'white', bg = "#76BB7C" , activebackground="#C9D4E5" , borderwidth=0)

        #placing buttons
        backButton.place(x=5 , y=5 , width=25 , height=20)
        AddButton.place(x=166, y=497 , height=47 , width=205) 

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
        classes = [x[0] for x in classes if x[0] != "student_data"]


        #creating menu
        
        ClassOptions=StringVar(screen )
        ClassOptions.set("SELECT CLASS")
        Class=OptionMenu(screen,ClassOptions,*classes)
        Class.place(x=315,y=330,height=70,width=170)

        Class.config(
            bg="#CBCBCB",  # background color
            fg="white",  # text color
            font=("Arial", 11 , "bold"),  # font and font size
            bd = -1,
            activebackground="#CBCBCB",  # background color when clicked
            highlightbackground="#CBCBCB",  # background color when focused
        )


        button = Button(screen , text="Submit" , command=lambda: (FaceDetectInstance.capture(ClassOptions.get())) , bg="#41545B" , activebackground="#dff5f6" , fg="white" , font=("Arial", 12 , "bold") , borderwidth=0)
        button.place(x=194 , y=470 , width=145 , height=88)

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
        entry = Entry(ClassScreen , borderwidth=0 , font=("Arial", 14 , "bold") , bg="#41545B" , border=0)

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
        AddButoon = Button(ClassScreen , text="ADD" , command = lambda:(query()) , borderwidth=0 , bg="#BF977B" , activebackground="#c9d4e5" , fg="white" , font=("Arial", 12 , "bold") )
        #placing buttons

        AddButoon.place(x=185, y=490 , height=65 , width=130)
        entry.place(x=135 , y = 345 , height = 60 , width = 230)
        backButton.place(x=5 , y=5 , width=25 , height=20)
        ## This function will have multiple lables

    def SeeAttendance(self):
        self.MainScreen.destroy()

        screen = Tk()
        screen.geometry("500x600")
        screen.resizable(0,0)
        screen.title("Attendance")

        canva= Canvas(screen)
        canva.place(x=0,y=0,width=800,height=600)
        screen.img= ImageTk.PhotoImage(Image.open("images\\seeattendancebg.png"))
        canva.create_image(0,0,anchor=NW,image=screen.img)

        enrollment = Entry(screen , bg = "white" , borderwidth=1 , font=("Arial", 14 , "bold") ,border=0)
        enrollment.place(x=153 , y=193 , width=210 , height=53)

        psqlcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
        classes = psqlcur.fetchall()
        classes = [x[0] for x in classes]

        #creating menu
        
        ClassOptions=StringVar(screen)
        ClassOptions.set("select Class")
        menu=OptionMenu(screen,ClassOptions,*classes)
        menu.place(x=140,y=280,height=60,width=225)

        menu.config(
            bg="#F7D797",  # background color
            fg="black",  # text color
            font=("Arial", 14 , "bold"),  # font and font size
            borderwidth=1,
            activebackground="#c9d4e5",  # background color when clicked
        )

        backButton = Button(screen , text="<-" ,
                            command=lambda: (self.destruction(screen)) ,
                            bg="#ffffff" , activebackground="#ffffff" ,
                            fg="#524646" , font=("Arial", 12 , "bold") ,
                            borderwidth=0)
        
        backButton.place(x=5 , y=5 , width=25 , height=20)

        SubmitButton = Button(screen , text="Submit" , command=lambda: (self.ShowAttendance(enrollment.get(),ClassOptions.get() ,screen)) , bg="#BF977B" , activebackground="#c9d4e5" , fg='white' , font=("Arial", 12 , "bold") , borderwidth=0)
        SubmitButton.place(x=94 , y=510 , width=120 , height=78)

        GetTotalAttendance = Button(screen , text = "GENERATE\nCSV" , command = lambda: self.GetTotalAttendance(ClassOptions.get()), bg="#BF977B" , activebackground="#c9d4e5" , fg='white' , font=("Arial", 9 , "bold") , borderwidth=0)
        GetTotalAttendance.place(x=316 , y=510, width=120 , height=78)

    def ShowAttendance(self,enrollment,Class ,screen):
        try:
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}' and present = 't';".format(Class,enrollment))
            present = psqlcur.fetchall()[0][0]
            psqlcur.execute("SELECT COUNT(DISTINCT day) FROM {};".format(Class,enrollment))
            total = psqlcur.fetchall()[0][0]
        except Exception as e:
            print(e)
            psqlcur.execute("ROLLBACK")
            psqlcon.commit()
            messagebox.showerror("Error","Error in Values")
            return
        if total != 0:
            percentage = round((present/total)*100,2)
        else:
            percentage = 0

        NameLabel = Label(screen , text="Name: {}".format(np.load("Students.npy" , allow_pickle=True).item()[enrollment]) , bg="#F7D797" , font=("Arial", 14 , "bold") , fg='white')
        AttendancePercentage = Label(screen , text="Attendance: {}".format(percentage) ,bg="#F7D797" , font=("Arial", 14 , "bold"), fg='white')
        ClassesAttended = Label(screen , text="Classes Attended: {}".format(present) , bg="#F7D797" , font=("Arial", 12 , "bold"), fg='white')
        TotalClasses = Label(screen , text="Total Classes: {}".format(total) , bg="#F7D797" , font=("Arial", 12 , "bold"), fg='white')

        NameLabel.place(x=100 , y=350 , width=170 , height=35)
        AttendancePercentage.place(x=300 , y=350 , width=170 , height=35)
        ClassesAttended.place(x=100 , y=410 , width=170 , height=35)
        TotalClasses.place(x=300 , y=410 , width=170 , height=35)

    def GetTotalAttendance(self ,Class):
        if Class == "select Class":
            messagebox.showerror("Error","Enter Class")
            return
        Students = np.load("Students.npy" , allow_pickle=True).item()
        
        enrollment = []
        name = []
        attendance = []

        psqlcur.execute("SELECT COUNT(DISTINCT day) FROM {};".format(Class))
        total = psqlcur.fetchall()[0][0]
        for i in Students:
            psqlcur.execute("SELECT COUNT(*) FROM {} WHERE enrollment = '{}' and present = 't';".format(Class,i))
            present = psqlcur.fetchall()[0][0]
            enrollment.append(i)
            name.append(Students[i])
            attendance.append(round((present/total)*100,2))
        
        data = {
            "Enrollment":enrollment,
            "Name":name,
            "Attendance":attendance
        }

        data = pd.DataFrame(data)
        data.to_csv("{}Attendance.csv".format(Class),index=False)

#vid = FaceDetect.video.capture()
App = App()
mainloop()