from tkinter import *
from tkinter import ttk
from datetime import datetime
import calendar

root = Tk()
frm = ttk.Frame(root, padding=10)
root.title("Kalender")
frm.grid()

year = int(datetime.now().strftime("%Y"))
month_name = str(datetime.now().strftime("%B"))
month_number = int(datetime.now().strftime("%m"))

style = ttk.Style(root)
style.theme_use('alt')  # Theme, das Hintergrundfarben unterstützt
#style.theme_use('aqua')  # Standard-Theme
style.configure("CustomButton.TButton", background="orange", foreground="white")

def get_days_in_month(month_number, year):
    return calendar.monthrange(year, month_number)[1]

def get_first_day_of_month(month_number, year):
    return calendar.weekday(year, month_number, 1)

def clear_frame():
    for widget in frm.winfo_children():
        widget.destroy()

def day(choosen_day):
    global month_number,year
    if (choosen_day == int(datetime.now().strftime("%d")) and 
        month_number == int(datetime.now().strftime("%m")) and 
        year == int(datetime.now().strftime("%Y"))):
        print(f"Heute ist der {choosen_day}.{month_number}.{year}")
    else:
        print(f"Das ist der {choosen_day}.{month_number}.{year}")

def next_month():
    global month_number,month_name, year
    if month_number == 12:
        month_number = 1
        month_name = calendar.month_name[month_number]
        year += 1
    else:
        month_number += 1
        month_name = calendar.month_name[month_number]
    clear_frame()
    build_calendar(month_name,month_number,year)

def previous_month():
    global month_number,month_name, year
    if month_number == 1:
        month_number = 12
        month_name = calendar.month_name[month_number]
        year -= 1
    else:
        month_number -= 1
        month_name = calendar.month_name[month_number]
    clear_frame()
    build_calendar(month_name,month_number,year)

def back_to_today():
    global month_number,month_name, year
    month_number = int(datetime.now().strftime("%m"))
    month_name = str(datetime.now().strftime("%B"))
    year = int(datetime.now().strftime("%Y"))
    clear_frame()
    build_calendar(month_name,month_number,year)

def build_menu(month_name,year):
    ttk.Label(frm, text=str(month_name)+" "+str(year),font=('Arial',25)).grid(column=0, row=0, columnspan=3,pady=10)

    ttk.Button(frm, text="<-",command=lambda:previous_month()).grid(column=4, row=0, columnspan=1,pady=10)
    ttk.Button(frm, text="->",command=lambda:next_month()).grid(column=6, row=0, columnspan=1,pady=10)

    ttk.Button(frm, text="Heute",command=lambda:back_to_today()).grid(column=5, row=0, columnspan=1,pady=10)

    ttk.Label(frm, text="Mo").grid(column=0, row=1)
    ttk.Label(frm, text="Di").grid(column=1, row=1)
    ttk.Label(frm, text="Mi").grid(column=2, row=1)
    ttk.Label(frm, text="Do").grid(column=3, row=1)
    ttk.Label(frm, text="Fr").grid(column=4, row=1)
    ttk.Label(frm, text="Sa").grid(column=5, row=1)
    ttk.Label(frm, text="So").grid(column=6, row=1)

def build_calendar(month_name,month_number,year):
    rows = 7
    columns = 6
    label_number = 1
    button_number = 0

    build_menu(month_name,year)

    first_day_of_month = get_first_day_of_month(month_number, year)
    days_in_month = get_days_in_month(month_number, year)

    for i in range(columns):
        for a in range(rows):
            if button_number > days_in_month-1+first_day_of_month:
                ttk.Button(frm, text=" ").grid(column=a, row=i+2)
            elif button_number < first_day_of_month:
                ttk.Button(frm, text=" ").grid(column=a, row=i+2)
            else:
                if label_number == int(datetime.now().day) and month_number == int(datetime.now().strftime("%m")) and year == int(datetime.now().strftime("%Y")):
                    ttk.Button(frm, text=label_number, style="CustomButton.TButton", command=lambda choosen_day=label_number: day(choosen_day)).grid(column=a, row=i+2)
                else:
                    ttk.Button(frm, text=label_number, command=lambda choosen_day=label_number: day(choosen_day)).grid(column=a, row=i+2)
                label_number += 1
            button_number += 1

build_calendar(month_name,month_number,year)
        
root.mainloop()