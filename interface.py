from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas
from tkinter import messagebox
from math import sqrt, acos, degrees, pi, sin, cos
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

WIN_WIDTH = 1400
WIN_HEIGHT = 900
WIN_COLOR = "GhostWhite"

CV_WIDE = 900
CV_HEIGHT = 900

GRAPH_WIDE = 60
GRAPH_HEIGHT = 60

TEXT_COLOR = "LightSkyBlue"

# Cicloid
CYCLOID_POINTS = 300  # количество точек для построения эпициклоиды
# должны быть в отношении 2 / 3
A_KF = 2
B_KF = 3

# Rectangle
LEFT_UP_X = -18  # координата X левой верхней точки прямоугольника
LEFT_UP_Y = 10  # координата Y левой верхней точки прямоугольника
RIGHT_DOWN_X = 18  # координата X правой нижней точки прямоугольника
RIGHT_DOWN_Y = -10  # координата Y правой нижней точки прямоугольника

EPS = 0.14  # 0.1973

X_CENTER = 0  # центр по оси X
Y_CENTER = 0  # центр по оси Y


def cycloid(f):
    """
        Функция для получения координат точки эпициклоиды при параметре f
    """
    x = (A_KF + B_KF) * np.cos(f) - A_KF * np.cos((A_KF + B_KF) * f / A_KF)
    y = (A_KF + B_KF) * np.sin(f) - A_KF * np.sin((A_KF + B_KF) * f / A_KF)

    return x + X_CENTER, y + Y_CENTER


def check_intersection(x_graph, y_graph, x, y):
    """
       Функция для нахождения пересечения между линией штриховки прямоугольника и эпициклоидой
    """
    for i in range(len(x_graph)):
        if (abs(x_graph[i] - x) < EPS) and (abs(y_graph[i] - y) < EPS):
            return 1

    return 0


def init_lines_rect(x_graph, y_graph):
    '''
        Функция для нахождения линий штриховки
    '''

    x_all = []
    y_all = []

    # Цикл, в котором проходятся все значения x, чтобы нарисовать линии на прямоугольнике
    for i in range(LEFT_UP_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, 5):
        y_b = RIGHT_DOWN_Y + Y_CENTER
        y_e = LEFT_UP_Y + Y_CENTER

        x_e = LEFT_UP_X + X_CENTER
        x_b = i

        x_line = []
        y_line = []

        # Цикл, в котором проходимся по всем y от y_b до y_e и добавляем координаты в x_line и y_line
        while y_b <= y_e:

            if check_intersection(x_graph, y_graph, x_b, y_b) == 1:
                break

            if x_b < x_e:
                break

            x_line.append(x_b)
            y_line.append(y_b)

            x_b -= 0.01
            y_b += 0.01

        x_all.append(x_line)
        y_all.append(y_line)

    for i in range(LEFT_UP_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, 5):
        y_b = LEFT_UP_Y + Y_CENTER
        y_e = RIGHT_DOWN_Y + Y_CENTER

        x_e = RIGHT_DOWN_X + X_CENTER
        x_b = i

        x_line = []
        y_line = []

        while y_b >= y_e:

            if check_intersection(x_graph, y_graph, x_b, y_b) == 1:
                break

            if x_b > x_e:  # Если x начала линии больше x конца, то выходим из цикла
                break

            x_line.append(x_b)
            y_line.append(y_b)
            x_b += 0.01
            y_b -= 0.01

        x_all.append(x_line)
        y_all.append(y_line)

    return x_all, y_all


# Функция для отрисовки линий штриховки на прямоугольнике
def draw_lines_rect(x_lines, y_lines):
    for line in range(3, len(x_lines)):
        plt.plot(x_lines[line], y_lines[line], 'b')  # Рисуем линию по координатам из x_lines и y_lines


# Функция для нахождения координат вершин прямоугольника
def init_rectangle():
    x_rect = [LEFT_UP_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, RIGHT_DOWN_X + X_CENTER, LEFT_UP_X + X_CENTER,
              LEFT_UP_X + X_CENTER]  # Задаем координаты x вершин прямоугольника
    y_rect = [RIGHT_DOWN_Y + Y_CENTER, RIGHT_DOWN_Y + Y_CENTER, LEFT_UP_Y + Y_CENTER, LEFT_UP_Y + Y_CENTER,
              RIGHT_DOWN_Y + Y_CENTER]  # Задаем координаты y вершин прямоугольника

    return x_rect, y_rect  # Возвращаем координаты вершин прямоугольника


def draw_rectangle(x_rect, y_rect):
    """
       Функция для отрисовки прямоугольника
    """
    plt.plot(x_rect, y_rect, linewidth=3)


# Получаем координаты точек эпициклоиды
def init_cycloid():
    """
        Функция для вычисления координат эпициклоиды для ее последующего построения
    """
    x_arr = []
    y_arr = []

    arr = np.linspace(0, 4 * pi, CYCLOID_POINTS)

    for i in arr:
        x, y = cycloid(i)

        x_arr.append(x)
        y_arr.append(y)

    return x_arr, y_arr


def draw_graph(x_graph, y_graph):
    """
        Функция для отрисовки графика эпициклоиды
    """
    plt.plot(x_graph, y_graph, linewidth=3)


def draw_picrure(x_all, y_all):
    """
        Функция для отрисовки всей картины
    """
    build_empty_figure()

    # Рисуем линии на прямоугольнике
    draw_lines_rect(x_all, y_all)
    # Рисуем прямоугольник
    draw_rectangle(x_all[2], y_all[2])
    # Рисуем эпициклоиду
    draw_graph(x_all[1], y_all[1])

    canvas.draw()


def init_all():
    """
        Функция для вычисления координат всех необходимых объектов
    """
    x_graph, y_graph = init_cycloid()
    x_lines, y_lines = init_lines_rect(x_graph, y_graph)
    x_rect, y_rect = init_rectangle()

    x_all = [[X_CENTER], x_graph, x_rect]
    y_all = [[Y_CENTER], y_graph, y_rect]

    for i in range(len(x_lines)):
        x_all.append(x_lines[i])
        y_all.append(y_lines[i])

    draw_picrure(x_all, y_all)

    return x_all, y_all


def move(x_all, y_all, dx, dy):
    """
        Функция для вычисления координат всех нужных точек при перемещении
    """

    # x_all = [[X_CENTER], x_graph, x_rect]
    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            x_all[i][j] += dx
            y_all[i][j] += dy

    set_figure_center(x_all[0][0], y_all[0][0])

    # deepcopy по причине copy не копирует элементы массива
    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    # отрисовать новейшие фигуры
    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


def spin(x_all, y_all, angle, x_c, y_c):
    """
        Функция для вычисления координат всех нужных точек при повороте
    """

    angle = (angle * pi) / 180

    matrix_spin = np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])

    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            # чтобы координаты центра не мешали вычислениям
            x_all[i][j] -= x_c
            y_all[i][j] -= y_c

            coords = np.dot(matrix_spin, [x_all[i][j], y_all[i][j]])

            # возвращаем координаты центра
            x_all[i][j] = coords[0] + x_c
            y_all[i][j] = coords[1] + y_c

    set_figure_center(x_all[0][0], y_all[0][0])

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


def scale(x_all, y_all, x_c, y_c, kx, ky):
    """
        Функция для вычисления координат всех нужных точек при масштабировании
    """

    for i in range(len(x_all)):
        for j in range(len(x_all[i])):
            # чтобы координаты центра не мешали вычислениям
            x_all[i][j] = kx * (x_all[i][j] - x_c) + x_c
            y_all[i][j] = ky * (y_all[i][j] - y_c) + y_c

    set_figure_center(x_all[0][0], y_all[0][0])

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


def build_empty_figure():
    """
        Функция для очистки поля для последующего построения на нем фигуры
    """
    global ax

    fig.clear()

    # 1x1, первый subplot
    ax = fig.add_subplot(111)

    ax.set_xlim([-GRAPH_WIDE, GRAPH_WIDE])
    ax.set_ylim([-GRAPH_HEIGHT, GRAPH_HEIGHT])
    ax.grid()

    fig.subplots_adjust(right=0.95, left=0.05, bottom=0.05, top=0.95)

    canvas.draw()


def reset():
    """
        Функция для сброса всех преобразований и возврата к начальному состояни фигуры
    """
    global x_all, y_all, x_history, y_history

    set_figure_center(0, 0)

    x_all, y_all = init_all()

    x_history.clear()
    y_history.clear()

    x_history.append(copy.deepcopy(x_all))
    y_history.append(copy.deepcopy(y_all))


def step_backing():
    """
        Функция для возврата к предыдущему состоянию фигуры
    """

    if (len(x_history) == 1):
        messagebox.showerror("Стоп", "Вы дошли до начального изображения")
        return

    x_history.pop()
    y_history.pop()

    set_figure_center(x_history[len(x_history) - 1][0][0], y_history[len(y_history) - 1][0][0])

    draw_picrure(x_history[len(x_history) - 1], y_history[len(y_history) - 1])


def parse_move():
    """
        Функция обработки параметров для перемещения и вызова функции перемещения
    """
    try:
        dx = float(move_x.get())
        dy = float(move_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введена величина смещения")
        return

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    move(x_cur, y_cur, dx, dy)


def parse_spin():
    """
        Функция обработки параметров для поворота и вызова функции поворота
    """
    try:
        x_c = float(center_x.get())
        y_c = float(center_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты центра поворота")

    try:
        angle = float(spin_angle.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введен угол поворота")

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    spin(x_cur, y_cur, angle, x_c, y_c)


def set_figure_center(x_c, y_c):
    """
        Функция для отрисовки в приложении текущего центра фигуры
    """

    figure_c = Label(root, text="Центр фигуры: (%3.2f;%3.2f)" % (x_c, y_c), width=32, font=("Arial", 14),
                     bg=TEXT_COLOR)
    figure_c.place(x=CV_WIDE + 1, y=850)


def parse_scale():
    """
        Функция обработки параметров для масштабирования и вызова функции масштабирования
    """
    try:
        x_c = float(center_x.get())
        y_c = float(center_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты центра поворота")

    try:
        kx = float(scale_x.get())
        ky = float(scale_y.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены коэффициенты масштабирования")

    x_cur = copy.deepcopy(x_history[len(x_history) - 1])
    y_cur = copy.deepcopy(y_history[len(y_history) - 1])

    scale(x_cur, y_cur, x_c, y_c, kx, ky)


root = Tk()
root['bg'] = WIN_COLOR
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
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
figure_c = Label(root, text="Центр фигуры: (%3.2f;%3.2f)" % (x_all[0][0], y_all[0][0]), font=("Arial", 14), width=36,
                 bg=TEXT_COLOR)
figure_c.place(x=CV_WIDE + 1, y=850)

# Center
center_label = Label(root, text="Центр (для масштабирования и поворота)", font=("Arial", 14), bg=WIN_COLOR)
center_label.place(x=CV_WIDE + 15, y=20)

center_x_label = Label(root, text="X:", font=("Arial", 14), bg=WIN_COLOR)
center_x_label.place(x=CV_WIDE + 70, y=50)
center_x = Entry(root, font=("Arial", 14), width=9)
center_x.insert(END, "0")
center_x.place(x=CV_WIDE + 100, y=50)

center_y_label = Label(root, text="Y:", font=("Arial", 14), bg=WIN_COLOR)
center_y_label.place(x=CV_WIDE + 270, y=50)
center_y = Entry(root, font=("Arial", 14), width=9)
center_y.insert(END, "0")
center_y.place(x=CV_WIDE + 300, y=50)

# Spin
spin_label = Label(root, text="Поворот", width=36, font=("Arial", 18), bg=TEXT_COLOR)
spin_label.place(x=CV_WIDE + 1, y=110)

spin_angle_label = Label(root, text="Угол°: ", font=("Arial", 14), bg=WIN_COLOR)
spin_angle_label.place(x=CV_WIDE + 160, y=155)
spin_angle = Entry(root, font=("Arial", 12), width=9)
spin_angle.insert(END, "0")
spin_angle.place(x=CV_WIDE + 240, y=155)

spin_btn = Button(root, text="Повернуть", font=("Arial", 14), command=parse_spin, width=15, height=2, bg=TEXT_COLOR)
spin_btn.place(x=CV_WIDE + 160, y=200)

# Scale
scale_label = Label(root, text="Масштабирование", width=36, font=("Arial", 18), bg=TEXT_COLOR)
scale_label.place(x=CV_WIDE + 1, y=300)

scale_x_label = Label(root, text="kx: ", font=("Arial", 14), bg=WIN_COLOR)
scale_x_label.place(x=CV_WIDE + 100, y=360)
scale_x = Entry(root, font=("Arial", 14), width=9)
scale_x.insert(END, "1")
scale_x.place(x=CV_WIDE + 140, y=360)

scale_y_label = Label(root, text="ky: ", font=("Arial", 14), bg=WIN_COLOR)
scale_y_label.place(x=CV_WIDE + 270, y=360)
scale_y = Entry(root, font=("Arial", 14), width=9)
scale_y.insert(END, "1")
scale_y.place(x=CV_WIDE + 310, y=360)

scale_btn = Button(root, text="Масштабировать", font=("Arial", 14), command=parse_scale,
                   width=15, height=2, bg=TEXT_COLOR)
scale_btn.place(x=CV_WIDE + 160, y=420)

# Move
move_label = Label(root, text="Перемещение", width=36, font=("Arial", 18), bg=TEXT_COLOR)
move_label.place(x=CV_WIDE + 1, y=520)

move_x_label = Label(root, text="Δx: ", font=("Arial", 14), bg=WIN_COLOR)
move_x_label.place(x=CV_WIDE + 100, y=580)
move_x = Entry(root, font=("Arial", 14), width=9)
move_x.insert(END, "0")
move_x.place(x=CV_WIDE + 140, y=580)

move_y_label = Label(root, text="Δy: ", font=("Arial", 14), bg=WIN_COLOR)
move_y_label.place(x=CV_WIDE + 270, y=580)
move_y = Entry(root, font=("Arial", 14), width=9)
move_y.insert(END, "0")
move_y.place(x=CV_WIDE + 310, y=580)

move_btn = Button(root, text="Переместить", font=("Arial", 14), command=parse_move, width=15, height=2, bg=TEXT_COLOR)
move_btn.place(x=CV_WIDE + 160, y=640)

line = Label(root, text="", width=36, font=("Arial", 18), bg=TEXT_COLOR)
line.place(x=CV_WIDE + 1, y=710)

step_back = Button(root, text="Шаг назад", font=("Arial", 14), command=step_backing, width=15, height=2, bg=TEXT_COLOR)
step_back.place(x=CV_WIDE + 25, y=760)

clear = Button(root, text="Сбросить", font=("Arial", 14), command=reset, width=15, height=2, bg=TEXT_COLOR)
clear.place(x=CV_WIDE + 300, y=760)

root.mainloop()
