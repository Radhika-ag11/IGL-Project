#Importing Libraries
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import nu`  mpy as np
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

#DB connectivity
mydb = mysql.connector.connect(host="localhost", user="root", password="xxxx", database='dbstorage')

mycursor = mydb.cursor()
mycursor.execute("select * from dbinformation;")
myresult = mycursor.fetchall()
df = pd.DataFrame(myresult, columns = ['Time','Table_SpaceName','UsedSpace_in_MB','FreeSpace_in_MB','TotalSpace_in_MB','Percentage_Free'])
tail14_df=df.tail(14)

SYSTEMcur = mydb.cursor()
SYSTEMcur.execute("select * from dbinformation where Table_SpaceName='SYSTEM';")
SYSTEMresult = SYSTEMcur.fetchall()
SYSTEMdf = pd.DataFrame(SYSTEMresult, columns = ['Time','Table_SpaceName','UsedSpace_in_MB','FreeSpace_in_MB','TotalSpace_in_MB','Percentage_Free'])

UNDOTBS1cur = mydb.cursor()
UNDOTBS1cur.execute("select * from dbinformation where Table_SpaceName='UNDOTBS1';")
UNDOTBS1result = UNDOTBS1cur.fetchall()
UNDOTBS1df = pd.DataFrame(UNDOTBS1result, columns = ['Time','Table_SpaceName','UsedSpace_in_MB','FreeSpace_in_MB','TotalSpace_in_MB','Percentage_Free'])

SYSAUXcur = mydb.cursor()
SYSAUXcur.execute("select * from dbinformation where Table_SpaceName='SYSAUX';")
SYSAUXresult = SYSAUXcur.fetchall()
SYSAUXdf = pd.DataFrame(SYSAUXresult, columns = ['Time','Table_SpaceName','UsedSpace_in_MB','FreeSpace_in_MB','TotalSpace_in_MB','Percentage_Free'])

CSPRDATAcur = mydb.cursor()
CSPRDATAcur.execute("select * from dbinformation where Table_SpaceName='CSPRDATA';")
CSPRDATAresult = CSPRDATAcur.fetchall()
CSPRDATAdf = pd.DataFrame(CSPRDATAresult, columns = ['Time','Table_SpaceName','UsedSpace_in_MB','FreeSpace_in_MB','TotalSpace_in_MB','Percentage_Free'])

EXSMTcur = mydb.cursor()
EXSMTcur.execute("select * from dbinformation where Table_SpaceName='EXSMT';")
EXSMTresult = EXSMTcur.fetchall()
EXSMTdf = pd.DataFrame(EXSMTresult, columns = ['Time','Table_SpaceName','UsedSpace_in_MB','FreeSpace_in_MB','TotalSpace_in_MB','Percentage_Free'])

total_cur=mydb.cursor()
total_cur.execute("select * from total_space;")
totalResult = total_cur.fetchall()
total_df = pd.DataFrame(totalResult, columns = ['Time','TotalSpace_in_TB'])

#GUI Code
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\sambhav\DBSMS-IGL-main\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("960x540")
window.configure(bg = "#F1F4F7")

canvas = Canvas(
    window,
    bg = "#F1F4F7",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

canvas.create_rectangle(
    12.0,
    147.0,
    189.0,
    525.0,
    fill="#FCFCFC",
    outline="")

canvas.create_rectangle(
    13.0,
    9.0,
    951.0,
    139.0,
    fill="#F9F9F9",
    outline="")

canvas.create_rectangle(
    199.0,
    147.0,
    946.0,
    352.0,
    fill="#FFFFFF",
    outline="")

# prediction box:
canvas.create_rectangle(
    199.0,
    362.0,
    409.0,
    526.0,
    fill="#FCFCFC",
    outline="")

#DB Detail box:
canvas.create_rectangle(
    421.0,
    362.0,
    946.0,
    525.0,
    fill="#FCFCFC",
    outline="")

canvas.create_text(
    247.0,
    367.0,
    anchor="nw",
    text="PREDICTION",
    fill="#6F6F6F",
    font=("Inter Medium", 16 * -1)
)

canvas.create_text(
    598.0,
    369.0,
    anchor="nw",
    text="DATABASE DETAILS",
    fill="#6F6F6F",
    font=("Inter Medium", 16 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    552.0,
    73.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    150.0,
    73.0,
    image=image_image_2
)

canvas.create_text(
    53.0,
    155.0,
    anchor="nw",
    text="DATABASES",
    fill="#6F6F6F",
    font=("Inter Medium", 16 * -1)    
)

def sep_space_text(indi_size_info):
    canvas.create_rectangle(
        610.0,
        400.0,
        946.0,
        550.0,
        fill="#FCFCFC",
        outline=""
    )
    canvas.create_text(
        620.0,
        410.0,
        anchor="nw",
        text="Used Space: "+str(indi_size_info[0])+" MB",
        fill="#000000",
        font=("Inter Medium", 16 * -1)
    )    
    canvas.create_text(
        620.0,
        440.0,
        anchor="nw",
        text="Free Space: "+str(indi_size_info[1])+" MB",
        fill="#000000",
        font=("Inter Medium", 16 * -1)
    )
    canvas.create_text(
        620.0,
        470.0,
        anchor="nw",
        text="Total Space: "+str(total_df['TotalSpace_in_TB'].iloc[-1])+" MB",
        fill="#000000",
        font=("Inter Medium", 16 * -1)
    )
    canvas.create_text(
        620.0,
        500.0,
        anchor="nw",
        text="Percentage Free: "+str(indi_size_info[3])+" %",
        fill="#000000",
        font=("Inter Medium", 16 * -1)
    )

def pred_text(txt):
    canvas.create_rectangle(
    199.0,
    400.0,
    409.0,
    526.0,
    fill="#FCFCFC",
    outline=""
    )
    canvas.create_text(
    220.0,
    400.0,
    anchor="nw",
    text=txt,
    fill="#000000",
    font=("Inter Medium", 16 * -1),
    width=180
    )

fig_ovr = Figure(figsize=(8, 2))
ax_ovr = fig_ovr.add_subplot(111)

ax_ovr.plot(SYSTEMdf['Time'], SYSTEMdf['UsedSpace_in_MB'], linestyle='-', color='red', label='SYSTEM')
ax_ovr.plot(UNDOTBS1df['Time'], UNDOTBS1df['UsedSpace_in_MB'], linestyle='-', color='Green', label='UNDOTBS1')
ax_ovr.plot(SYSAUXdf['Time'], SYSAUXdf['UsedSpace_in_MB'], linestyle='-', color='Blue', label='SYSAUX')
ax_ovr.plot(CSPRDATAdf['Time'], CSPRDATAdf['UsedSpace_in_MB'], linestyle='-', color='Violet', label='CSPRDATA')
ax_ovr.plot(EXSMTdf['Time'], EXSMTdf['UsedSpace_in_MB'], linestyle='-', color='Cyan', label='EXSMT')

ax_ovr.set_ylabel('Size In MB')
ax_ovr.set_title('DB: PRDOTDB')
ax_ovr.grid(True)
ax_ovr.legend()
canvas_ovr = FigureCanvasTkAgg(fig_ovr, master=window)
canvas_ovr.draw()
canvas_ovr.get_tk_widget().place(x=200.0,y=144.0)

#Graph Functions:
def DB1():
    indi_size_info=[SYSTEMdf['UsedSpace_in_MB'].iloc[-1], SYSTEMdf['FreeSpace_in_MB'].iloc[-1], SYSTEMdf['TotalSpace_in_MB'].iloc[-1], SYSTEMdf['Percentage_Free'].iloc[-1]]
    sep_space_text(indi_size_info)
 
    figpie = Figure(figsize=(1.7, 1.6))
    axpie = figpie.add_subplot(111)
    myexplode = [0.2, 0, 0, 0,0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0, 0 ]
    axpie.pie(tail14_df['UsedSpace_in_MB'],explode = myexplode)
    canvaspie = FigureCanvasTkAgg(figpie, master=window)
    canvaspie.draw()
    canvaspie.get_tk_widget().place(x=426.0,y=361.0)

    order=(1,1,1)
    data = np.array(SYSTEMdf['UsedSpace_in_MB'])
    model=ARIMA(data, order=order)
    model_result=model.fit()
    forecast_steps = 4
    forecast=model_result.forecast(steps=forecast_steps, alpha=0.05)
    forecast_dates = pd.date_range(SYSTEMdf['Time'].iloc[-1], periods=forecast_steps+1, freq='D')[1:]
    forecast_df = pd.DataFrame({'Time': forecast_dates, 'Forecast': forecast})
    for val in forecast: 
        if np.isinf(val): 
            txt="Found an infinity value in forecast!"
        else: 
            txt="In next 4 weeks, this tablespace will reach : " + str(val)+" MB"     
    pred_text(txt)

    fig = Figure(figsize=(8, 2))
    ax = fig.add_subplot(111)
    ax.plot(SYSTEMdf['Time'], SYSTEMdf['UsedSpace_in_MB'], linestyle='-', color='Red', label='Used Space')
    ax.plot(SYSTEMdf['Time'], SYSTEMdf['FreeSpace_in_MB'], linestyle='-', color='Green', label='Free Space')
    ax.plot(forecast_df['Time'], forecast_df['Forecast'], linestyle='--',color='Black', label='Forecast')
    #ax.set_xlabel('Time')
    ax.set_ylabel('Size In MB')
    ax.set_title('Table Space Name: SYSTEM')
    ax.grid(True)
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=200.0,y=144.0)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=DB1 ,
    relief="flat"
)
button_1.place(
    x=32.0,
    y=189.0,
    width=137.0,
    height=24.0
)


def DB2():
    indi_size_info=[UNDOTBS1df['UsedSpace_in_MB'].iloc[-1], UNDOTBS1df['FreeSpace_in_MB'].iloc[-1], UNDOTBS1df['TotalSpace_in_MB'].iloc[-1], UNDOTBS1df['Percentage_Free'].iloc[-1]]
    sep_space_text(indi_size_info)
 
    figpie = Figure(figsize=(1.7, 1.6))
    axpie = figpie.add_subplot(111)
    myexplode = [0, 0.2, 0, 0,0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0, 0 ]
    axpie.pie(tail14_df['UsedSpace_in_MB'],explode = myexplode)
    canvaspie = FigureCanvasTkAgg(figpie, master=window)
    canvaspie.draw()
    canvaspie.get_tk_widget().place(x=426.0,y=361.0)

    order=(1,1,1)
    data = np.array(UNDOTBS1df['UsedSpace_in_MB'])
    model=ARIMA(data, order=order)
    model_result=model.fit()
    forecast_steps = 4
    forecast=model_result.forecast(steps=forecast_steps, alpha=0.05)
    forecast_dates = pd.date_range(UNDOTBS1df['Time'].iloc[-1], periods=forecast_steps+1, freq='D')[1:]
    forecast_df = pd.DataFrame({'Time': forecast_dates, 'Forecast': forecast})
    for val in forecast: 
        if np.isinf(val): 
            txt="Found an infinity value in forecast!" 
        else: 
            txt="In next 4 weeks, this tablespace will reach : " + str(val)+" MB"       
    pred_text(txt)

    fig = Figure(figsize=(8, 2))
    ax = fig.add_subplot(111)
    ax.plot(UNDOTBS1df['Time'], UNDOTBS1df['UsedSpace_in_MB'], linestyle='-', color='Red', label='Used Space')
    ax.plot(UNDOTBS1df['Time'], UNDOTBS1df['FreeSpace_in_MB'], linestyle='-', color='Green', label='Free Space')
    ax.plot(forecast_df['Time'], forecast_df['Forecast'], linestyle='--',color='Black', label='Forecast')
    #ax.set_xlabel('Time')
    ax.set_ylabel('Size In MB')
    ax.set_title('Table Space Name: UNDOTBS1')
    ax.grid(True)
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=200.0,y=144.0)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=DB2,
    relief="flat"
)
button_2.place(
    x=32.0,
    y=227.0,
    width=137.0,
    height=24.0
)


def DB3():
    indi_size_info=[SYSAUXdf['UsedSpace_in_MB'].iloc[-1], SYSAUXdf['FreeSpace_in_MB'].iloc[-1], SYSAUXdf['TotalSpace_in_MB'].iloc[-1], SYSAUXdf['Percentage_Free'].iloc[-1]]
    sep_space_text(indi_size_info)
 
    figpie = Figure(figsize=(1.7, 1.6))
    axpie = figpie.add_subplot(111)
    myexplode = [0, 0, 0.2, 0,0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0, 0 ]
    axpie.pie(tail14_df['UsedSpace_in_MB'],explode = myexplode)
    canvaspie = FigureCanvasTkAgg(figpie, master=window)
    canvaspie.draw()
    canvaspie.get_tk_widget().place(x=426.0,y=361.0)

    order=(1,1,1)
    data = np.array(SYSAUXdf['UsedSpace_in_MB'])
    model=ARIMA(data, order=order)
    model_result=model.fit()
    forecast_steps = 4
    forecast=model_result.forecast(steps=forecast_steps, alpha=0.05)
    forecast_dates = pd.date_range(SYSAUXdf['Time'].iloc[-1], periods=forecast_steps+1, freq='D')[1:]
    forecast_df = pd.DataFrame({'Time': forecast_dates, 'Forecast': forecast})
    for val in forecast: 
        if np.isinf(val): 
            txt="Found an infinity value in forecast!" 
        else: 
            txt="In next 4 weeks, this tablespace will reach : " + str(val)+" MB"       
    pred_text(txt)

    fig = Figure(figsize=(8, 2))
    ax = fig.add_subplot(111)
    ax.plot(SYSAUXdf['Time'], SYSAUXdf['UsedSpace_in_MB'], linestyle='-', color='Red', label='Used Space')
    ax.plot(SYSAUXdf['Time'], SYSAUXdf['FreeSpace_in_MB'], linestyle='-', color='Green', label='Free Space')
    ax.plot(forecast_df['Time'], forecast_df['Forecast'], linestyle='--',color='Black', label='Forecast')
    #ax.set_xlabel('Time')
    ax.set_ylabel('Size In MB')
    ax.set_title('Table Space Name: SYSAUX')
    ax.grid(True)
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=200.0,y=144.0)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=DB3,
    relief="flat"
)
button_3.place(
    x=32.0,
    y=267.0,
    width=137.0,
    height=24.0
)

def DB4():
    indi_size_info=[CSPRDATAdf['UsedSpace_in_MB'].iloc[-1], CSPRDATAdf['FreeSpace_in_MB'].iloc[-1], CSPRDATAdf['TotalSpace_in_MB'].iloc[-1], CSPRDATAdf['Percentage_Free'].iloc[-1]]
    sep_space_text(indi_size_info)
 
    figpie = Figure(figsize=(1.7, 1.6))
    axpie = figpie.add_subplot(111)
    myexplode = [0, 0, 0, 0.2,0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0, 0 ]
    axpie.pie(tail14_df['UsedSpace_in_MB'],explode = myexplode)
    canvaspie = FigureCanvasTkAgg(figpie, master=window)
    canvaspie.draw()
    canvaspie.get_tk_widget().place(x=426.0,y=361.0)

    order=(1,1,1)
    data = np.array(CSPRDATAdf['UsedSpace_in_MB'])
    model=ARIMA(data, order=order)
    model_result=model.fit()
    forecast_steps = 4
    forecast=model_result.forecast(steps=forecast_steps, alpha=0.05)
    forecast_dates = pd.date_range(CSPRDATAdf['Time'].iloc[-1], periods=forecast_steps+1, freq='D')[1:]
    forecast_df = pd.DataFrame({'Time': forecast_dates, 'Forecast': forecast})
    for val in forecast: 
        if np.isinf(val): 
            txt="Found an infinity value in forecast!" 
        else: 
            txt="In next 4 weeks, this tablespace will reach : " + str(val)+" MB"        
    pred_text(txt)

    fig = Figure(figsize=(8, 2))
    ax = fig.add_subplot(111)
    ax.plot(CSPRDATAdf['Time'], CSPRDATAdf['UsedSpace_in_MB'], linestyle='-', color='Red', label='Used Space')
    ax.plot(CSPRDATAdf['Time'], CSPRDATAdf['FreeSpace_in_MB'], linestyle='-', color='Green', label='Free Space')
    ax.plot(forecast_df['Time'], forecast_df['Forecast'], linestyle='--',color='Black', label='Forecast')
    #ax.set_xlabel('Time')
    ax.set_ylabel('Size In MB')
    ax.set_title('Table Space Name: CSPRDATA')
    ax.grid(True)
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=200.0,y=144.0)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=DB4,
    relief="flat"
)
button_4.place(
    x=32.0,
    y=307.0,
    width=137.0,
    height=24.0
)

def DB5():
    indi_size_info=[EXSMTdf['UsedSpace_in_MB'].iloc[-1], EXSMTdf['FreeSpace_in_MB'].iloc[-1], EXSMTdf['TotalSpace_in_MB'].iloc[-1], EXSMTdf['Percentage_Free'].iloc[-1]]
    sep_space_text(indi_size_info)
 
    figpie = Figure(figsize=(1.7, 1.6))
    axpie = figpie.add_subplot(111)
    myexplode = [0, 0, 0, 0,0.2 ,0 ,0 ,0 ,0 ,0, 0, 0, 0, 0 ]
    axpie.pie(tail14_df['UsedSpace_in_MB'],explode = myexplode)
    canvaspie = FigureCanvasTkAgg(figpie, master=window)
    canvaspie.draw()
    canvaspie.get_tk_widget().place(x=426.0,y=361.0)

    order=(1,1,1)
    data = np.array(EXSMTdf['UsedSpace_in_MB'])
    model=ARIMA(data, order=order)
    model_result=model.fit()
    forecast_steps = 4
    forecast=model_result.forecast(steps=forecast_steps, alpha=0.05)
    forecast_dates = pd.date_range(EXSMTdf['Time'].iloc[-1], periods=forecast_steps+1, freq='D')[1:]
    forecast_df = pd.DataFrame({'Time': forecast_dates, 'Forecast': forecast})
    for val in forecast: 
        if np.isinf(val): 
            txt="Found an infinity value in forecast!" 
        else: 
            txt="In next 4 weeks, this tablespace will reach : " + str(val)+" MB"        
    pred_text(txt)

    fig = Figure(figsize=(8, 2))
    ax = fig.add_subplot(111)
    ax.plot(EXSMTdf['Time'], EXSMTdf['UsedSpace_in_MB'], linestyle='-', color='Red', label='Used Space')
    ax.plot(EXSMTdf['Time'], EXSMTdf['FreeSpace_in_MB'], linestyle='-', color='Green', label='Free Space')
    ax.plot(forecast_df['Time'], forecast_df['Forecast'], linestyle='--',color='Black', label='Forecast')
    #ax.set_xlabel('Time')
    ax.set_ylabel('Size In MB')
    ax.set_title('Table Space Name: EXSMT')
    ax.grid(True)
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=200.0,y=144.0)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=DB5,
    relief="flat"
)
button_5.place(
    x=32.0,
    y=347.0,
    width=137.0,
    height=24.0
)

window.resizable(False, False)
window.mainloop()
