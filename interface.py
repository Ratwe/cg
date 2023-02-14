import tkinter as tk
import random
from copy import copy

from numpy import sqrt

from main import get_min_difference, Point, get_circle_center, get_circle_radius

canvas_width = 600
canvas_height = 600
coords_range = 1000  # min(canvas_height, canvas_width)
padding = 0

points = []
o_text = []
o_centre = []
r = canvas_width / 2
tk_width = 15
pnum = 4


def display_message(message, color):
    message_box.config(state='normal', fg=color)
    message_box.delete("1.0", "end")
    message_box.insert("end", message)
    message_box.config(state='disabled')


def add_random_point():
    global pnum, coords_range
    x = float(random.randint(- int(coords_range), int(coords_range)))
    y = float(random.randint(- int(coords_range), int(coords_range)))

    display_message("Point {} added: ({}, {})".format(pnum, x, y), "green")
    listbox.insert(tk.END, f"Point {pnum}: ({x}, {y})")

    x = canvas_width / 2 + x
    y = canvas_height / 2 - y
    points.append(Point(x, y, pnum))
    # canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    pnum += 1


def add_point():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
        global pnum

        if abs(x) <= coords_range and abs(y) <= coords_range:
            display_message("Point {} added: ({}, {})".format(pnum, x, y), "green")
            listbox.insert(tk.END, f"Point {pnum}: ({x}, {y})")

            x = canvas_width / 2 + x
            y = canvas_height / 2 - y
            points.append(Point(x, y, pnum))
            # canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
            pnum += 1
        else:
            display_message(
                f"Error: Invalid input. There must be |x| <= {coords_range} and |y| <= {coords_range} ", "red")
    except ValueError:
        display_message("Error: Invalid input, must be a number", "red")


def delete_point():
    selected = listbox.curselection()

    if selected:
        index = selected[0]
        display_message(
            f"Point {points[index].num} ({- canvas_width / 2 + points[index].x}, {canvas_height / 2 - points[index].y}) removed",
            "green")
        listbox.delete(index)
        del points[index]
        canvas.delete("all")

        for point in points:
            x = point.x
            y = point.y
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")


def solve():
    if len(points) < 3:
        display_message("Error: There must be at least three points", "red")
        return

    min_diff, res_points, p_in, p_out = get_min_difference(points)

    p1 = points[res_points[0]]
    p2 = points[res_points[1]]
    p3 = points[res_points[2]]
    center = get_circle_center(p1, p2, p3)
    print(f"center: ({center.x}, {center.y})")

    # scale_shapes(p1, p2, p3, center, 0.5)
    # print(20*"-")
    # scale_shapes(p1, p2, p3, center, 1)
    # print(20*"-")
    # scale_shapes(p1, p2, p3, center, 2)
    # print(20*"-")
    scale_shapes(p1, p2, p3, center, 3)

    display_message(f"Result: minimal diff is {min_diff}: points in triangle - {p_in}, out of - {p_out}\n"
                    f"Triangle is based on points №{p1.num}, {p2.num}, {p3.num}", "black")


def get_width(a, b, c, o):
    # можно вычислить минимальные и максимальные значения координат
    x_min = min(a.x, b.x, c.x)
    x_max = max(a.x, b.x, c.x)

    # ширина фигуры
    width = x_max - x_min

    print("width", width)
    return width


def get_height(a, b, c, o):
    # можно вычислить минимальные и максимальные значения координат
    y_min = min(a.y, b.y, c.y)
    y_max = max(a.y, b.y, c.y)

    # высота фигуры
    height = y_max - y_min

    print("height", height)
    return height


def scale_shapes(a, b, c, o, scale_factor):
    canvas.delete("all")
    scale_factor_x = (canvas_width - padding) / get_width(a, b, c, o)
    scale_factor_y = (canvas_height - padding) / get_height(a, b, c, o)
    # scale_factor = 2  # min(scale_factor_x, scale_factor_y)
    print("scale_factor", scale_factor)

    # рисуем треугольник
    triangle = canvas.create_polygon(a.x, canvas_height - a.y, b.x, canvas_height - b.y, c.x, canvas_height - c.y, fill="", outline="blue", tags="triangle")

    radius = get_circle_radius(a, b, c)

    # рисуем окружность
    x0 = (o.x - radius) * scale_factor
    y0 = canvas_height - (o.y - radius) * scale_factor
    x1 = (o.x + radius) * scale_factor
    y1 = canvas_height - (o.y + radius) * scale_factor
    circle = canvas.create_oval(x0, y0, x1, y1, outline="red", tags="circle")
    print(f"circle: ({x0}, {y0}) ({x1}, {y1})")

    # получаем координаты всех фигур на холсте
    coords_triangle = canvas.coords(triangle)
    coords_circle = canvas.coords(circle)

    # находим центр холста
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    # масштабируем координаты треугольника
    new_coords_triangle = []
    for i in range(0, len(coords_triangle), 2):
        x = (coords_triangle[i] - center_x) / scale_factor + center_x
        y = (coords_triangle[i+1] - center_y) / scale_factor + center_y
        new_coords_triangle.extend([x, y])
    canvas.coords(triangle, *new_coords_triangle)
    print("triangle coords:", *new_coords_triangle)

    # масштабируем координаты окружности
    new_coords_circle = []
    for i in range(0, len(coords_circle), 2):
        x = (coords_circle[i] - center_x) / scale_factor + center_x
        y = (coords_circle[i+1] - center_y) / scale_factor + center_y
        new_coords_circle.extend([x, y])
    canvas.coords(circle, *new_coords_circle)
    print("circle coords:", *new_coords_circle)

    # масштабируем холст
    canvas.scale("all", center_x, center_y, scale_factor, scale_factor)


def draw_grid(step):
    for i in range(0, canvas_width, step):
        canvas.create_line(i, 0, i, canvas_height, fill="lightgray", tags="gridline")
    for i in range(0, canvas_height, step):
        canvas.create_line(0, i, canvas_width, i, fill="lightgray", tags="gridline")





root = tk.Tk()
root.title("Задача о нахождении оптимального треугольника")
root.geometry("1100x750")
root.resizable(False, False)

message_box = tk.Text(root, height=2, width=50, state='disabled')
message_box.pack(side='top', fill='x', padx=5, pady=5)

# создаем метку (надпись) с двумя строками текста
label = tk.Label(root, text="На плоскости дано множество точек.\nНайти такой треугольник с вершинами в этих точках, "
                            "для которого разность количеств\nточек этого множества, попавших внутрь треугольника и за "
                            "его пределы, но внутри описанной окружности, минимальна.", font=("Arial", 12),
                 wraplength=root.winfo_screenwidth(), justify="left")

# располагаем метку внизу окна и центрируем ее по левой стороне
label.pack(side="bottom", anchor="w")

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack(side="right", padx=20)

frame = tk.Frame(root)
frame.pack(side="right", fill="both", expand=False)

listbox = tk.Listbox(frame, width=50)
listbox.pack(side="right", fill="both", expand=False)

x_label = tk.Label(root, text="Enter X:")
x_label.pack(side='top')

x_entry = tk.Entry(root)
x_entry.pack(side='top', padx=tk_width - 1, pady=5)

y_label = tk.Label(root, text="Enter Y:")
y_label.pack(side='top')

y_entry = tk.Entry(root)
y_entry.pack(side='top', padx=tk_width - 1, pady=5)

add_button = tk.Button(root, text="Add", command=add_point, width=tk_width)
add_button.pack(side='top')

add_random_button = tk.Button(root, text="Add Random Point", command=add_random_point, width=tk_width)
add_random_button.pack(side='top')

delete_button = tk.Button(root, text="Delete Point", command=delete_point, width=tk_width)
delete_button.pack(side='top')

solve_button = tk.Button(root, text="Solve", command=solve, width=tk_width)
solve_button.pack(side='top')

points.append(Point(0, 100, 1))
listbox.insert(tk.END, f"Point {1}: ({0}, {100})")

points.append(Point(100, 200, 2))
listbox.insert(tk.END, f"Point {2}: ({100}, {200})")

points.append(Point(100, 0, 3))
listbox.insert(tk.END, f"Point {3}: ({100}, {0})")

root.mainloop()
