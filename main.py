from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading
from datetime import datetime, timedelta
from tzlocal import get_localzone
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(base_path, 'sleeping_dog.png')

class SleepReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сонный Патруль")
        self.root['bg'] = "#191970"

        def program_info():
            info_window = Toplevel(self.root)
            info_window.title("О программе")
            info_window['bg'] = "#FFE4E1"

            icon = PhotoImage(file=img_path)
            info_window.iconphoto(False, icon)

            description_text = (
                "Программа 'Сонный Патруль' была создана Сашей.\n"
                "Благодаря этой программе мы будем\n"
                "ложиться пораньше и вставать пораньше,\n"
                "чтобы подольше ничего не делать.\n"
                "\n"
                    "Версия:  1.01."
            )

            info_label = Label(info_window, text=description_text, font=("Times New Roman", 14), 
                               bg="#FFE4E1")
            info_label.pack(padx=10, pady=10)

            ok_button = ttk.Button(info_window, text="OK", command=info_window.destroy)
            ok_button.pack(pady=10)

        self.root.option_add("*tearOff", FALSE)
        self.main_menu = Menu()
        self.main_menu.add_command(label="О программе", command=program_info)

        self.root.config(menu=self.main_menu)
        
        icon = PhotoImage(file=img_path)
        self.root.iconphoto(False, icon)

        self.label = Label(root, text="Введите время для напоминания (HH:MM):", 
                                    font=("Times New Roman", 16), background="#191970", foreground="#FFFAF0")
        self.label.pack(pady=10)

        time_frame = Frame(root)
        time_frame.pack(pady=10)

        hours = [f"{i:02}" for i in range(1, 13)]
        minutes = [f"{i:02}" for i in range(60)]
        am_pm = ["AM", "PM"]

        self.hour_combobox = ttk.Combobox(time_frame, values=hours, width=5)
        self.hour_combobox.set("12")
        self.hour_combobox.pack(side=LEFT)

        self.minute_combobox = ttk.Combobox(time_frame, values=minutes, width=5)
        self.minute_combobox.set("00")
        self.minute_combobox.pack(side=LEFT)

        self.ampm_combobox = ttk.Combobox(time_frame, values=am_pm, width=5)
        self.ampm_combobox.set("AM")
        self.ampm_combobox.pack(side=LEFT)

        self.set_button = ttk.Button(root, text="Установить напоминание", command=self.set_reminder)
        self.set_button.pack(pady=10)

        self.reminder_label = Label(root, text="", bg="#191970", fg="#FFFAF0")
        self.reminder_label.pack(pady=10)

        self.reminder_time = None
        self.timezone = get_localzone()
        self.timezone_label = Label(root, text=f"Ваш часовой пояс: {self.timezone}")
        self.timezone_label.pack(pady=10)

    def set_reminder(self):
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()
        ampm = self.ampm_combobox.get()

        hour = int(hour)
        minute = int(minute)

        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0

        reminder_time = datetime.strptime(f"{hour:02}:{minute:02}", "%H:%M").time()
        now = datetime.now(self.timezone)
        self.reminder_time = datetime.combine(now.date(), reminder_time, tzinfo=self.timezone)
        if self.reminder_time < now:
            self.reminder_time = self.reminder_time + timedelta(days=1)
        messagebox.showinfo("Напоминание установлено", f"Напоминание установлено на {self.reminder_time.strftime('%I:%M %p')} ({self.timezone})")
        self.root.iconify()
        self.start_checking_time()

    def start_checking_time(self):
        def check_time():
            while True:
                current_time = datetime.now(self.timezone)
                if current_time >= self.reminder_time:
                    self.show_reminder_window()
                    break
                time.sleep(10)

        thread = threading.Thread(target=check_time)
        thread.daemon = True
        thread.start()

    def show_reminder_window(self):
        self.root.deiconify()
        self.root.lift()
        reminder_window = Toplevel(self.root)
        reminder_window.title("Sasha is on sleep guard")
        reminder_window.geometry("400x300")
        reminder_window['bg'] = "#191970"

        #img_path = 'sleeping_dog.png'
        icon = PhotoImage(file=img_path)
        reminder_window.iconphoto(False, icon)

        img = Image.open(img_path)
        bg_image = ImageTk.PhotoImage(img)

        canvas = Canvas(reminder_window, bg="#191970", width=img.width, height=img.height)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(193, 130, image=bg_image)

        reminder_label = Label(reminder_window, text="Время ложиться спать!", font=("Times New Roman", 20), 
                               bg="#191970", fg="#FFFAF0", compound="bottom")
        canvas.create_window(195, 40, window=reminder_label)

        snooze_button = ttk.Button(reminder_window, text="Отложить на 30 минут", command=self.snooze_reminder)
        canvas.create_window(188, 235, window=snooze_button)

        dismiss_button = ttk.Button(reminder_window, text="Закрыть напоминание", command=reminder_window.destroy)
        canvas.create_window(188, 270, window=dismiss_button)

        reminder_window.bg_image = bg_image
    
    def snooze_reminder(self):
        self.reminder_time += timedelta(minutes=30)
        messagebox.showinfo("Напоминание отложено", f"Напоминание отложено на 30 минут до {self.reminder_time.strftime('%I:%M %p')}.")
        self.root.iconify()
        self.start_checking_time()

if __name__ == "__main__":
    root = Tk()
    app = SleepReminderApp(root)
    root.mainloop()
