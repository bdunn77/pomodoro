from tkinter import *
import math
import subprocess
import os
from tkinter import ttk


def add_task():
    task = task_entry.get()
    if task != "":
        task_list.insert(END, task)
        task_entry.delete(0, END)


def remove_task():
    selected_task = task_list.curselection()
    if selected_task:
        task_list.delete(selected_task)


# Get the file path relative to the current directory
gong_wav = os.path.join(os.path.dirname(__file__), "121800__boss-music__gong.wav")
yoga_wav = os.path.join(os.path.dirname(__file__), "493524__danbl__pulse-breath.wav")


def make_buzz():
    subprocess.Popen(['afplay', "-v", ".1", gong_wav])


# Define the subprocess object
yoga_process = None


def yoga_sound():
    global yoga_process
    yoga_process = subprocess.Popen(['afplay', "-v", ".3", yoga_wav])


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 3
LONG_BREAK_MIN = 10
# WORK_MIN = .05
# SHORT_BREAK_MIN = .05
# LONG_BREAK_MIN = .05
reps = 0
timer = None
push_ups = 0
squats = 0
yoga_count = 0
total_time_worked = 0
# progress = 0
PROGRESS_INCREMENT = 2.5


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    check_mark.config(text="")

    global reps
    global push_ups
    global squats
    global yoga_count
    global total_time_worked
    global yoga_process
    if yoga_process is not None:
        yoga_process.terminate()
        yoga_process = None
    # Calculate total time worked in minutes
    total_time_worked = reps * WORK_MIN

    # Display summary
    summary_label.config(
        text=f"Previous Session Stats\nTotal Time Worked: {total_time_worked} minutes\nTotal Push-ups: {push_ups}\nTotal Squats: {squats}\nTotal Yoga Sessions: {yoga_count}")
    # summary_label.config(text=f"Total Time Worked: {total_time_worked} minutes\nTotal Push-ups: {push_ups}\nTotal "
    #                           f"Squats: {squats}\nTotal Yoga Sessions: {yoga_count}")
    print(summary_label)
    # summary = f"Summary:\nTotal Time Worked: {total_time_worked} minutes\nTotal Push-ups: {push_ups}\nTotal Squats: {squats}\nTotal Yoga Sessions: {yoga_count}"
    # print(summary)  # You can change this to display the summary in the UI or log it to a file

    reps = 0
    push_ups = 0
    squats = 0
    yoga_count = 0
    total_time_worked = 0
    progress_bar["value"] = 0
    push_up_counter.config(text=f"{push_ups} Push Ups")
    squat_counter.config(text=f"{squats} Squats")
    yoga_counter.config(text=f"{yoga_count} Yoga Sessions")
    total_time_worked_label.config(text=f"Total Time Worked: {total_time_worked} minutes")
    return True


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global push_ups
    global squats
    global reps
    global yoga_count
    global total_time_worked
    total_time_worked += 1
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
# TODO make it so there arent overlaps in breaks and yoga time because of remainders
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Long Break. Do 50 Pushups", fg=RED)
        push_ups += 50
        push_up_counter.config(text=f"{push_ups} Push Ups")  # Update push-up count label
        # Finish the progress bar
        progress_bar["value"] = 8
        # progress_bar["value"] = 0

    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Short Break. Do 30 Squats", fg=PINK)
        squats += 30
        squat_counter.config(text=f"{squats} Squats")  # Update squats count label
        # Update the progress bar
        # progress_bar["value"] += PROGRESS_INCREMENT

        # progress_bar.update(10)
    elif reps % 5 == 0:  # Add a condition for yoga counter
        count_down(short_break_sec)
        timer_label.config(text="Yoga Time. Do Yoga Exercises", fg=GREEN)
        yoga_count += 1
        yoga_counter.config(text=f"{yoga_count} Yoga Sessions")
        yoga_sound()

    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)
        # progress_bar["value"] += PROGRESS_INCREMENT


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(seconds):
    progress_bar["value"] = reps
    if reps > 8:
        progress_bar["value"] = 0
        progress_bar["value"] += reps % 8

    count_min = math.floor(seconds / 60)
    count_sec = seconds % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if seconds > 0:
        global timer
        timer = window.after(1000, count_down, seconds - 1)
    else:
        make_buzz()
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_mark.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Add picture to window using Canvas
canvas = Canvas(width=1000, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(500, 112, image=tomato_img)
timer_text = canvas.create_text(500, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# summary label
summary_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 14), wraplength=250, justify="center")
summary_label.grid(column=1, row=7)

# Total time worked label
total_time_worked_label = Label(text=f"Total Time Worked: {total_time_worked} minutes", bg=YELLOW, fg=GREEN,
                                font=(FONT_NAME, 20, "bold"))
total_time_worked_label.grid(column=1, row=5)
# Timer label
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
timer_label.grid(column=1, row=0)

# Start button
start_button = Button(window, text="Start", bg=YELLOW, highlightthickness=0, command=start_timer,
                      font=(FONT_NAME, 20, "bold"))
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(window, text="Reset", bg=YELLOW, highlightthickness=0, command=reset_timer,
                      font=(FONT_NAME, 20, "bold"))
reset_button.grid(column=2, row=2)

# Check mark
check_mark = Label(bg=YELLOW, fg=GREEN, highlightthickness=0)
check_mark.grid(column=1, row=3)

# push_ups
push_up_counter = Label(text=f"{push_ups} Push Ups", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"),
                        highlightthickness=0)
push_up_counter.grid(column=0, row=4, padx=20)
# squats
squat_counter = Label(text=f"{squats} Squats", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"), highlightthickness=0)
squat_counter.grid(column=2, row=4, padx=20)
# yoga sessions
yoga_counter = Label(text=f"{yoga_count} Yoga Sessions", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"),
                     highlightthickness=0)
yoga_counter.grid(column=1, row=4, padx=20)

# Create the task entry field
task_entry = Entry(window, width=25, bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"))
task_entry.grid(column=1, row=8)

# Create the "Add Task" button
add_button = Button(window, text="Add Task", command=add_task, bg=YELLOW, highlightthickness=0,
                    font=(FONT_NAME, 20, "bold"))
add_button.grid(column=1, row=9)

# Create the task list
task_list = Listbox(window, height=6, width=27, bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"))
task_list.grid(row=10, columnspan=3)

# Create the "Remove Task" button
remove_button = Button(window, text="Remove Task", command=remove_task, bg=YELLOW, highlightthickness=0,
                       font=(FONT_NAME, 20, "bold"))
remove_button.grid(column=1, row=11)

progress_bar = ttk.Progressbar(window, maximum=8, length=200, mode="determinate")
progress_bar.grid(column=1, row=15, pady=10)

window.mainloop()
