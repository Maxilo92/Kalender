from tkinter import *
from tkinter import ttk
from datetime import datetime
import calendar

#Globale Variablen
year = int(datetime.now().strftime("%Y"))
month_name = str(datetime.now().strftime("%B"))
month_number = int(datetime.now().strftime("%m"))
selected_date = None
selected_date_count = int(0)
selected_date_range = None
selected_date_range_str = ""
root = None  # Wird später initialisiert
frm = None   # Wird später initialisiert


def get_days_in_month(month_number, year):
    return calendar.monthrange(year, month_number)[1]

def get_first_day_of_month(month_number, year):
    return calendar.weekday(year, month_number, 1)

def clear_frame():
    for widget in frm.winfo_children():
        widget.destroy()

def day(choosen_day):
    global selected_date, month_number, year, selected_date_count, selected_date_range, selected_date_range_str
    if selected_date_count == 0:
        selected_date = (choosen_day, month_number, year)
        selected_date_count = 1
        selected_date_range = [selected_date]
        selected_date_range_str = clean_selected_date_range(str(selected_date_range))
    elif selected_date_count == 1:
        # Speichere Start- und Enddatum der Range
        start_date = selected_date
        end_date = (choosen_day, month_number, year)
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        selected_date_range = [start_date, end_date]
        selected_date_range_str = clean_selected_date_range(str(selected_date_range))
        selected_date_count = 2
    else:
        selected_date_count = 0
        selected_date_range = None
        selected_date_range_str = ""
    
    clear_frame()
    build_calendar(month_name, month_number, year)

def clean_selected_date_range(selected_date_range_str):
    date_range = eval(selected_date_range_str)  # Konvertiere String zurück in Liste von Tupeln
    if len(date_range) == 1:
        day, month, year = date_range[0]
        return f"{day}.{month}.{year}"
    elif len(date_range) == 2:
        start_day, start_month, start_year = date_range[0]
        end_day, end_month, end_year = date_range[1]
        return f"{start_day}.{start_month}.{start_year} bis {end_day}.{end_month}.{end_year}"
    return ""

def is_date_in_range(day, month, year, date_range):
    if len(date_range) == 0:
        return False
    elif len(date_range) == 1:
        day_date, month_date, year_date = date_range[0]
        return day == day_date and month == month_date and year == year_date
    start_day, start_month, start_year = date_range[0]
    end_day, end_month, end_year = date_range[1]
    
    # Erstelle datetime-Objekte für Vergleich
    current_date = datetime(year, month, day)
    start_date = datetime(start_year, start_month, start_day)
    end_date = datetime(end_year, end_month, end_day)

    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    return start_date <= current_date <= end_date


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

def reset_selection():
    global selected_date, selected_date_count, selected_date_range,selected_date_range_str
    selected_date = None
    selected_date_count = 0
    selected_date_range = None
    selected_date_range_str = ""
    clear_frame()
    build_calendar(month_name, month_number, year)

def build_menu(month_name,year):
    ttk.Label(frm, text=str(month_name)+" "+str(year),font=('Arial',25)).grid(column=0, row=0, columnspan=3,pady=10)

    ttk.Button(frm, text="←",command=lambda:previous_month()).grid(column=4, row=0, columnspan=1,pady=10)
    ttk.Button(frm, text="→",command=lambda:next_month()).grid(column=6, row=0, columnspan=1,pady=10)

    ttk.Button(frm, text="Heute",command=lambda:back_to_today()).grid(column=5, row=0, columnspan=1,pady=10)

    ttk.Label(frm, text="Mo").grid(column=0, row=1)
    ttk.Label(frm, text="Di").grid(column=1, row=1)
    ttk.Label(frm, text="Mi").grid(column=2, row=1)
    ttk.Label(frm, text="Do").grid(column=3, row=1)
    ttk.Label(frm, text="Fr").grid(column=4, row=1)
    ttk.Label(frm, text="Sa").grid(column=5, row=1)
    ttk.Label(frm, text="So").grid(column=6, row=1)

    ttk.Label(frm,text=selected_date_range_str).grid(column=2,columnspan=3, row=9,pady=10)
    ttk.Button(frm, text="Reset", command=reset_selection).grid(column=5, row=9)
    ttk.Button(frm, text="Fertig", command=lambda: root.destroy()).grid(column=6, row=9, columnspan=1, pady=10)
    

def build_calendar(month_name,month_number,year):
    global selected_date, selected_date_count, selected_date_range,is_selected
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
                # letzte Tage
                ttk.Button(frm, text=" ").grid(column=a, row=i+2)
            elif button_number < first_day_of_month:
                # erste Tage
                ttk.Button(frm, text=" ").grid(column=a, row=i+2)
            else:
                current_day = label_number
                is_today = (current_day == datetime.now().day and month_number == datetime.now().month and year == datetime.now().year)

                # Prüfe, ob das Datum in der Range liegt
                is_selected = False
                if selected_date_range and selected_date_count == 1:
                    is_selected = is_date_in_range(current_day, month_number, year, selected_date_range)
                elif selected_date_range and selected_date_count == 2:
                    is_selected = is_date_in_range(current_day, month_number, year, selected_date_range)

                if is_today and not(is_selected):
                    # Den Heutigen Tag orange machen
                    ttk.Button(frm, text=label_number, style="TodayButton.TButton", command=lambda choosen_day=label_number: day(choosen_day)).grid(column=a, row=i+2)
                elif is_selected:
                    # ausgewählt Button
                    ttk.Button(frm, text=label_number, style="SelectedButton.TButton", command=lambda choosen_day=label_number: day(choosen_day)).grid(column=a, row=i+2)
                else:
                    # Normaler Button
                    ttk.Button(frm, text=label_number, command=lambda choosen_day=label_number: day(choosen_day)).grid(column=a, row=i+2)
                label_number += 1
            button_number += 1

def start_calendar():
    global root, frm
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    root.title("Kalender")
    frm.grid()
    style = ttk.Style(root)
    style.theme_use('clam')

    font_size = 15
    style.configure("TButton", font=('Arial', font_size))  # Globaler Stil
    style.configure("TodayButton.TButton", background="orange", foreground="white", font=('Arial', font_size))
    style.configure("SelectedButton.TButton", background="blue", foreground="white", font=('Arial', font_size))

    build_calendar(month_name, month_number, year)
    root.mainloop()

def open_calendar():
    global selected_date, root, frm
    selected_date = None
    
    root = Toplevel()
    root.title("Kalender")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    
    style = ttk.Style(root)
    style.theme_use('clam')
    
    font_size = 15
    style.configure("TButton", font=('Arial', font_size))  # Globaler Stil
    style.configure("TodayButton.TButton", background="orange", foreground="white", font=('Arial', font_size))
    style.configure("SelectedButton.TButton", background="blue", foreground="white", font=('Arial', font_size))
    
    build_calendar(month_name, month_number, year)
    # Reset global variables before closing
    global selected_date_count, selected_date_range
    selected_date_count = 0
    selected_date_range = None
    selected_date_range_str = ""
    root.wait_window()
    return selected_date_range,selected_date_count

# Nur ausführen, wenn die Datei direkt gestartet wird
if __name__ == "__main__":
    start_calendar()