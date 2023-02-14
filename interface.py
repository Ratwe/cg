import tkinter as tk
import random

from numpy import sqrt

from main import get_min_difference, Point, get_circle_center, get_circle_radius

canvas_width = 600
canvas_height = 600
coords_range = min(canvas_height, canvas_width) / 4

points = []
triangle = []
circle = []
o_text = []
o_centre = []
r = canvas_width / 2
width = 15
pnum = 1


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
        display_message(f"Point {points[index].num} ({- canvas_width / 2 + points[index].x}, {canvas_height / 2 - points[index].y}) removed", "green")
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

    o = get_circle_center(p1, p2, p3)
    if o is None:
        display_message("Error: Impossible to get circle centre", "red")
        for auto in triangle:
            canvas.delete(auto)
        return
    r = get_circle_radius(p1, p2, p3)
    real_r = 250
    k = r / real_r

    for auto in triangle:
        canvas.delete(auto)

    triangle.append(canvas.create_oval(p1.x * k - 3, p1.y * k - 3,
                                       p1.x * k + 3, p1.y * k + 3, fill="black"))
    triangle.append(canvas.create_oval(p2.x - 3, p2.y - 3, p2.x + 3, p2.y + 3, fill="black"))
    triangle.append(canvas.create_oval(p3.x - 3, p3.y - 3, p3.x + 3, p3.y + 3, fill="black"))

    p1_coords = Point(- canvas_width / 2 + p1.x, canvas_height / 2 - p1.y, None)
    triangle.append(canvas.create_text(p1.x + 10, p1.y - 10, text=f"({p1_coords.x:.3f}, {p1_coords.y:.3f})", anchor=tk.W))
    triangle.append(canvas.create_text(p1.x - 10, p1.y + 12, text=f"№{p1.num}", anchor=tk.W))

    p2_coords = Point(- canvas_width / 2 + p2.x, canvas_height / 2 - p2.y, None)
    triangle.append(canvas.create_text(p2.x + 10, p2.y - 10, text=f"({p2_coords.x:.3f}, {p2_coords.y:.3f})", anchor=tk.W))
    triangle.append(canvas.create_text(p2.x - 10, p2.y + 12, text=f"№{p2.num}", anchor=tk.W))

    p3_coords = Point(- canvas_width / 2 + p3.x, canvas_height / 2 - p3.y, None)
    triangle.append(canvas.create_text(p3.x + 10, p3.y - 10, text=f"({p3_coords.x:.3f}, {p3_coords.y:.3f})", anchor=tk.W))
    triangle.append(canvas.create_text(p3.x - 10, p3.y + 12, text=f"№{p3.num}", anchor=tk.W))

    line1 = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="blue")
    line2 = canvas.create_line(p2.x, p2.y, p3.x, p3.y, fill="blue")
    line3 = canvas.create_line(p3.x, p3.y, p1.x, p1.y, fill="blue")
    triangle.append(line1)
    triangle.append(line2)
    triangle.append(line3)

    for auto in circle:
        canvas.delete(auto)
    circle.append(canvas.create_oval(canvas_width / 2 - real_r, canvas_height / 2 - real_r, canvas_width / 2 + real_r,
                                     canvas_height / 2 + real_r, fill='', outline='green'))

    o_coords = Point(- canvas_width / 2 + o.x, canvas_height / 2 - o.y, None)
    circle.append(canvas.create_oval(canvas_width / 2 - 4, canvas_height / 2 - 4, canvas_width / 2 + 4, canvas_height / 2 + 4, fill="green"))
    circle.append(canvas.create_text(canvas_width / 2 + 10, canvas_height / 2 - 10, text=f"({o_coords.x:.3f}, {o_coords.y:.3f})", anchor=tk.W))

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

    # Draw the x and y axis ticks
    for x in range(0, canvas_width - 1, 50):
        if not x or abs(x) == canvas_width:
            continue
        canvas.create_line(x, canvas_height - 5, x, canvas_height, width=1)
        canvas.create_text(x, canvas_height - 20, text=str(x - canvas_width / 2), anchor='n')

    for y in range(0, canvas_height - 1, 50):
        if not y or abs(y) == canvas_height:
            continue
        canvas.create_line(-5, y, 5, y, width=1)
        canvas.create_text(10, y, text=str(canvas_height / 2 - y), anchor='w')

    # Label the x and y axis
    canvas.create_text(canvas_width - 3, canvas_height - 15, text='X', anchor='e')
    canvas.create_text(15, 10, text='Y', anchor='w')

    # draw X axis
    canvas.create_line(3, canvas_height - 3, canvas_width, canvas_height - 3, arrow=tk.LAST, fill='black')

    # draw Y axis
    canvas.create_line(5, canvas_height, 5, 5, arrow=tk.LAST, fill='black')

    # draw black border around canvas
    # canvas.create_rectangle(2, 2, canvas_width, canvas_height, outline='black')


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
x_entry.pack(side='top', padx=width - 1, pady=5)

y_label = tk.Label(root, text="Enter Y:")
y_label.pack(side='top')

y_entry = tk.Entry(root)
y_entry.pack(side='top', padx=width - 1, pady=5)

add_button = tk.Button(root, text="Add", command=add_point, width=width)
add_button.pack(side='top')

add_random_button = tk.Button(root, text="Add Random Point", command=add_random_point, width=width)
add_random_button.pack(side='top')

delete_button = tk.Button(root, text="Delete Point", command=delete_point, width=width)
delete_button.pack(side='top')

solve_button = tk.Button(root, text="Solve", command=solve, width=width)
solve_button.pack(side='top')

root.mainloop()
