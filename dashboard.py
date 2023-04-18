import threading
from tkinter import *
from tkinter import messagebox
import numpy as np
import pandas as pd
import serial
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

battery = 0
wind = 0
pv=0
busbarCurrent =0
busbarVoltage=0
mainCap=0


record = np.array([])

def close():
    Quit = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application')
    if Quit == 'yes':
        root.destroy()

def download():
    global record
    askdownload=messagebox.askquestion('Download data','Do you want to download the data')
    if askdownload:
        pd.DataFrame(record).to_csv('data.csv')

def help():
    Help = messagebox.showinfo('User Guide', 'Smart Meter Dashboard')

def review1():
    file='D5_TeamB.pptx'
    os.startfile(file)

def review2():
    file = 'D5_TeamB_2.pptx'
    os.startfile(file)

def resize_image(image, width, height):
    new_width = width
    new_height = height
    image = image.resize((new_width, new_height))
    return image

class Dashboard2:
    global battery,wind,pv,busbarCurrent,busbarVoltage

    def __init__(self, window):
        self.window = window
        self.window.title("Smart meter application")
        self.window.geometry("1366x800")
        self.window.resizable(0, 0)
        #  self.window.state('zoomed')
        self.window.config(background='#eff5f6')
        # self.window.config(background='black')
        # Window Icon Photo
        icon = PhotoImage(file='./electricity-icon.png')
        self.window.iconphoto(True, icon)

        # ==============================================================================
        # ================== HEADER ====================================================
        # ==============================================================================
        self.header = Frame(self.window, bg='#009df4')
        self.header.place(x=300, y=0, width=1070, height=60)

        # ==============================================================================
        # ================== SIDEBAR ===================================================
        # ==============================================================================
        self.sidebar = Frame(self.window, bg='#ffffff')
        # self.sidebar = Frame(self.window, bg='black')
        self.sidebar.place(x=0, y=0, width=300, height=800)

        # =============================================================================
        # ============= BODY ==========================================================
        # =============================================================================
        self.heading = Label(self.window, text='Dashboard', font=("", 15, "bold"), fg='#0064d3', bg='#eff5f6')
        self.heading.place(x=325, y=70)

        # body frame 1
        self.bodyFrame1 = Frame(self.window, bg='#ffffff')
        # self.bodyFrame1 = Frame(self.window, bg='black')
        self.bodyFrame1.place(x=328, y=110, width=1040, height=400)

        # wind
        self.bodyFrame2 = Frame(self.window, bg='#009aa5')
        self.bodyFrame2.place(x=328, y=545, width=310, height=220)
        self.powerImage = Image.open('./wind3.png')
        self.powerImage = resize_image(self.powerImage, 100, 100)
        self.powerImage = ImageTk.PhotoImage(self.powerImage)
        self.power = Label(self.bodyFrame2, image=self.powerImage, bg='#009aa5')  # e21f26
        self.power.image = self.powerImage
        self.power.configure(image=self.powerImage)
        # self.battery.place(x=680,y=550)
        # self.battery.pack(side=LEFT)
        self.power.place(relx=0.06, rely=0)

        self.windDisp = Text(self.bodyFrame2, bg='#009aa5', fg='white', font=('Times New Roman', 17, 'bold'), height=50,
                           bd=0)
        self.windDisp.insert(INSERT, "Wind: "+ str(wind))
        # self.text1.pack()
        self.windDisp.place(relx=0.42, rely=0.22)

        #PV
        self.pfImage = Image.open('./PV.png')
        self.pfImage = resize_image(self.pfImage, 100, 100)
        self.pfImage = ImageTk.PhotoImage(self.pfImage)
        self.pf = Label(self.bodyFrame2, image=self.pfImage, bg='#009aa5')  # e21f26
        self.pf.image = self.pfImage
        self.pf.configure(image=self.pfImage)
        # self.battery.place(x=680,y=550)
        # self.battery.pack(side=LEFT)
        self.pf.place(relx=0.05, rely=0.5)

        self.pvdisp = Text(self.bodyFrame2, bg='#009aa5', fg='white', font=('Times New Roman', 17, 'bold'), height=50,
                           bd=0)
        self.pvdisp.insert(INSERT, "PV: "+str(pv))
        # self.text1.pack()
       # self.powerc.place(relx=0.32, rely=0.65)
        self.pvdisp.place(relx=0.44, rely=0.72)


        # Battery
        self.bodyFrame3 = Frame(self.window, bg='#e21f26')
        self.bodyFrame3.place(x=670, y=545, width=310, height=220)

        # self.bodyFrame31 = Frame(self.window, bg='#e21f26')
        # self.bodyFrame31.place(x=680, y=655, width=310, height=110)
        # self.bodyFrame31 = Frame(self.bodyFrame3, bg='#e21f26')
        # self.bodyFrame31.place(relx=0,rely=0,width=310,height=110)
        #
        # self.bodyFrame32 = Frame(self.bodyFrame3, bg='#e21f26')
        # self.bodyFrame32.place(relx=0.3, rely=0.5, width=310, height=110)

        self.batteryImage = Image.open('./battery2.png')
        self.batteryImage = resize_image(self.batteryImage, 100, 100)
        self.batteryImage = ImageTk.PhotoImage(self.batteryImage)
        self.battery = Label(self.bodyFrame3, image=self.batteryImage, bg='#e21f26')#e21f26
        self.battery.image = self.batteryImage
        self.battery.configure(image=self.batteryImage)
        # self.battery.place(x=680,y=550)
        # self.battery.pack(side=LEFT)
        self.battery.place(relx=0.05, rely=0)
        # self.battery.place(relx=0.5, rely=0.25, anchor=CENTER)
        # self.batterydisp = Label(self.bodyFrame3,text='battery:', fg='white', bg='#e21f26', font=("", 15, "bold"))
        self.batterydisp = Text(self.bodyFrame3, fg='white', bg='#e21f26', font=("", 15, "bold"), bd=0)
        self.batterydisp.insert(INSERT, "Battery: " + str(battery))
        # self.batterydisp.place(relx=0.2,rely=0.2,anchor=CENTER)
        # self.batterydisp.pack(side=RIGHT)
        self.batterydisp.place(relx=0.40, rely=0.18)

        #Draw From Main
        self.renewableImage = Image.open('./grid5.png')
        self.renewableImage = resize_image(self.renewableImage, 100, 100)
        self.renewableImage = ImageTk.PhotoImage(self.renewableImage)
        self.renewable = Label(self.bodyFrame3, image=self.renewableImage, bg='#e21f26')
        self.renewable.image = self.renewableImage
        self.renewable.configure(image=self.renewableImage)
        # self.battery.place(x=680,y=550)
        # self.battery.pack(side=LEFT)
        self.renewable.place(relx=0.05, rely=0.45)

        self.maindisp = Text(self.bodyFrame3, fg='white', bg='#e21f26', font=("", 15, "bold"), bd=0)
        self.maindisp.insert(INSERT, "Main Capacity: " + str(mainCap))
        self.maindisp.place(relx=0.40, rely=0.60)

        # busbar Current
        self.bodyFrame4 = Frame(self.window, bg='#ffcb1f')
        self.bodyFrame4.place(x=1010, y=545, width=340, height=220)

        self.mainImage = Image.open('./ampere.png')
        self.mainImage = resize_image(self.mainImage, 100, 100)
        self.mainImage = ImageTk.PhotoImage(self.mainImage)
        self.busbarCurrent = Label(self.bodyFrame4, image=self.mainImage, bg='#ffcb1f')
        self.busbarCurrent.image = self.mainImage
        self.busbarCurrent.configure(image=self.mainImage)
        self.busbarCurrent.place(relx=0.05, rely=0.05)

        self.busbarCurrentdisp = Text(self.bodyFrame4, fg='white', bg='#ffcb1f', font=("", 15, "bold"), bd=0)
        self.busbarCurrentdisp.insert(INSERT, "Busbar Current: " + str(busbarCurrent))
        self.busbarCurrentdisp.place(relx=0.38, rely=0.23)

        #busbar Voltage
        self.busbarVoltageImage = Image.open('./busbarVoltage.png')
        self.busbarVoltageImage = resize_image(self.busbarVoltageImage, 100, 100)
        self.busbarVoltageImage = ImageTk.PhotoImage(self.busbarVoltageImage)
        self.busbarVoltage = Label(self.bodyFrame4, image=self.busbarVoltageImage, bg='#ffcb1f')
        self.busbarVoltage.image = self.busbarVoltageImage
        self.busbarVoltage.configure(image=self.busbarVoltageImage)
        # self.battery.place(x=680,y=550)
        # self.battery.pack(side=LEFT)
        self.busbarVoltage.place(relx=0.05, rely=0.55)

        self.busbarVoltagedisp = Text(self.bodyFrame4, fg='white', bg='#ffcb1f', font=("", 15, "bold"), bd=0)
        self.busbarVoltagedisp.insert(INSERT, "Busbar Voltage: " + str(busbarVoltage))
        self.busbarVoltagedisp.place(relx=0.38, rely=0.72)

        # ==============================================================================
        # ================== SIDEBAR ===================================================
        # ==============================================================================
        #
        # logo
        self.logoImage = Image.open('./electricity-icon.png')
        self.logoImage = resize_image(self.logoImage, 100, 100)
        self.logoImage = ImageTk.PhotoImage(self.logoImage)
        self.logo = Label(self.sidebar, bg='#ffffff')
        self.logo.image = self.logoImage
        self.logo.configure(image=self.logoImage)
        self.logo.place(x=70, y=80)

        # Name of brand/person
        self.brandName = Label(self.sidebar, text='TEAM B', bg='#ffffff', font=("", 15, "bold"))
        self.brandName.place(x=80, y=200)

        # Dashboard
        self.dashboardImage = Image.open('./chart.png')
        self.dashboardImage = resize_image(self.dashboardImage, 40, 40)
        self.dashboardImage = ImageTk.PhotoImage(self.dashboardImage)
        self.dashboard = Label(self.sidebar, image=self.dashboardImage, bg='#ffffff')
        self.dashboard.Image = self.dashboardImage
        self.dashboard.configure(image=self.dashboardImage)
        self.dashboard.place(x=55, y=310)

        self.dashboard_text = Button(self.sidebar, text="Dashboard", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground='#ffffff')
        self.dashboard_text.place(x=100, y=320)

        # Download
        self.DownloadImage = Image.open('./download.png')
        self.DownloadImage = resize_image(self.DownloadImage, 50, 50)
        self.DownloadImage = ImageTk.PhotoImage(self.DownloadImage)
        self.Download = Label(self.sidebar, bg='#ffffff')
        self.Download.image = self.DownloadImage
        self.Download.configure(image=self.DownloadImage)

        self.Download.place(x=50, y=380)

        self.Download_text = Button(self.sidebar, text="Download Data", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff', command=download)
        self.Download_text.place(x=105, y=390)

        # Help
        self.HelpImage = Image.open('./help.png')
        self.HelpImage = resize_image(self.HelpImage, 50, 50)
        self.HelpImage = ImageTk.PhotoImage(self.HelpImage)
        self.Help = Label(self.sidebar, bg='#ffffff')
        self.Help.image = self.HelpImage
        self.Help.configure(image=self.HelpImage)

        self.Help.place(x=50, y=590)

        self.Help_text = Button(self.sidebar, text="Help", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff', command=help)
        self.Help_text.place(x=105, y=600)

        # First Review
        self.firstReviewImage = Image.open('./review1.png')
        self.firstReviewImage = resize_image(self.firstReviewImage, 50, 50)
        self.firstReviewImage = ImageTk.PhotoImage(self.firstReviewImage)
        self.firstReview = Label(self.sidebar, bg='#ffffff')
        self.firstReview.image = self.firstReviewImage
        self.firstReview.configure(image=self.firstReviewImage)

        self.firstReview.place(x=50, y=450)

        self.firstReview_text = Button(self.sidebar, text="Review 1 slides", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff', command=review1)
        self.firstReview_text.place(x=105, y=460)


        # Review2
        self.secondReviewImage = Image.open('./secondreview.png')
        self.secondReviewImage = resize_image(self.secondReviewImage, 50, 50)
        self.secondReviewImage = ImageTk.PhotoImage(self.secondReviewImage)
        self.secondReview = Label(self.sidebar, bg='#ffffff')
        self.secondReview.image = self.secondReviewImage
        self.secondReview.configure(image=self.secondReviewImage)

        self.secondReview.place(x=50, y=520)

        self.secondReview_text = Button(self.sidebar, text="Review 2 slides", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff', command=review2)
        self.secondReview_text.place(x=105, y=530)

        # Exit
        self.ExitImage = Image.open('./quit.png')
        self.ExitImage = resize_image(self.ExitImage, 50, 50)
        self.ExitImage = ImageTk.PhotoImage(self.ExitImage)
        self.Exit = Label(self.sidebar, bg='#ffffff')
        self.Exit.image = self.ExitImage
        self.Exit.configure(image=self.ExitImage)

        self.Exit.place(x=50, y=660)

        self.Exit_text = Button(self.sidebar, text="Exit", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff', command=close)
        self.Exit_text.place(x=105, y=670)




        # =============================================================================
        # ============= BODY ==========================================================
        # =============================================================================

        # Graph
        self.graph_image = ImageTk.PhotoImage(file='images/graph.png')
        self.graph = Label(self.bodyFrame1, image=self.graph_image, bg='#ffffff')
        self.graph.place(x=40, y=70)
        #
        # self.text1 = Text(self.bodyFrame2, bg='#009aa5', fg='white', font=('Times New Roman', 17, 'bold'), height=50,bd=0)
        # self.text1.insert(INSERT, "Power Consumption: 1.6W \n\nPower Factor: 0.64")
        # #self.text1.pack()
        # self.text1.place(relx=0.05,rely=0.3)


root = Tk()
dashboard = Dashboard2(root)

# initialise serial communication
# ser = serial.Serial(port='COM8', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
#                   bytesize=serial.EIGHTBITS,
#                   timeout=1)  # ensure non-blocking) #Change the COM port to whichever port your arduino is in
# ser.reset_input_buffer()

start = False


# def plot_data():
#     #print("ok")
#     global record,start
#     if(start == True):
#         line=ser.readline()
#         string=line.decode()
#         num = int(string)
#         print(string)
#         if(len(record)<24):
#             record=np.append(record,num)
#
#         lines.set_xdata(np.arange(0,len(record)))
#         lines.set_ydata(record)
#         canvas.draw()
#         #root.update()
#         print("ok")
#
#     root.after(1,plot_data)



#
def plot_start():
    global start
    start = True
    ser.reset_input_buffer()


def plot_stop():
    global start
    start = False


def plot_graph():
    # lines.set_xdata(np.arange(0, len(record)))
    # lines.set_ydata(record)
    ax.plot(np.arange(0, len(record)), record)
    canvas.draw()
    root.after(1, plot_graph)


def read_data():
    global record, battery,wind,pv,busbarCurrent,busbarVoltage,mainCap
    while True:
        line = ser.readline()
        if line:
            string = line.decode()
            #print("Opcode is " + string[0])
            try:
                num = int(string[1:-1])
                print("Opcode is " + string[0] +  "  "+ str(num))
                #print(num)

                # if opcode is 0 means power extra or deficit
                if string[0] == '0':
                    #if (len(record) < 24):
                        record = np.append(record, num)
                # if opcode is 1 means battery
                elif string[0] == '1':
                    battery = num
                    print(battery)
                    dashboard.batterydisp.delete(1.0, END)
                    dashboard.batterydisp.insert(INSERT, "Battery: " + str(battery))
                #   root.update()

                # if opcode is 2 means wind capacity
                elif string[0] == '2':
                    wind = num
                    dashboard.windDisp.delete(1.0, END)
                    dashboard.windDisp.insert(INSERT, "Wind: " + str(wind))

                    # if opcode is 3 means PV capacity
                elif string[0] == '3':
                    pv = num
                    dashboard.pvdisp.delete(1.0, END)
                    dashboard.pvdisp.insert(INSERT, "PV: " + str(pv))

                    # if opcode is 4 means busbarVoltage
                elif string[0] == '4':
                    busbarVoltage = num
                    dashboard.busbarVoltagedisp.delete(1.0, END)
                    dashboard.busbarVoltagedisp.insert(INSERT, "Busbar Voltage: " + str(busbarVoltage))

                # if opcode is 5 means busbarCurrent
                elif string[0]=='5':
                    busbarCurrent = (((num/1024)*3.3)*6.4272 - 11.2)
                    dashboard.busbarCurrentdisp.delete(1.0, END)
                    dashboard.busbarCurrentdisp.insert(INSERT, "Busbar Current: " + str(busbarCurrent))
                    print(busbarCurrent)

                # if opcode is invalid do nothing
                else:
                    pass
            except:
                print(" hello")


fig = Figure()
ax = fig.add_subplot(111)
ax.set_title("Energy Consumption vs Time")
#ax.set_xlabel("Time Interval")
ax.set_ylabel("Energy Consumption")
lines = ax.plot([], [])[0]
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=350, y=120, width=1000, height=330)
canvas.draw()

img2 = Image.open('./start2.png')
img2 = img2.resize((90, 90))
img2 = ImageTk.PhotoImage(img2)

btnStart = Button(
    root,
    width=300,
    height=50,
    image=img2,
    relief=FLAT,
    border=0,
    bg='white',
    command=plot_graph
)

btnStart.img = img2
btnStart.pack()
btnStart.place(x=680, y=450)

# start_btn=Button(root,text="start",command= plot_graph)
# start_btn.place(x=800,y=470)
# stop_btn=Button(root,text="stop",command=plot_stop)
# stop_btn.place(x=900,y=470)

t1 = threading.Thread(target=read_data)
t1.start()

# root.after(1,plot_data)
root.mainloop()

# if __name__ == '__main__':
#     wind()
