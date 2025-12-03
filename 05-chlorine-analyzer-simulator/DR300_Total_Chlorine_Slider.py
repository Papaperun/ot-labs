
import tkinter as tk

# DR300 Total Chlorine – real pink → purple progression
def mg_to_rgb_and_name(mg):
    mg = max(0.0, min(10.0, float(mg)))
    
    if mg <= 0.05:  return "#ffffff", "Clear / No Color"
    elif mg <= 0.3: return "#fff0f8", "Barely Pink"
    elif mg <= 0.8: return "#ffe0f0", "Light Pink"
    elif mg <= 1.5: return "#ffc0e8", "Rose"
    elif mg <= 3.0: return "#ffa0d8", "Medium Magenta"
    elif mg <= 5.0: return "#ff70c8", "Strong Magenta"
    elif mg <= 7.0: return "#e040b0", "Deep Purple-Pink"
    elif mg <= 9.0: return "#c000a0", "Dark Purple"
    else:           return "#900080", "Off-Scale Purple"

root = tk.Tk()
root.title("DR300 Total Chlorine – Slider Test")
root.configure(bg="black")
root.geometry("600x600")

canvas = tk.Canvas(root, width=500, height=350, bg="#ffffff", highlightthickness=0)
canvas.pack(pady=30)

value_label = tk.Label(root, text="0.00 mg/L Total CL2", font=("Arial", 40, "bold"), fg="white", bg="black", wraplength=650,)
value_label.pack(pady=5)

color_name_label = tk.Label(root, text="", font=("Arial", 20), fg="#ff70c8", bg="black")
color_name_label.pack(pady=10)

# Slider 0.00 → 10.00 (resolution 0.01 mg/L)
slider = tk.Scale(
    root, from_=0, to=10, orient=tk.HORIZONTAL,
    resolution=0.01, length=450,
    bg="black", fg="white", troughcolor="#444",
    highlightthickness=0
)
slider.pack(pady=20)

def update_from_slider(value):
    mg = float(value)
    color, cname = mg_to_rgb_and_name(mg)
    
    canvas.configure(bg=color)
    value_label.config(text=f"{mg:.2f} mg/L")
    color_name_label.config(text=cname)

slider.configure(command=update_from_slider)

# Set default to 1.5 for initial pink
slider.set(1.5)
update_from_slider("1.5")

root.mainloop()
