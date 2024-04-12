from tkinter import *
import mysql.connector as sql
import FaceDetect
import GatherData

#creating instance of FaceDetect class
FaceDetectInstance = FaceDetect
GatherDataInstance = GatherData.Video()

#setting up connection

class App():
    def MainWindow(self):
        #setting up main screen
        MainScreen = Tk()
        MainScreen.geometry("500x500")
        MainScreen.resizable(0,0)
        MainScreen.title("Attendance System")
        
        canvas = Canvas(MainScreen , background="blue")
        canvas.place(x=0 , y=0, width=500 , height=600)

        #creating buttons
        CaptureButton = Button(MainScreen , text="Capture" ,command = lambda: (self.CaptureWindow()))
        DataButton = Button(MainScreen , text="Add Students", command=lambda:(self.DataWindow() , MainScreen.destroy()))
        AddClassButton = Button(MainScreen , text="Add Class", command=lambda: (self.AddClassWindow() , MainScreen.destroy()))

        #placing buttons
        CaptureButton.place(x=160, y=100 , height=50 , width=200)
        DataButton.place(x=160, y=250 , height=50 , width=200)
        AddClassButton.place(x=160, y=400 , height=50 , width=200)

    def CaptureWindow(self):
        #setting up capture screen
        CaptureScreen = Tk()
        CaptureScreen.geometry("500x500")
        CaptureScreen.resizable(0,0)
        CaptureScreen.title("Capture")
        
        canvas = Canvas(CaptureScreen , background="red")
        canvas.place(x=0 , y=0, width=500 , height=600)

        #creating buttons
        CaptureButton = Button(CaptureScreen , text="Capture" , command=lambda:(FaceDetectInstance.Video.GetClass(),CaptureScreen.destroy()))
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

    def AddClassWindow(self):
        #setting up Add Class screen
        ClassScreen = Tk()
        ClassScreen.geometry("900x700")

        #adding buttons
        BackButton = Button(ClassScreen , text="<-" , command=lambda: (self.MainWindow(),ClassScreen.destroy()))

        #placing buttons
        BackButton.place(x=10, y=10 , height=30 , width=40)

        ## This function will have multiple lables




#vid = FaceDetect.video.capture()
App = App()
App.MainWindow()
mainloop()