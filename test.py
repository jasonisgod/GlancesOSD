from tkinter import *
import subprocess, threading, requests, mouse

URL = 'http://localhost:61208/api/3/all'
DELAY = 1

TITLE = 'GlancesOSD'
ICON_PATH = 'test.png'
ROOT_GEO = (240, 135, 240, 135)
MENU_GEO = (480, 270, 480, 270)
FONT_FAMILY, FONT_SIZE = 'Consolas', 12
TITLE_SIZE = 50
FG, BG = 'yellow', '#333'
#FONT_SIZE_LIST = [8, 12, 16, 20, 30, 50]

global running
global root, menu, svar, label
global wx, wy

def init_glances():
    subprocess.Popen(["glances", "-w"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def init_polling():
    threading.Timer(DELAY, polling).start()

def polling():
    global running
    if not running: return
    data = ''
    try: data = requests.get(URL).json()
    except: init_glances()
    cpu_used, cpu_temp, gpu_used, gpu_temp, mem_used, mem_total = [' '*6]*6
    try: cpu_used = f'{data["cpu"]["total"]:6.1f}'
    except: pass
    try: cpu_temp = f'{data["sensors"][2]["value"]:6.1f}'
    except: pass
    try: gpu_used = f'{data["gpu"][0]["proc"]:6.1f}'
    except: pass
    try: gpu_temp = f'{data["gpu"][0]["temperature"]:6.1f}'
    except: pass
    try: mem_used = f'{(data["mem"]["used"] / (1<<30)):6.1f}'
    except: pass
    try: mem_total = f'{(data["mem"]["total"] / (1<<30)):6.1f}'
    except: pass
    set_label((cpu_used, cpu_temp, gpu_used, gpu_temp, mem_used, mem_total))
    update_label()
    init_polling()

def on_released():
    root.bind('<B1-Motion>', lambda e: on_moved(e, mode = True))

def on_moved(widget, mode = False):
    global wx, wy
    if mode: 
        wx, wy = widget.x, widget.y
    root.bind('<B1-Motion>', lambda e: on_moved(e))
    mx, my = mouse.get_position()
    root.geometry(f'+{mx - wx}+{my - wy}')

def on_closed(): 
    root.destroy()

def on_clicked_show(): 
    root.deiconify()

def on_clicked_hide(): 
    root.withdraw()

def on_clicked_scale(size):
    label.config(font = (FONT_FAMILY, size))
    update_label()

def init_root():
    global root
    root = Tk()
    root.geometry("%dx%d+%d+%d" % ROOT_GEO)
    root.configure(background = BG)
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.lift()
    root.bind('<B1-Motion>', lambda e: on_moved(e, mode = True))
    root.bind('<ButtonRelease-1>', lambda e: on_released())
    global svar, label
    svar = StringVar()
    label = Label(root, textvariable = svar, fg = FG, bg = BG, font = (FONT_FAMILY, FONT_SIZE))
    label.pack()
    set_label([' '*6]*6)
    update_label()

def init_menu():
    global menu
    menu = Toplevel(root)
    menu.geometry("%dx%d+%d+%d" % MENU_GEO)
    menu.configure(background = BG)
    menu.iconphoto(False, PhotoImage(file = ICON_PATH))
    menu.title(TITLE)
    frame0 = Frame(menu, background = BG)
    frame0.pack(side = TOP, pady = 10)
    frame1 = Frame(menu, background = BG)
    frame1.pack(side = TOP, pady = 10)
    frame2 = Frame(menu, background = BG)
    frame2.pack(side = TOP, pady = 10)
    Label(frame0, text = TITLE, fg = FG, bg = BG, font = (FONT_FAMILY, TITLE_SIZE)).pack()
    Button(frame1, text = "Show", command = on_clicked_show).pack(side = LEFT, padx = 10)
    Button(frame1, text = "Hide", command = on_clicked_hide).pack(side = LEFT, padx = 10)
    Button(frame2, text = "Small", command = lambda: on_clicked_scale(8)).pack(side = LEFT, padx = 10)
    Button(frame2, text = "Normal", command = lambda: on_clicked_scale(12)).pack(side = LEFT, padx = 10)
    Button(frame2, text = "Large", command = lambda: on_clicked_scale(16)).pack(side = LEFT, padx = 10)
    menu.protocol("WM_DELETE_WINDOW", on_closed)

def set_label(data):
    cpu_used, cpu_temp, gpu_used, gpu_temp, mem_used, mem_total = data
    cpu_msg = f'CPU {cpu_used}% {cpu_temp}\'C'
    gpu_msg = f'GPU {gpu_used}% {gpu_temp}\'C'
    mem_msg = f'MEM {mem_used}/ {mem_total}GB'
    msg = '\n'.join([cpu_msg, gpu_msg, mem_msg])
    global svar
    svar.set(msg)

def update_label():
    w, h = label.winfo_reqwidth(), label.winfo_reqheight()
    x, y = root.winfo_x(), root.winfo_y()
    root.geometry(f'{w}x{h}+{x}+{y}')

running = True
init_polling()
init_root()
init_menu()
mainloop()
running = False




# tk.wait_visibility(tk)
# tk.after(1000, lambda:tk.wm_attributes('-type', 'normal'))

# Button(tk, text="-", command=lambda:tk.wm_state('iconic')).pack()
# Button(tk, text="x", command=tk.destroy).pack()

# screen_width = tk.winfo_screenwidth()
# screen_height = tk.winfo_screenheight()
# def hide_title(): tk.wm_attributes('-type', 'splash')
# def show_title(): tk.wm_attributes('-type', 'normal')
# Button(tk, text="Hide Title", command=hide_title).pack()
# Button(tk, text="Show Title", command=show_title).pack()



# def init_interval(func, sec):
#     def func_wrapper():
#         init_interval(func, sec)
#         func()
#     interval = threading.Timer(sec, func_wrapper)
#     interval.start()
#     return interval