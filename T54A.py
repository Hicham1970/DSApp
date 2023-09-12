import tkinter as tk
import math

def T54A():
    try:
        density = float(density_entry.get())
        temperature = float(temperature_entry.get())
        
        C = density * 1000
        D = int((613.9723 / (C * C)) / 0.0000001 + 0.5) * 0.0000001
        F = temperature - 15
        G = int((D * F) / 0.00000001 + 0.5) * 0.00000001
        H = int((0.8 * G) / 0.00000001 + 0.5) * 0.00000001
        Y = math.exp(-G * (H + 1))
        result = int(Y / 0.0001 + 0.5) * 0.0001
        
        result_label.config(text=str(result))
    except ValueError:
        result_label.config(text="Invalid input")

# Create the main window
window = tk.Tk()
window.title("T54A Calculator")

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
calculate_button = tk.Button(window, text="Calculate", command=T54A)
calculate_button.grid(row=3, columnspan=2)

# Run the main event loop
window.mainloop()
