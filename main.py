# main.py

# MARK: Imports
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# MARK: Global Constants
r0 = 1.2  # [fm], typischer Wert für den Nuklearradius-Parameter
U_TO_MEV = 931.494  # 1 u in MeV/c²

# MARK: GUI Setup
class NuclearCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nuclear Calculator")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # MARK: Main Layout Frames
        self.left_frame = tk.Frame(self.root, width=200, bg="#f0f0f0")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # MARK: Add Function Buttons
        self.add_function_buttons()

        # MARK: Placeholders for dynamic content
        self.input_fields = []
        self.result_label = None
        self.equation_canvas = None

        # MARK: Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit,
                                     bg="red", fg="white", font=("Arial", 10, "bold"))
        self.exit_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    # MARK: Function Buttons
    def add_function_buttons(self):
        tk.Button(self.left_frame, text="Nuclear radius",
                  command=self.display_nuclear_radius_ui).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(self.left_frame, text="Recoil energy",
                  command=self.display_recoil_energy_ui).pack(pady=10, padx=10, fill=tk.X)

    # MARK: Utility – Clear & Equation
    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.input_fields = []

    def display_equation(self, latex_string):
        if self.equation_canvas:
            self.equation_canvas.get_tk_widget().destroy()

        fig = plt.Figure(figsize=(6, 1), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis("off")
        ax.text(0.5, 0.5, f"${latex_string}$", fontsize=16, ha='center', va='center')

        self.equation_canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        self.equation_canvas.draw()
        self.equation_canvas.get_tk_widget().pack(pady=(20, 10), padx=20, anchor="w")

    # MARK: Input Field Generator
    def create_input(self, label_text, var_name, unit):
        frame = tk.Frame(self.right_frame)
        frame.pack(pady=5, padx=20, anchor="w")

        tk.Label(frame, text=label_text, width=20, anchor="w").pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=10)
        entry.pack(side=tk.LEFT)
        tk.Label(frame, text=unit).pack(side=tk.LEFT, padx=5)

        self.input_fields.append((var_name, entry))

    def get_input_value(self, varname):
        for name, entry in self.input_fields:
            if name == varname:
                return float(entry.get())
        raise ValueError(f"Input field '{varname}' not found.")

    # MARK: UI – Nuclear Radius
    def display_nuclear_radius_ui(self):
        self.clear_right_frame()
        self.display_equation("R_{eq} = r_0 \\cdot A^{1/3}")

        self.create_input("A (Mass Number):", "A", "[unitless]")

        tk.Button(self.right_frame, text="Run", command=self.run_nuclear_radius_calc)\
            .pack(pady=10, padx=20, anchor="w")

        self.result_label = tk.Label(self.right_frame, text="", font=("Courier", 12), fg="blue")
        self.result_label.pack(pady=10, padx=20, anchor="w")

    def run_nuclear_radius_calc(self):
        try:
            A = int(self.get_input_value('A'))
            Req = self.calc_Req(A)
            self.result_label.config(text=f"Result: Req = {Req:.3f} fm")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_Req(self, A):
        if not isinstance(A, int) or A <= 0:
            raise ValueError("A must be a positive integer representing the mass number.")
        return r0 * (A ** (1 / 3))

    # MARK: UI – Recoil Energy
    def display_recoil_energy_ui(self):
        self.clear_right_frame()
        self.display_equation("E_R = \\frac{2 E^2 \\sin^2(\\theta/2)}{m + 2E \\sin^2(\\theta/2)}")

        self.create_input("E (Incoming energy):", "E", "[MeV]")
        self.create_input("θ (Scattering angle):", "theta", "[deg]")
        self.create_input("m (Target mass):", "m", "[u]")

        # Hinweis zur Masseinheit
        unit_hint = tk.Label(self.right_frame, text="Note: 1 u = 931.494 MeV/c²", font=("Arial", 8, "italic"), fg="gray")
        unit_hint.pack(pady=(0, 5), padx=20, anchor="w")

        tk.Button(self.right_frame, text="Run", command=self.run_recoil_energy_calc)\
            .pack(pady=10, padx=20, anchor="w")

        self.result_label = tk.Label(self.right_frame, text="", font=("Courier", 12), fg="blue")
        self.result_label.pack(pady=10, padx=20, anchor="w")

    def run_recoil_energy_calc(self):
        try:
            E = self.get_input_value('E')  # [MeV]
            theta = self.get_input_value('theta')  # [deg]
            m_u = self.get_input_value('m')  # [u]
            m = m_u * U_TO_MEV  # Convert to MeV/c²

            E_R_keV = self.calc_recoil_energy(E, theta, m)
            self.result_label.config(text=f"Result: E₍R₎ = {E_R_keV:.3f} keV")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_recoil_energy(self, E, theta, m):
        theta_radians = math.radians(theta)
        sin2_theta_over_2 = math.sin(theta_radians / 2) ** 2
        E_R = (2 * E**2 * sin2_theta_over_2) / (m + 2 * E * sin2_theta_over_2)
        return E_R * 1000  # Convert MeV to keV


# MARK: Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = NuclearCalculatorApp(root)
    root.mainloop()
