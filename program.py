from tkinter import *
import tkinter.messagebox
import cv2 as cv
from cv2 import *
import inspection as myModule
import sys


def nothing(x):
    x


def do_nothing():
    print("Doing absolutely nothing")


def set_ROI(filepath):
    global ref_point
    ref_point = []

    def shape_selection(event, x, y, flags, param):
        global ref_point
        if event == cv2.EVENT_LBUTTONDOWN:
            ref_point = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:
            ref_point.append((x, y))
            cv2.rectangle(img, ref_point[0], ref_point[1], (0, 255, 0), 2)

    img = cv.imread(filepath)
    cv.namedWindow("Set ROI")
    cv.setMouseCallback("Set ROI", shape_selection)
    while 1:
        k = cv.waitKey(1)
        if k!=-1:
            break
        cv.imshow("Set ROI", img)
    cv.destroyAllWindows()
    global x_min, x_max, y_min, y_max
    x_min = ref_point[0][0]
    x_max = ref_point[1][0]
    y_min = ref_point[0][1]
    y_max = ref_point[1][1]


def canny_threshold(smooth_size, filepath):
    img = cv.imread(filepath)
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    filter_img = cv.medianBlur(imgray, smooth_size)
    cv.namedWindow("CANNY")
    cv.createTrackbar("MIN", "CANNY", 0, 255, nothing)
    cv.createTrackbar("MAX", "CANNY", 0, 255, nothing)
    while 1:
        k = cv.waitKey(1)
        if k != -1:
            break
        t1 = cv.getTrackbarPos("MIN", "CANNY")
        t2 = cv.getTrackbarPos("MAX", "CANNY")
        current_img = cv.Canny(filter_img, t1, t2)
        cv.imshow("CANNY", current_img)
    cv.destroyAllWindows()
    global min_threshold
    global max_threshold
    min_threshold = t1
    max_threshold = t2


def read_settings():
    with open("settings\\program_settings.txt", "r") as f:
        settings = f.readlines()
    settings = [x.strip() for x in settings]
    output = []
    for line in settings:
        parts = line.split(';')
        output.append(parts)
    return output


def load_image(path):
    global filepath
    filepath=path
    print("Loading image: "+filepath)
    img = PhotoImage(file=filepath)
    display_image.my_image=img
    root_width=img.width()+40
    root_height=img.height()+40+24+20
    root_posX=int(round(root.winfo_screenwidth()/2))-int(round(root_width/2))
    root_posY=int(round(root.winfo_screenheight()/2))-int(round(root_height/2))-20
    root_geometry = str(root_width)+"x"+str(root_height)+"+"+str(root_posX)+"+"+str(root_posY)
    root.geometry(root_geometry)
    display_image.config(image=display_image.my_image)
    button_settings.config(state=NORMAL)
    button_run.config(state=NORMAL)


def tool_load_image():
    window_load_image = Tk()
    window_load_image.geometry("240x100+550+325")
    window_load_image.title("Load image")

    path = 'images\\'
    path_display = Label(window_load_image, text=path)
    path_display.grid(row=0, column=0, pady=15, sticky=E)

    entry_load_image = Entry(window_load_image)
    entry_load_image.insert(END, '')
    entry_load_image.grid(row=0, column=1, pady=15, sticky=W)

    button_load_function = Button(window_load_image, text="Load", command=lambda: load_image(path+entry_load_image.get()), width=15)
    button_load_function.grid(columnspan=2, pady=5, padx=65)

    status.config(text="Adjust settings or run inspection")
    window_load_image.mainloop()


def tool_run():
    print("Inspection running...")
    settings = read_settings()
    settings_names=[]
    settings_values=[]
    for i in range(len(settings)):
        settings_names.append(settings[i][0])
        for j in range(1,len(settings[i])):
            settings_values.append(settings[i][j])
    for i in range(len(settings_values)):
        settings_values[i]=int(settings_values[i])
    global x, y, w, h, images
    x,y,w,h, filepath_inspected, images = myModule.inspect(filepath, settings_values)
    status.config(text=" Main defect size: "+str(w)+" x "+str(h))
    load_image(filepath_inspected)
    button_display_process.config(state=NORMAL)


def tool_settings():
    def save_on_closing():
        if_save = tkinter.messagebox.askquestion("Quit", "Do you want to save these settings?")
        if if_save=="yes":
                print("Saving settings...")
                with open("settings\\program_settings.txt", "w") as f:
                    f.write(label_0["text"]+";"+str(setting_0_return.get())+"\n")
                    try:
                        f.write(label_1["text"] + ";" + str(min_threshold) + ";" + str(max_threshold) + "\n")
                    except:
                        print(sys.exc_info()[0])
                        print(label_1["text"]+": Setting default value: 30 - 255")
                        f.write(label_1["text"] + ";" + "30;255\n")
                    f.write(label_2["text"] + ";" + setting_2.get() + "\n")
                    f.write(label_3["text"] + ";" + setting_3.get() + "\n")
                    # f.write(label_4["text"] + ";" + str(x_min) + " < x < " + str(x_max) + "," + str(y_min) + " < y < " + str(y_max) + "\n")
                    try:
                        f.write(label_4["text"] + ";" + str(x_min) + ";" + str(x_max) + ";" + str(y_min) + ";" + str(y_max) + "\n")
                    except:
                        print(sys.exc_info()[0])
                        print(label_4["text"]+": Setting default value: 0 < x < 500,200 < y < 335")
                        f.write(label_4["text"] + ";" + "0;500;200;335\n")
                tkinter.messagebox.showinfo("Quit", "Settngs saved in:\nsettings\\program_settings.txt")
        window_settings.destroy()

    print("Accessing settings...")
    settings = read_settings()
    settings_names = []
    settings_values = []
    for i in range(len(settings)):
        settings_names.append(settings[i][0])
        for j in range(1, len(settings[i])):
            settings_values.append(settings[i][j])

    window_settings = Tk()
    window_settings.geometry("375x180+468+300")

    window_settings.title("Settings")

    label_title_default = Label(window_settings, text="Default settings", font='Helvetica 10 bold')
    label_0 = Label(window_settings, text="Filter size")
    label_1 = Label(window_settings, text="Canny threshold")
    label_2 = Label(window_settings, text="Dilation - kernel size")
    label_3 = Label(window_settings, text="Dilation - iterations")
    label_4 = Label(window_settings, text="Region of interest")

    label_title_current = Label(window_settings, text="Current settings", font='Helvetica 10 bold')
    label_0_1 = Label(window_settings, text=str(settings_values[0]))
    label_1_1 = Label(window_settings, text=str(settings_values[1])+"-"+str(settings_values[2]))
    label_2_1 = Label(window_settings, text=str(settings_values[3]))
    label_3_1 = Label(window_settings, text=str(settings_values[4]))
    label_4_1 = Label(window_settings, text="x: "+str(settings_values[5])+"-"+str(settings_values[6])+"\ty: "+str(settings_values[7])+"-"+str(settings_values[8]))

    label_title_default.grid(row=0,columnspan=2)
    label_0.grid(row=1, column=0, sticky=E)
    label_1.grid(row=2, column=0, sticky=E)
    label_2.grid(row=3, column=0, sticky=E)
    label_3.grid(row=4, column=0, sticky=E)
    label_4.grid(row=5, column=0, sticky=E)

    label_title_current.grid(row=0, column=2)
    label_0_1.grid(row=1, column=2)
    label_1_1.grid(row=2, column=2)
    label_2_1.grid(row=3, column=2)
    label_3_1.grid(row=4, column=2)
    label_4_1.grid(row=5, column=2)

    filterType = [3, 5, 7, 9]
    setting_0_return = IntVar(window_settings)
    setting_0_return.set(filterType[0])
    setting_0 = OptionMenu(window_settings,setting_0_return, *filterType)
    setting_0.grid(row=1, column=1)

    setting_1 = Button(window_settings, text="SET", width=15, command=lambda: canny_threshold(setting_0_return.get(), filepath))
    setting_1.grid(row=2, column=1)

    setting_2 = Entry(window_settings)
    setting_2.insert(END, "3")
    setting_2.grid(row=3, column=1, sticky=W)

    setting_3 = Entry(window_settings)
    setting_3.insert(END, "4")
    setting_3.grid(row=4, column=1, sticky=W)

    setting_4_current = Label(window_settings, text="Current ROI")
    setting_4_current.grid(row=5, column=1)
    setting_4 = Button(window_settings, text="SET", width=15, command=lambda:set_ROI(filepath))
    setting_4.grid(row=6, column=1, pady=5)

    window_settings.protocol("WM_DELETE_WINDOW", save_on_closing)
    window_settings.mainloop()


root = Tk()
root.title("Program")
root.geometry("500x500+400+100")

toolbar = Frame(root, bd=1, relief=RIDGE)
toolbar.pack(side=TOP, fill=X)

inspection_frame = Frame(root)
inspection_frame.pack(side=BOTTOM, fill=X)

status = Label(inspection_frame, text="Load image to inspect...", bd=1, relief=SUNKEN, anchor=W, font="Calibri 12", height=2) # bd-border, relief-how border appears, anchor-where
status.pack(side=BOTTOM, fill=X)

button_load = Button(toolbar, text="Load image", command=tool_load_image)
button_load.pack(side=LEFT, padx=2, pady=2)

button_settings = Button(toolbar, text="Settings", state=DISABLED, command=tool_settings)
button_settings.pack(side=LEFT, padx=2,pady=2)

button_run = Button(toolbar, text="Run", state=DISABLED, command=tool_run)
button_run.pack(side=LEFT, padx=2, pady=2)

button_display_process = Button(toolbar, text="Show process", state=DISABLED, command=lambda:myModule.display_process(images))
button_display_process.pack(side=LEFT, padx=2, pady=2)

display_image = Label(inspection_frame)
display_image.pack(padx=20, pady=20)

root.mainloop()
