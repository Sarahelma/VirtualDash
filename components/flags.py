import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_flags_with_header(frame, flags, colors):
    container = ttk.Frame(frame)
    container.pack(fill='both', expand=True)
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=3)

    img = tk.PhotoImage(file="components/msm.png")
    img = img.subsample(8, 8)
    logo_label = ttk.Label(container, image=img, style='White.TLabel')
    logo_label.image = img
    logo_label.grid(row=0, column=0, padx=10, pady=5)

    title_label = ttk.Label(container, text="Wireless Telemetry\nDiagnostic Tool", font=("Segoe UI", 16, "bold"), foreground="red", style='White.TLabel')
    title_label.grid(row=0, column=1, padx=10, pady=5)

    flags_frame = ttk.Frame(container, style='Black.TFrame')
    flags_frame.grid(row=0, column=2, sticky='nsew', padx=5)

    fig, ax = plt.subplots(figsize=(12, 0.8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    spacing = 3.6
    for i, (flag, color) in enumerate(zip(flags, colors)):
        flags_icon(ax, i * spacing, color, flag[0], flag[1] == 1)

    ax.set_xlim(-0.5, len(flags) * spacing + 0.5)
    ax.set_ylim(0, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout(pad=0.2)

    canvas = FigureCanvasTkAgg(fig, master=flags_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def flags_icon(ax, x, color, code, active):
    display_color = color if active else '#808080'
    triangle = patches.Polygon([[x, 1.2], [x + 1.6, 4.2], [x + 3.2, 1.2]], closed=True, edgecolor=display_color, facecolor='none', linewidth=2)
    ax.add_patch(triangle)
    ax.text(x + 1.6, 2, '!', fontsize=20, ha='center', va='center', color=display_color, fontname='Arial Rounded MT Bold')
    ax.text(x + 1.2, 0.4, code, fontsize=10, ha='center', va='center', color=display_color, fontname='Arial Rounded MT Bold')