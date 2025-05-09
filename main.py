import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import matplotlib.pyplot as plt

# Dummy-Funktion für die lineare Funktion
def plot_linear_function():
    try:
        m = float(entry_m.get())
        b = float(entry_b.get())
        x_min = float(entry_x_min.get())
        x_max = float(entry_x_max.get())
        
        if x_min >= x_max:
            result_label.config(text="Error: x_min must be less than x_max")
            return
        
        x = np.linspace(x_min, x_max, 500)
        y = m * x + b
        
        ax.clear()
        ax.plot(x, y, label=f"y = {m}x + {b}")
        ax.set_title("Linear Function")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        canvas.draw()
        result_label.config(text="Plot updated successfully!")
    except ValueError:
        result_label.config(text="Error: Invalid input. Please enter numeric values.")

# Funktion zum Umschalten auf die lineare Funktion
def show_linear_function_inputs():
    for widget in input_frame.winfo_children():
        widget.destroy()
    
    tk.Label(input_frame, text="m:").grid(row=0, column=0, sticky="w")
    global entry_m
    entry_m = tk.Entry(input_frame)
    entry_m.grid(row=0, column=1)
    
    tk.Label(input_frame, text="b:").grid(row=1, column=0, sticky="w")
    global entry_b
    entry_b = tk.Entry(input_frame)
    entry_b.grid(row=1, column=1)
    
    tk.Label(input_frame, text="x_min:").grid(row=2, column=0, sticky="w")
    global entry_x_min
    entry_x_min = tk.Entry(input_frame)
    entry_x_min.grid(row=2, column=1)
    
    tk.Label(input_frame, text="x_max:").grid(row=3, column=0, sticky="w")
    global entry_x_max
    entry_x_max = tk.Entry(input_frame)
    entry_x_max.grid(row=3, column=1)
    
    plot_button = tk.Button(input_frame, text="Plot", command=plot_linear_function)
    plot_button.grid(row=4, column=0, columnspan=2)

# Hauptfenster erstellen
root = tk.Tk()
root.title("Nuclear Physics Calculator")
root.geometry("800x600")

# Linke Spalte für Funktionsauswahl
function_frame = tk.Frame(root, width=200, bg="lightgray")
function_frame.pack(side="left", fill="y")

tk.Label(function_frame, text="Functions", bg="lightgray").pack(pady=10)
linear_button = tk.Button(function_frame, text="Lin. Function", command=show_linear_function_inputs)
linear_button.pack(pady=5)

# Mittlere Spalte für Eingabefelder
input_frame = tk.Frame(root, width=200)
input_frame.pack(side="left", fill="y", padx=10, pady=10)

# Rechte Seite für den Plot
plot_frame = tk.Frame(root, bg="white")
plot_frame.pack(side="right", fill="both", expand=True)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

# Ergebnis-Label
result_label = tk.Label(root, text="", fg="red")
result_label.pack(side="bottom", pady=5)

# Exit-Button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(side="bottom", anchor="e", padx=10, pady=10)

root.mainloop()