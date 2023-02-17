from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

WIN_WIDTH = 1000
WIN_HEIGHT = 700

CV_WIDE = 900
CV_HEIGHT = 900

GRAPH_WIDE = 60
GRAPH_HEIGHT = 60

# Cicloid
NUMB_POINTS = 300
A_KOEF = 2
B_KOEF = 3

# Rectangle
LEFT_UP_X = -18
LEFT_UP_Y = 10
RIGHT_DOWN_X = 18
RIGHT_DOWN_Y = -10

X_CENTER = 0
Y_CENTER = 0


def init_all():
    '''
        Функция для вычисления координат всех необходимых объектов
    '''
    x_graph, y_graph = init_graph()
    x_lines, y_lines = init_lines_rect(x_graph, y_graph)
    x_rect, y_rect = init_rectangle()

    x_all = [[X_CENTER], x_graph, x_rect]
    y_all = [[Y_CENTER], y_graph, y_rect]

    for i in range(len(x_lines)):
        x_all.append(x_lines[i])
        y_all.append(y_lines[i])

    draw_picrure(x_all, y_all)

    return x_all, y_all


root = Tk()
root.geometry("%dx%d" % (WIN_WIDTH, WIN_HEIGHT))
root.title("Лабораторная работа №2")
root.resizable(False, False)

x_history = []
y_history = []

fig = plt.figure()

canvas = FigureCanvasTkAgg(fig, master=root)
plot = canvas.get_tk_widget()
plot.place(x=0, y=0, width=CV_WIDE, height=CV_HEIGHT)
build_empty_figure()

x_all, y_all = init_all()

x_history.append(copy.deepcopy(x_all))
y_history.append(copy.deepcopy(y_all))

canvas.draw()

# Figure center
figure_c = Label(root, text="Центр фигуры: (%3.2f;%3.2f)" % (x_all[0][0], y_all[0][0]), width=36)
figure_c.place(x=CV_WIDE + 1, y=WIN_HEIGHT - 100)

# Center
center_label = Label(root, text="Центр(для масштабирования и поворота)")
center_label.place(x=CV_WIDE + 15, y=20)

center_x_label = Label(root, text="X:")
center_x_label.place(x=CV_WIDE + 70, y=50)
center_x = Entry(root, width=9)
center_x.insert(END, "0")
center_x.place(x=CV_WIDE + 100, y=50)

center_y_label = Label(root, text="Y:")
center_y_label.place(x=CV_WIDE + 270, y=50)
center_y = Entry(root, width=9)
center_y.insert(END, "0")
center_y.place(x=CV_WIDE + 300, y=50)

# Spin
spin_label = Label(root, text="Поворот", width=36)
spin_label.place(x=CV_WIDE + 1, y=110)

spin_angle_label = Label(root, text="Угол°: ")
spin_angle_label.place(x=CV_WIDE + 160, y=155)
spin_angle = Entry(root, width=9)
spin_angle.insert(END, "0")
spin_angle.place(x=CV_WIDE + 240, y=155)

spin_btn = Button(root, text="Повернуть", command=lambda: parse_spin(), width=15,
                  height=2)
spin_btn.place(x=CV_WIDE + 160, y=200)

# Scale
scale_label = Label(root, text="Масштабирование", width=36)
scale_label.place(x=CV_WIDE + 1, y=300)

scale_x_label = Label(root, text="kx: ")
scale_x_label.place(x=CV_WIDE + 100, y=360)
scale_x = Entry(root, width=9)
scale_x.insert(END, "1")
scale_x.place(x=CV_WIDE + 140, y=360)

scale_y_label = Label(root, text="ky: ")
scale_y_label.place(x=CV_WIDE + 270, y=360)
scale_y = Entry(root, width=9)
scale_y.insert(END, "1")
scale_y.place(x=CV_WIDE + 310, y=360)

scale_btn = Button(root, text="Масштабировать", command=lambda: parse_scale(), width=15, height=2)
scale_btn.place(x=CV_WIDE + 160, y=420)

# Move
move_label = Label(root, text="Перемещение", width=36)
move_label.place(x=CV_WIDE + 1, y=520)

move_x_label = Label(root, text="dx: ")
move_x_label.place(x=CV_WIDE + 100, y=580)
move_x = Entry(root, width=9)
move_x.insert(END, "0")
move_x.place(x=CV_WIDE + 140, y=580)

move_y_label = Label(root, text="dy: ")
move_y_label.place(x=CV_WIDE + 270, y=580)
move_y = Entry(root, width=9)
move_y.insert(END, "0")
move_y.place(x=CV_WIDE + 310, y=580)

move_btn = Button(root, text="Передвинуть", command=lambda: parse_move(), width=15, height=2)
move_btn.place(x=CV_WIDE + 160, y=640)

line = Label(root, text="", width=36)
line.place(x=CV_WIDE + 1, y=710)

stab_back = Button(root, text="Шаг назад", command=lambda: step_backing(), width=15, height=2)
stab_back.place(x=CV_WIDE + 25, y=760)

clear = Button(root, text="Сбросить", command=lambda: reset(), width=15, height=2)
clear.place(x=CV_WIDE + 300, y=760)

root.mainloop()