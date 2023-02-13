import tkinter as tk
import random

from main import get_min_difference, Point, get_circle_center, get_circle_radius

canvas_width = 500
canvas_height = 500

points = []
triangle = []
circle = []
o_text = []
o_centre = []
width = 15


def display_message(message, color):
    message_box.config(state='normal', fg=color)
    message_box.delete("1.0", "end")
    message_box.insert("end", message)
    message_box.config(state='disabled')


def add_random_point():
    x = float(random.randint(- int(canvas_width / 2), int(canvas_width / 2)))
    y = float(random.randint(- int(canvas_height / 2), int(canvas_height / 2)))

    display_message("Point added: ({}, {})".format(x, y), "green")
    listbox.insert(tk.END, f"Point {len(points) + 1}: ({x}, {y})")

    x = canvas_width / 2 + x
    y = canvas_height / 2 - y
    points.append(Point(x, y))
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")


def add_point():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())

        if abs(x) <= canvas_width / 2 and abs(y) <= canvas_height / 2:
            display_message("Point added: ({}, {})".format(x, y), "green")
            listbox.insert(tk.END, f"Point {len(points) + 1}: ({x}, {y})")

            x = canvas_width / 2 + x
            y = canvas_height / 2 - y
            points.append(Point(x, y))
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        else:
            display_message(
                f"Error: Invalid input. There must be |x| <= {canvas_width / 2} and |y| <= {canvas_height / 2} ", "red")
    except ValueError:
        display_message("Error: Invalid input, must be a number", "red")


def delete_point():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        listbox.delete(index)
        del points[index]
        canvas.delete("all")
        draw_canvas()

        # вот тут трабл
        for point in points:
            x, y = point
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")


def solve():
    if len(points) < 3:
        display_message("Error: There must be at least three points", "red")
        return

    min_diff, res_points = get_min_difference(points)
    print("Минимальная разность:", min_diff)
    print("При точках:", res_points[0] + 1, res_points[1] + 1, res_points[2] + 1)

    p1 = points[res_points[0]]
    p2 = points[res_points[1]]
    p3 = points[res_points[2]]

    for line in triangle:
        canvas.delete(line)

    line1 = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="blue")
    line2 = canvas.create_line(p2.x, p2.y, p3.x, p3.y, fill="blue")
    line3 = canvas.create_line(p3.x, p3.y, p1.x, p1.y, fill="blue")
    triangle.append(line1)
    triangle.append(line2)
    triangle.append(line3)

    o = get_circle_center(p1, p2, p3)
    if o is None:
        display_message("Error: Impossible to get circle centre", "red")
        return
    r = get_circle_radius(p1, p2, p3)

    for auto in circle:
        canvas.delete(auto)
    circle.append(canvas.create_oval(o.x - r, o.y - r, o.x + r, o.y + r, fill='', outline='green'))

    o_coords = Point(- canvas_width / 2 + o.x, canvas_height / 2 - o.y)
    circle.append(canvas.create_oval(o.x - 3, o.y - 3, o.x + 3, o.y + 3, fill="green"))
    circle.append(canvas.create_text(o.x + 10, o.y - 10, text=f"({o_coords.x:.3f}, {o_coords.y:.3f})", anchor=tk.W))


def draw_grid(step):
    for i in range(0, canvas_width, step):
        canvas.create_line(i, 0, i, canvas_height, fill="lightgray", tags="gridline")
    for i in range(0, canvas_height, step):
        canvas.create_line(0, i, canvas_width, i, fill="lightgray", tags="gridline")


def draw_canvas():
    draw_grid(10)

    # Draw the origin
    canvas.create_text(canvas_width / 2 + 5, canvas_height / 2 + 10, text="(0, 0)", anchor=tk.W)

    # Draw the x and y axis ticks
    for x in range(0, canvas_width - 1, 50):
        if not x or x == abs(canvas_width / 2) or abs(x) == canvas_width:
            continue
        canvas.create_line(x, canvas_height / 2 - 5, x, canvas_height / 2 + 5, width=1)
        canvas.create_text(x, canvas_height / 2 + 10, text=str(x - canvas_width / 2), anchor='n')

    for y in range(0, canvas_height - 1, 50):
        if not y or y == abs(canvas_height / 2) or abs(y) == canvas_height:
            continue
        canvas.create_line(canvas_width / 2 - 5, y, canvas_width / 2 + 5, y, width=1)
        canvas.create_text(canvas_width / 2 + 10, y, text=str(canvas_height / 2 - y), anchor='w')

    # Label the x and y axis
    canvas.create_text(canvas_width - 10, canvas_height / 2 + 15, text='X', anchor='e')
    canvas.create_text(canvas_width / 2 - 15, 10, text='Y', anchor='w')

    # draw X axis
    canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, arrow=tk.LAST, fill='black')

    # draw Y axis
    canvas.create_line(canvas_height / 2, canvas_height, canvas_width / 2, 0, arrow=tk.LAST, fill='black')

    # draw black border around canvas
    canvas.create_rectangle(2, 2, canvas_width, canvas_height, outline='black')


root = tk.Tk()
root.title("Circumcircle Problem")
root.geometry("1000x600")

message_box = tk.Text(root, height=2, width=50, state='disabled')
message_box.pack(side='top', fill='x', padx=5, pady=5)

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
