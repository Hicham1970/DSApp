import tkinter as tk
import math

def T54B():
    try:
        density = float(density_entry.get())
        temperature = float(temperature_entry.get())
        
        dens = density * 1000
        X = int((dens * 100 + 25) / 50) * 0.5
        Y = int((temperature * 1000 + 25) / 50) * 0.05
        
        if 653 <= X <= 770.5:
            A1 = int(10000000000 * 346.4228 / X / X) / 10000000000
            B1 = int(10000000000 * 0.4388 / X) / 10000000000
            C1 = int(10000000 * (A1 + B1) + 0.5) / 10000000
        elif 770.5 < X <= 787.5:
            A1 = int(10000000000 * 2680.3206 / X / X) / 10000000000
            C1 = int(10000000 * (A1 - 0.00336312) + 0.5) / 10000000
        elif 787.5 < X <= 839:
            A1 = int(10000000000 * 594.5418 / X / X) / 10000000000
            C1 = int(10000000 * A1 + 0.5) / 10000000
        elif 839 < X <= 1075:
            A1 = int(10000000000 * 186.9696 / X / X) / 10000000000
            B1 = int(10000000000 * 0.4862 / X) / 10000000000
            C1 = int(10000000 * (A1 + B1) + 0.5) / 10000000
        else:
            result_label.config(text="False")
            return
        
        D = Y - 15
        E1 = -(C1 * D) - (0.8 * C1 * C1 * D * D)
        E = int(100000000 * E1) / 100000000
        F = int(math.exp(E) * 100000000 + 0.5) / 100000000
        F = int(F * 10000 + 0.5) / 10000
        
        result_label.config(text=str(F))
    except ValueError:
        result_label.config(text="Invalid input")

# Create the main window
window = tk.Tk()
window.title("T54B Calculator")

# Create labels
tk.Label(window, text="Temperature:").grid(row=0, column=0, sticky="e")
tk.Label(window, text="Density:").grid(row=1, column=0, sticky="e")
tk.Label(window, text="Result:").grid(row=2, column=0, sticky="e")

# Create entries
temperature_entry = tk.Entry(window)
temperature_entry.grid(row=0, column=1)
density_entry = tk.Entry(window)
density_entry.grid(row=1, column=1)
result_label = tk.Label(window, text="")
result_label.grid(row=2, column=1)

# Create the button
calculate_button = tk.Button(window, text="Calculate", command=T54B)
calculate_button.grid(row=3, columnspan=2)

# Run the main event loop
window.mainloop()
