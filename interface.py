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
triangle = []
circle = []
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
        draw_canvas()

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

    for line in triangle:
        canvas.delete(line)
    for auto in triangle:
        canvas.delete(auto)

    # p1_coords = Point(- canvas_width / 2 + p1.x, canvas_height / 2 - p1.y, None)
    # triangle.append(
    #     canvas.create_text(p1.x + 10, p1.y - 10, text=f"({p1_coords.x:.3f}, {p1_coords.y:.3f})", anchor=tk.W))
    # triangle.append(canvas.create_text(p1.x - 10, p1.y + 12, text=f"№{p1.num}", anchor=tk.W))
    #
    # p2_coords = Point(- canvas_width / 2 + p2.x, canvas_height / 2 - p2.y, None)
    # triangle.append(
    #     canvas.create_text(p2.x + 10, p2.y - 10, text=f"({p2_coords.x:.3f}, {p2_coords.y:.3f})", anchor=tk.W))
    # triangle.append(canvas.create_text(p2.x - 10, p2.y + 12, text=f"№{p2.num}", anchor=tk.W))
    #
    # p3_coords = Point(- canvas_width / 2 + p3.x, canvas_height / 2 - p3.y, None)
    # triangle.append(
    #     canvas.create_text(p3.x + 10, p3.y - 10, text=f"({p3_coords.x:.3f}, {p3_coords.y:.3f})", anchor=tk.W))
    # triangle.append(canvas.create_text(p3.x - 10, p3.y + 12, text=f"№{p3.num}", anchor=tk.W))
    #
    # line1 = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="blue")
    # line2 = canvas.create_line(p2.x, p2.y, p3.x, p3.y, fill="blue")
    # line3 = canvas.create_line(p3.x, p3.y, p1.x, p1.y, fill="blue")
    # triangle.append(line1)
    # triangle.append(line2)
    # triangle.append(line3)
    #
    o = get_circle_center(p1, p2, p3)
    if o is None:
        display_message("Error: Impossible to get circle centre", "red")
        for auto in triangle:
            canvas.delete(auto)
        return
    r = get_circle_radius(p1, p2, p3)

    for auto in circle:
        canvas.delete(auto)
    circle.clear()
    # circle.append(canvas.create_oval(o.x - r, o.y - r, o.x + r, o.y + r, fill='', outline='green'))
    #
    # circle.append(canvas.create_oval(o.x - 3, o.y - 3, o.x + 3, o.y + 3, fill="green"))
    # o_coords = Point(- canvas_width / 2 + o.x, canvas_height / 2 - o.y, None)
    # circle.append(canvas.create_oval(o.x - 4, o.y - 4, o.x + 4, o.y + 4, fill="green"))
    # circle.append(canvas.create_text(o.x + 10, o.y - 10, text=f"({o_coords.x:.3f}, {o_coords.y:.3f})", anchor=tk.W))

    scale_to_fit_bbox(p1, p2, p3, o)
    # draw_triangle(p1, p2, p3, o)

    display_message(f"Result: minimal diff is {min_diff}: points in triangle - {p_in}, out of - {p_out}\n"
                    f"Triangle is based on points №{p1.num}, {p2.num}, {p3.num}", "black")


def draw_grid(step):
    for i in range(0, canvas_width, step):
        canvas.create_line(i, 0, i, canvas_height, fill="lightgray", tags="gridline")
    for i in range(0, canvas_height, step):
        canvas.create_line(0, i, canvas_width, i, fill="lightgray", tags="gridline")


def draw_canvas():
    draw_grid(10)

    # Draw the origin
    # canvas.create_text(canvas_width / 2 + 5, canvas_height / 2 + 10, text="(0, 0)", anchor=tk.W)

    # # Draw the x and y axis ticks
    # for x in range(0, canvas_width - 1, 50):
    #     if not x or abs(x) == canvas_width:
    #         continue
    #     canvas.create_line(x, canvas_height - 5, x, canvas_height, width=1)
    #     canvas.create_text(x, canvas_height - 20, text=str(x - canvas_width / 2), anchor='n')
    #
    # for y in range(0, canvas_height - 1, 50):
    #     if not y or abs(y) == canvas_height:
    #         continue
    #     canvas.create_line(-5, y, 5, y, width=1)
    #     canvas.create_text(10, y, text=str(canvas_height / 2 - y), anchor='w')

    # # Label the x and y axis
    # canvas.create_text(canvas_width - 3, canvas_height - 15, text='X', anchor='e')
    # canvas.create_text(15, 10, text='Y', anchor='w')
    #
    # # draw X axis
    # canvas.create_line(3, canvas_height - 3, canvas_width, canvas_height - 3, arrow=tk.LAST, fill='black')
    #
    # # draw Y axis
    # canvas.create_line(5, canvas_height, 5, 5, arrow=tk.LAST, fill='black')

    # draw black border around canvas
    # canvas.create_rectangle(2, 2, canvas_width, canvas_height, outline='black')


def scale_to_fit_bbox(a, b, c, center):
    # определяем bbox
    rad = get_circle_radius(a, b, c)
    bbox = (center.x - rad, center.y - rad, center.x + rad, center.y + rad)

    # получаем размеры bbox
    bbox_width = canvas_width - padding * 2
    bbox_height = canvas_height - padding * 2

    # определяем масштаб, необходимый для изменения размера графика
    scale = min(canvas_width / bbox_width, canvas_height / bbox_height)

    # определяем координаты центра bbox
    center_x = center.x
    center_y = center.y

    # применяем масштабирование и перемещение координат
    ap = copy(a)
    bp = copy(b)
    cp = copy(c)
    cc = copy(center)

    for point in [ap, bp, cp, cc]:
        point.x = (point.x - center_x) * scale + canvas_width / 2
        point.y = (point.y - center_y) * scale + canvas_height / 2

    # проверяем, выходит ли окружность за пределы графика
    max_radius = min(canvas_width, canvas_height) / 2
    if get_circle_radius(ap, bp, cp) > max_radius:
        # масштабируем график так, чтобы радиус окружности был равен максимально возможному значению в пределах графика
        scale = max_radius / get_circle_radius(ap, bp, cp)

    # перерисовываем график
    circle.append(canvas.create_oval(cc.x - scale * get_circle_radius(ap, bp, cp),
                                     cc.y - scale * get_circle_radius(ap, bp, cp),
                                     cc.x + scale * get_circle_radius(ap, bp, cp),
                                     cc.y + scale * get_circle_radius(ap, bp, cp),
                                     outline="green"))

    circle.append(canvas.create_line(scale * ap.x, scale * ap.y, scale * bp.x, scale * bp.y))
    circle.append(canvas.create_line(scale * bp.x, scale * bp.y, scale * cp.x, scale * cp.y))
    circle.append(canvas.create_line(scale * cp.x, cp.y, ap.x, ap.y))
    circle.append(canvas.create_oval(ap.x - 3, ap.y - 3, ap.x + 3, ap.y + 3, fill="green"))
    circle.append(canvas.create_oval(bp.x - 3, bp.y - 3, bp.x + 3, bp.y + 3, fill="green"))
    circle.append(canvas.create_oval(cp.x - 3, cp.y - 3, cp.x + 3, cp.y + 3, fill="green"))
    circle.append(canvas.create_oval(cc.x - 3, cc.y - 3, cc.x + 3, cc.y + 3, fill="blue"))

    o_coords = Point(- canvas_width / 2 + cc.x, canvas_height / 2 - cc.y, None)
    circle.append(canvas.create_oval(cc.x - 4, cc.y - 4, cc.x + 4, cc.y + 4, fill="green"))
    circle.append(canvas.create_text(cc.x + 10, cc.y - 10, text=f"({center.x:.3f}, {center.y:.3f})", anchor=tk.W))

    canvas.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3],
                            outline='red')


def draw_triangle(a, b, c, center):
    # определяем bbox
    rad = get_circle_radius(a, b, c)
    bbox = (0, 0, center.x + rad, center.y + rad)

    # получаем размеры bbox
    bbox_width = bbox[2]
    bbox_height = bbox[3]

    # определяем координаты центра bbox
    bbox_center_x = bbox_width / 2
    bbox_center_y = bbox_height / 2

    # определяем размеры и координаты центра окружности относительно bbox
    circle_center_x = center.x - bbox[0]
    circle_center_y = center.y - bbox[1]
    circle_radius = get_circle_radius(a, b, c)

    # определяем размеры и координаты вершин треугольника относительно bbox
    triangle_points = [a, b, c]
    triangle_points_x = [(p.x - bbox[0]) for p in triangle_points]
    triangle_points_y = [(p.y - bbox[1]) for p in triangle_points]

    # определяем масштаб, необходимый для изменения размера окружности и треугольника
    scale = min(canvas_width / bbox_width, canvas_height / bbox_height)

    # применяем масштаб и сдвиг координат, чтобы переместить окружность и треугольник в центр графика
    circle_center_x = circle_center_x * scale + (canvas_width / 2 - bbox_center_x * scale)
    circle_center_y = circle_center_y * scale + (canvas_height / 2 - bbox_center_y * scale)
    circle_radius *= scale
    triangle_points_x = [x * scale + (canvas_width / 2 - bbox_center_x * scale) for x in triangle_points_x]
    triangle_points_y = [y * scale + (canvas_height / 2 - bbox_center_y * scale) for y in triangle_points_y]

    # перерисовываем окружность
    rad = get_circle_radius(a, b, c)
    circle_center = center
    if circle_center.x - rad < 0:
        circle_center.x = rad
    if circle_center.y - rad < 0:
        circle_center.y = rad
    if circle_center.x + rad > bbox[2]:
        circle_center.x = bbox[2] - rad
    if circle_center.y + rad > bbox[3]:
        circle_center.y = bbox[3] - rad

    circle.append(canvas.create_oval(circle_center.x - rad,
                                     circle_center.y - rad,
                                     circle_center.x + rad,
                                     circle_center.y + rad,
                                     outline="green"))

    canvas.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3],
                            outline='red')

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

draw_canvas()

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

points.append(Point(100, 500, 2))
listbox.insert(tk.END, f"Point {2}: ({100}, {500})")

points.append(Point(100, -50, 3))
listbox.insert(tk.END, f"Point {3}: ({100}, {-50})")

root.mainloop()
