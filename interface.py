import tkinter as tk
import random


def display_message(message):
    message_box.config(state='normal')
    message_box.delete("1.0", "end")
    message_box.insert("end", message)
    message_box.config(state='disabled')


def add_random_point():
    x = float(random.randint(0, 500))
    y = float(random.randint(0, 500))
    points.append((x, y))
    display_message("Point added: ({}, {})".format(x, y))
    listbox.insert(tk.END, f"Point {len(points)}: ({x}, {y})")


def add_point():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
        points.append((x, y))
        display_message("Point added: ({}, {})".format(x, y))
        listbox.insert(tk.END, f"Point {len(points)}: ({x}, {y})")
    except ValueError:
        display_message("Error: Invalid input, must be a number")


def delete_point():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        listbox.delete(index)
        del points[index]


def solve():
    # Your code for finding the triangle and the circumcircle
    pass


root = tk.Tk()
root.title("Circumcircle Problem")
root.geometry("1000x600")
points = []
width = 15

message_box = tk.Text(root, height=2, width=50, state='disabled')
message_box.pack(side='top', fill='x', padx=5, pady=5)

frame = tk.Frame(root)
frame.pack(side="right", fill="both", expand=True)

listbox = tk.Listbox(frame)
listbox.pack(side="right", fill="both", expand=True)

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
