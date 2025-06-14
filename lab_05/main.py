from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas, Radiobutton, LEFT, RIGHT, IntVar, PhotoImage
from tkinter import messagebox

from time import time, sleep


WIN_WIDTH = 1500
WIN_HEIGHT = 800
WIN_COLOR = "#CBF1F5"

CV_WIDE = 700
CV_HEIGHT = 700
CV_COLOR = "#ffffff"
MAIN_TEXT_COLOR = "#11999E"
TEXT_COLOR = "#EEEEEE"

TEMP_SIDE_COLOR_CHECK = (34, 40, 49)  # black
TEMP_SIDE_COLOR = "#222831"

BOX_COLOR = "#71C9CE"

COLOR_LINE = "black"
COLOR_LINE_CHECK = (0, 0, 0)

FILL_COLOR = "#008000"


def check_option(option):
    messagebox.showinfo("Выбран", "Выбрана опция %d" % option)


def clear_canvas():
    canvas_win.delete("all")


def draw_dot(x, y, color):
    image_canvas.put(color, (x, y))



def sign(difference):
    if difference < 0:
        return -1
    elif difference == 0:
        return 0
    else:
        return 1


def bresenham_int(p1, p2, color):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    x = x1
    y = y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    s1 = sign(x2 - x1)
    s2 = sign(y2 - y1)

    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        swaped = 1
    else:
        swaped = 0

    e = 2 * dy - dx

    i = 1

    while i <= dx + 1:

        draw_dot(x, y, color)

        while e >= 0:
            if swaped:
                x = x + s1
            else:
                y = y + s2

            e = e - 2 * dx

        if swaped:
            y = y + s2
        else:
            x = x + s1

        e = e + 2 * dy

        i += 1


def read_dot():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return

    add_dot(int(x), int(y))


def add_dot_click(event):
    x = event.x
    y = event.y

    add_dot(x, y)


def add_dot(x, y, close=False):
    dots_ind = len(dots) - 1  # номер набора точек dots_ind-й фигуры
    dots[dots_ind].append([x, y])

    cur_dot = len(dots[dots_ind]) - 1  # индекс набора точек для текущей фигуры

    if not close:
        dotslist_box.insert(END, "%d. (%4d;%4d)" %(cur_dot + 1, x, y))

    if len(dots[dots_ind]) > 1:
        sides_list[dots_ind].append([dots[dots_ind][cur_dot - 1], dots[dots_ind][cur_dot]])

        bresenham_int(dots[dots_ind][cur_dot - 1], dots[dots_ind][cur_dot], COLOR_LINE)


def del_dot():
    dots_ind = len(dots) - 1
    cur_dot = len(dots[dots_ind]) - 1

    if len(dots[dots_ind]) == 0:
        return

    if len(dots[dots_ind]) > 1:
        sides_list[dots_ind].pop()
        bresenham_int(dots[dots_ind][cur_dot - 1], dots[dots_ind][cur_dot], "white")

    # Find index for a table

    index = 0

    for i in range(dots_ind + 1):
        index += (len(dots[i]))

    dotslist_box.delete(index - 1, END)

    dots[dots_ind].pop(len(dots[dots_ind]) - 1)


def close_figure():
    dots_ind = len(dots)
    cur_dot = len(dots[dots_ind - 1])

    if cur_dot < 3:
        messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")

    add_dot(dots[dots_ind - 1][0][0], dots[dots_ind - 1][0][1], close=True)

    dots.append(list())
    sides_list.append(list())

    dotslist_box.insert(END, "_______________________")


def line_coefficients(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1*y2 - x2*y1

    return a, b, c


def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1*b2 - a2*b1  # oriented product of rays
    opr1 = (-c1)*b2 - b1*(-c2)
    opr2 = a1*(-c2) - (-c1)*a2

    x = opr1 / opr
    y = opr2 / opr

    return x, y


# очерчивание
def round_side(first_dot, second_dot):
    if first_dot[1] == second_dot[1]:
        return

    a_side, b_side, c_side = line_coefficients(first_dot[0], first_dot[1], second_dot[0], second_dot[1])

    if first_dot[1] > second_dot[1]:
        y_max = first_dot[1]
        y_min = second_dot[1]
        x = second_dot[0]
    else:
        y_max = second_dot[1]
        y_min = first_dot[1]
        x = first_dot[0]

    y = y_min

    # цикл сканирующих прямых снизу вверх
    while y < y_max:
        a_scan_line, b_scan_line, c_scan_line = line_coefficients(x, y, x + 1, y)

        # пересечение прямой со стороной
        x_intersection, y_intersection = solve_lines_intersection(a_side, b_side, c_side, a_scan_line, b_scan_line, c_scan_line)

        print("got", image_canvas.get(int(x_intersection), y))

        if image_canvas.get(int(x_intersection) + 1, y) != TEMP_SIDE_COLOR_CHECK:
            image_canvas.put(TEMP_SIDE_COLOR, (int(x_intersection) + 1, y))
        else:
            image_canvas.put(TEMP_SIDE_COLOR, (int(x_intersection) + 2, y))

        y += 1

        canvas_win.update()


def round_figure():
    for figure in range(len(sides_list)):
        sides_num = len(sides_list[figure]) - 1

        for side in range(sides_num + 1):
            round_side(sides_list[figure][side][0], sides_list[figure][side][1])


def get_edges(dots):
    x_max = 0
    x_min = CV_WIDE

    y_max = CV_HEIGHT
    y_min = 0

    for figure in dots:
        for dot in figure:
            if dot[0] > x_max:
                x_max = dot[0]

            if dot[0] < x_min:
                x_min = dot[0]

            if dot[1] < y_max:
                y_max = dot[1]

            if dot[1] > y_min:
                y_min = dot[1]

    block_edges = (x_min, y_min, x_max, y_max)

    return block_edges


def parse_fill():

    dots_ind = len(dots) - 1

    if len(dots[dots_ind]) != 0:
        messagebox.showerror("Ошибка", "Последняя фигура не замкнута")
        return

    block_edges = get_edges(dots)

    if option_filling.get() == 1:
        delay = True
    else:
        delay = False

    color_fill = parse_color(option_color.get())
    print("color " + color_fill)

    fill_with_sides_and_flag(sides_list, block_edges, color_fill, delay = delay)


def fill_with_sides_and_flag(sides_list, block_edges, color_fill, delay = False):
    round_figure()
    canvas_win.update()

    x_max = block_edges[2]
    x_min = block_edges[0]

    y_max = block_edges[3]
    y_min = block_edges[1]

    start_time = time()

    # снизу вверх идут сканирующие линии
    for y in range(y_min, y_max - 1, -1):
        flag = False

        # слева направо чертим
        for x in range(x_min, x_max + 1):

            # если пересекаем ребро - меняем флаг (признак)
            if image_canvas.get(x, y) == TEMP_SIDE_COLOR_CHECK:
                flag = not flag

            if flag:
                image_canvas.put(color_fill, (x, y))
            else:
                image_canvas.put(CV_COLOR, (x, y))

            print("x, y =", x, y, "-> flag", flag)

        if delay:
            canvas_win.update()
            sleep(0.001 * 3)

    end_time = time()

    # Sides
    for fig in sides_list:
        for side in fig:
            bresenham_int(side[0], side[1], COLOR_LINE)

    time_label = Label(text = "Время: %-3.2f с" %(end_time - start_time), font="-family {Consolas} -size 16", bg = "lightgrey")
    time_label.place(x = 20, y = CV_HEIGHT - 50)


def reboot_prog():
    global dots
    global sides_list
    global image_canvas

    canvas_win.delete("all")

    image_canvas = PhotoImage(width = CV_WIDE, height = CV_HEIGHT)
    canvas_win.create_image((CV_WIDE / 2, CV_HEIGHT / 2), image = image_canvas, state = "normal")

    canvas_win.place(x = 0, y = 0)

    dots = [[]]
    sides_list = [[]]
    dotslist_box.delete(0, END)


def parse_color(num_color):
    color = "orange"

    if num_color == 1:
        color = "#ff6e41"
    elif num_color == 2:
        color = "#FF0000"
    elif num_color == 3:
        color = "#0055ff"
    elif num_color == 4:
        color = "#45ff00"

    return color




if __name__ == "__main__":
    '''
        Основной графический модуль
    '''

    win = Tk()
    win['bg'] = WIN_COLOR
    win.geometry("%dx%d" % (WIN_WIDTH, WIN_HEIGHT))
    win.title("ЛР №5. Алгоритм заполнения со списком ребер и флагом.")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)

    image_canvas = PhotoImage(width = CV_WIDE, height = CV_HEIGHT)
    canvas_win.create_image((CV_WIDE / 2, CV_HEIGHT / 2), image = image_canvas, state = "normal")

    canvas_win.place(x = 0, y = 0)

    # Add dot

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 3, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 30)

    add_dot_text = Label(win, text = "Добавить точку", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    add_dot_text.place(x = CV_WIDE + 20, y = 30)

    x_text = Label(text = "x: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    x_text.place(x = CV_WIDE + 70, y = 70)

    x_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    x_entry.place(x = CV_WIDE + 130, y = 70)

    y_text = Label(text = "y: ", font="-family {Consolas} -size 14", bg = BOX_COLOR)
    y_text.place(x = CV_WIDE + 330, y = 70)

    y_entry = Entry(font="-family {Consolas} -size 14", width = 9)
    y_entry.place(x = CV_WIDE + 390, y = 70)

    add_dot_btn = Button(win, text = "Добавить точку", font="-family {Consolas} -size 14", command = lambda: read_dot())
    add_dot_btn.place(x = CV_WIDE + 110, y = 140)

    del_dot_btn = Button(win, text = "Удалить крайнюю", font="-family {Consolas} -size 14", command = lambda: del_dot())
    del_dot_btn.place(x = CV_WIDE + 310, y = 140)

    close_figure_btn = Button(win, text = "Замкнуть фигуру", font="-family {Consolas} -size 14", command = lambda: close_figure())
    close_figure_btn.place(x = CV_WIDE + 200, y = 190)


    # Dots list

    dots = [[]]
    sides_list = [[]]

    back_box = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 9, bg = BOX_COLOR)
    back_box.place(x = CV_WIDE + 20, y = 250)

    dots_list_text = Label(win, text = "Список точек", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    dots_list_text.place(x = CV_WIDE + 20, y = 250)

    dotslist_box = Listbox(bg = "white")
    dotslist_box.configure(height = 7, width = 45)
    dotslist_box.configure(font="-family {Consolas} -size 14")
    dotslist_box.place(x = CV_WIDE + 55, y = 290)

    # Fill figure

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 3, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 500)

    color_text = Label(win, text = "Выбрать тип закраски", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 500)

    option_filling = IntVar()
    option_filling.set(1)

    draw_delay = Radiobutton(text = "С задержкой", font="-family {Consolas} -size 14", variable = option_filling, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    draw_delay.place(x = CV_WIDE + 25, y = 540)

    draw_without_delay = Radiobutton(text = "Без задержки", font="-family {Consolas} -size 14", variable = option_filling, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    draw_without_delay.place(x = CV_WIDE + 350, y = 540)

    fill_figure_btn = Button(win, text = "Закрасить выбранную область", font="-family {Consolas} -size 14", command = lambda: parse_fill())
    fill_figure_btn.place(x = CV_WIDE + 150, y = 590)

    # Binds

    canvas_win.bind("<1>", add_dot_click)

    back_box_filling = Label(text = "", font="-family {Consolas} -size 16", width = 43, height = 5, bg = BOX_COLOR)
    back_box_filling.place(x = CV_WIDE + 20, y = 650)

    color_text = Label(win, text = "Выбрать цвет заполнения", width = 43, font="-family {Consolas} -size 16", bg = MAIN_TEXT_COLOR)
    color_text.place(x = CV_WIDE + 20, y = 650)

    option_color = IntVar()
    option_color.set(1)

    color_orange = Radiobutton(text = "Оранжевый", font="-family {Consolas} -size 14", variable = option_color, value = 1, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_orange.place(x = CV_WIDE + 25, y = 680)

    color_red = Radiobutton(text = "Красный", font="-family {Consolas} -size 14", variable = option_color, value = 2, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_red.place(x = CV_WIDE + 400, y = 680)

    color_blue = Radiobutton(text = "Синий", font="-family {Consolas} -size 14", variable = option_color, value = 3, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_blue.place(x = CV_WIDE + 25, y = 720)

    color_green = Radiobutton(text = "Зеленый", font="-family {Consolas} -size 14", variable = option_color, value = 4, bg = BOX_COLOR, activebackground = BOX_COLOR, highlightbackground = BOX_COLOR)
    color_green.place(x = CV_WIDE + 400, y = 720)

    # Time and clear

    time_label = Label(text="Время: %-3.2f с" % 0, font="-family {Consolas} -size 16", bg="lightgrey")
    time_label.place(x=20, y=CV_HEIGHT - 50)

    clear_win_btn = Button(win, width=42, height=2, text="Очистить экран", font="-family {Consolas} -size 14",
                           command=lambda: reboot_prog())
    clear_win_btn.place(x=20, y=CV_HEIGHT + 20)



    win.mainloop()