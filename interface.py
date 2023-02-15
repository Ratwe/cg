import tkinter as tk
import random

from main import get_min_difference, Point, get_circle_center, get_circle_radius

EPS = 1e-8

canvas_width = 600
canvas_height = 600
coords_range = 1000
padding = 0

point_coord = []
new_point_coord = []
points = []
triangle_points = [-1, -1, -1]
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

    points.append(Point(x, y, pnum))
    # canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    pnum += 1
    solve()

def print_points():
    count = 0
    for i in point_coord:
        count += 1
        print(f"{count}: ({i[0]}, {i[1]})")


def add_point():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
        global pnum

        display_message("Point {} added: ({}, {})".format(pnum, x, y), "green")
        listbox.insert(tk.END, f"Point {pnum}: ({x}, {y})")

        points.append(Point(x, y, pnum))
        # canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    except ValueError:
        display_message("Error: Invalid input, must be a number", "red")


def delete_point():
    selected = listbox.curselection()

    if selected:
        index = selected[0]
        display_message(
            f"Point {points[index].num} ({- canvas_width / 2 + points[index].x}, {canvas_height / 2 - points[index].y}) removed", "green")
        listbox.delete(index)
        del points[index]

    solve()


def tranc_coord(y):
    return (-1) * y + canvas_height


def tranc_coord_back(y):
    return canvas_height - y


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

    global point_coord
    point_coord = [[point.x, point.y] for point in points]
    # print_points()
    print(f"point_coord = {point_coord}")

    search_coef_scaling(p1, p2, p3)
    # build_points(p1, p2, p3)
    build_triangle(p1, p2, p3, res_points)

    display_message(f"Result: minimal diff is {min_diff}: points in triangle - {p_in}, out of - {p_out}\n"
                    f"Triangle is based on points №{p1.num}, {p2.num}, {p3.num}", "black")


def build_triangle(p1, p2, p3, res_points):
    canvas.delete("all")
    build_points(p1, p2, p3)

    res_triangle = [new_point_coord[res_points[0]], new_point_coord[res_points[1]], new_point_coord[res_points[2]]]

    canvas.create_line(res_triangle[0], res_triangle[1], width=2, fill="green")
    canvas.create_line(res_triangle[1], res_triangle[2], width=2, fill="green")
    canvas.create_line(res_triangle[0], res_triangle[2], width=2, fill="green")

    k_x, k_y, x_min, y_min = search_coef_scaling(p1, p2, p3)
    R = get_circle_radius(p1, p2, p3) * k_y
    print(f"R = {R}")

    if R > 4:
        R -= 4

    min_y = min(res_triangle[0][1], res_triangle[1][1], res_triangle[2][1])
    max_y = max(res_triangle[0][1], res_triangle[1][1], res_triangle[2][1])

    for i in range(len(point_coord)):
        x = new_point_coord[i][0]
        y = new_point_coord[i][1]
        r = 3.5
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           width=1, fill="black")

        triangle_points = [[p1.x, p1.y], [p2.x, p2.y], [p3.x, p3.y]]

        for j in range(len(triangle_points)):
            if i != triangle_points[j] and j == len(triangle_points) - 1:
                canvas.create_text(x, y - 15,
                                   text="%d [%.1f,%.1f]" % (
                                       i + 1, point_coord[i][0], tranc_coord_back(point_coord[i][1])),
                                   font=("Courier New", 8, "bold"), fill="black")

            elif i == triangle_points[j]:
                if abs(y - min_y) < EPS:
                    canvas.create_text(x, y - 15,
                                       text="%d [%.1f,%.1f]" % (
                                           i + 1, point_coord[i][0], tranc_coord_back(point_coord[i][1])),
                                       font=("Courier New", 8, "bold"), fill="black")

                elif abs(y - max_y) < EPS:
                    canvas.create_text(x, y + 15,
                                       text="%d [%.1f,%.1f]" % (
                                           i + 1, point_coord[i][0], tranc_coord_back(point_coord[i][1])),
                                       font=("Courier New", 8, "bold"), fill="black")

                else:
                    res_triangle.pop(j)
                    res_triangle.sort(key=lambda array: array[1])

                    x_min_y = res_triangle[0][0]
                    x_max_y = res_triangle[1][0]

                    if abs(x - x_min_y) > abs(x - x_max_y):
                        canvas.create_text(x, y - 15,
                                           text="%d [%.1f,%.1f]" % (
                                               i + 1, point_coord[i][0], tranc_coord_back(point_coord[i][1])),
                                           font=("Courier New", 16, "bold"), fill="black")
                    else:
                        canvas.create_text(x, y + 15,
                                           text="%d [%.1f,%.1f]" % (
                                               i + 1, point_coord[i][0], tranc_coord_back(point_coord[i][1])),
                                           font=("Courier New", 16, "bold"), fill="black")
                break


def search_coef_scaling(p1, p2, p3):
    global point_coord
    print(f"point_coord = {point_coord}")

    x_min = point_coord[0][0]
    y_min = point_coord[0][1]

    x_max = point_coord[0][0]
    y_max = point_coord[0][1]

    for i in point_coord:
        x_min = min(i[0], x_min)
        y_min = max(i[1], y_min)

        x_max = max(i[0], x_max)
        y_max = min(i[1], y_max)

    o = get_circle_center(p1, p2, p3)
    r = get_circle_radius(p1, p2, p3)
    print(f"r0 = {r}")
    x_min = min(x_min, o.x - r)
    x_max = max(x_max, o.x + r)
    y_min = max(y_min, tranc_coord(o.y) + r)
    y_max = min(y_max, tranc_coord(o.y) - r)

    y_min = tranc_coord_back(y_min)
    y_max = tranc_coord_back(y_max)

    if x_max != x_min:
        k_x = (0.8 * canvas_width) / (x_max - x_min)
    else:
        k_x = 0

    if y_max != y_min:
        k_y = (0.8 * canvas_height) / (y_max - y_min)
    else:
        k_y = 0

    print(f"k_x = {k_x}")
    print(f"k_y = {k_y}")
    print(f"x_min = {x_min}")
    print(f"y_min = {y_min}")

    return k_x, k_y, x_min, y_min


def build_points(p1, p2, p3):
    n = len(point_coord)
    point_coord.clear()
    new_point_coord.clear()
    canvas.delete("all")

    for i in range(0, n):
        x, y = points[i].x, points[i].y

        y = tranc_coord(y)
        point_coord.append([x, y])

    k_x, k_y, x_min, y_min = search_coef_scaling(p1, p2, p3)

    draw_grid(int(10 * k_x))

    if k_x != 0 and k_y != 0:
        indent_x = 0.1 * canvas_width
        indent_y = 0.1 * canvas_height

        k_x = min(k_x, k_y)
        k_y = k_x

    elif k_x == 0 and k_y != 0:
        indent_x = 0.5 * canvas_width
        indent_y = 0.1 * canvas_height
    elif k_x != 0 and k_y == 0:
        indent_x = 0.1 * canvas_width
        indent_y = 0.5 * canvas_height
    else:
        indent_x = 0.5 * canvas_width
        indent_y = 0.5 * canvas_height

    for i in range(len(point_coord)):
        x = (point_coord[i][0] - x_min) * k_x + indent_x
        y = tranc_coord((tranc_coord_back(point_coord[i][1]) - y_min) * k_y + indent_y)
        new_point_coord.append([x, y])

        r = 3.5
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           width=1, fill="black")

        canvas.create_text(x, y - 15,
                           text="%d [%.1f,%.1f]" % (i + 1, point_coord[i][0], tranc_coord_back(point_coord[i][1])),
                           font=("Courier New", 8, "bold"), fill="black")

    o = get_circle_center(p1, p2, p3)
    x = (o.x - x_min) * k_x + indent_x
    y = tranc_coord((o.y - y_min) * k_y + indent_y)

    r = get_circle_radius(p1, p2, p3) * k_y
    canvas.create_oval(x - r, y - r, x + r, y + r, width=2, outline="red")

    print("point_coord build_point:", point_coord)
    print(f"circle: ({x}, {y}), r = {r}")


def modify_point():
    # получаем индекс выбранной точки
    selection = listbox.curselection()

    if not selection:
        display_message("Please select a point to modify", "red")
        return

    index = int(selection[0])

    # получаем новые координаты точки из полей ввода
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
    except ValueError:
        display_message("Invalid coordinates", "red")
        return

    # обновляем координаты точки
    points[index] = Point(x, y, points[index].num)

    # обновляем строку в listbox
    listbox.delete(index)
    listbox.insert(index, f"Point {index+1}: ({x}, {y})")
    canvas.delete("all")
    solve()


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

delete_button = tk.Button(root, text="Modify Point", command=modify_point, width=tk_width)
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
