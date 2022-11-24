import math
import pyautogui
from tkinter import *
from tkinter import messagebox

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#ffffff"
BLACK = "#000000"
FONT_NAME = "Courier"

REP_TIME_IN_SECONDS = 30
SETUP_TIME_IN_SECONDS = 5

click_coord = None
is_setup = False
is_time_running = False
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    if timer is not None:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")


def click():
    global click_coord

    pyautogui.click(click_coord.x, click_coord.y)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global is_time_running
    if is_time_running:
        btn_start_stop.config(text='Start')
        reset_timer()
        is_time_running = False
    else:
        is_time_running = True
        btn_start_stop.config(text='Stop')
        count_down(REP_TIME_IN_SECONDS)


def setup_click():
    global is_setup
    is_setup = True
    count_down(SETUP_TIME_IN_SECONDS)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count: int):
    count_min = math.floor(count / 60)
    count_sec = math.floor(count % 60)

    if count_min == 0:
        count_min = f'0{count_min}'
    if count_sec < 10:
        count_sec = f'0{count_sec}'

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    global timer, click_coord, is_setup

    if count > 0:
        if click_coord is None and not is_setup:
            messagebox.showwarning('Atenção', 'A posição do mouse não foi definida! Clique na engrenagem e espere.')
            reset_timer()
            return

        timer = window.after(1000, count_down, count - 1)
    else:
        if is_setup:
            is_setup = False
            click_coord = pyautogui.position()
        else:
            click()
            count_down(REP_TIME_IN_SECONDS)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("noIDLE")
window.config(padx=50, pady=50, bg=WHITE)
window.resizable(False, False)

lbl_title = Label(text="noIDLE", font=(FONT_NAME, 35, "bold"), bg=WHITE, fg=BLACK)
lbl_title.grid(column=2, row=0)

canvas = Canvas(width=100, height=100, bg=WHITE, highlightthickness=0)
timer_text = canvas.create_text(50, 50, text="00:00", fill="black", font=(FONT_NAME, 20, "bold"))
canvas.grid(column=2, row=1)

# start_img = PhotoImage(file="images/play.png")
# stop_img = PhotoImage(file="images/stop.png")
btn_start_stop = Button(text='Start', command=start_timer, borderwidth=0, padx=10, bg=WHITE)
btn_start_stop.grid(column=1, row=2)

# gear_img = PhotoImage(file="images/gear.png")
btn_setup = Button(text='Setup',  command=setup_click, borderwidth=0, padx=10, bg=WHITE)
btn_setup.grid(column=3, row=2)

window.mainloop()
