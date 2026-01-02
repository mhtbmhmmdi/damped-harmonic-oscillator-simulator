import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import time
import matplotlib.pyplot as plt
import csv

running = False        
data_dict = None  


def simulate():
    """
    main simulation function: calculates damped SHM motion, updates animation,
    and stores data for plotting and saving.

    equations used in this simulation:
    1. m*x'' + b*x' + k*x = 0  # mass/spring equation with damping
    2. ω0 = sqrt(k/m)           # natural frequency
    3. y = b/(2*m)              # damping factor
    4. ωd = sqrt(ω0^2 - y^2)    # damped angular frequency
    5. T = 2*pi/ωd              # damped period
    6. x(t) = x0*exp(-y*t) * cos(ωd*t)  # displacement over time
    7. v(t) = -x0*exp(-y*t)*(y*cos(ωd*t) + ωd*sin(ωd*t))  # velocity over time
    8. a(t) = -2*y*v - ω0^2*x   # acceleration over time
    9. ke = 0.5*m*v^2           # kinetic energy
    10. pe = 0.5*k*x^2          # potential energy
    11. te = ke + pe            # total energy
    
    """
    global running, data_dict
    running = True

    
    try:
        m = float(entry_m.get())      # mass in kg
        k = float(entry_k.get())      # spring constant in n/m
        x0 = float(entry_x.get())     # initial displacement in meters
        tmax = float(entry_t.get())   # total simulation time in seconds
        b = float(entry_b.get())      # damping coefficient in kg/s
    except:
        label_result.config(text="please enter valid 'numbers'.")
        return

    # damped SHM parameters
    omega0 = np.sqrt(k/m)             # natural frequency
    y = b/(2*m)                       # damping factor

    if y >= omega0:
        label_result.config(text="overdamped / critical damping!")
        return

    omega_d = np.sqrt(omega0**2 - y**2)    # damped angular frequency
    T = 2*np.pi/omega_d                    # damped period

    
    label_result.config(
        text=f"ω₀={omega0:.2f} | y={y:.2f}\nωd={omega_d:.2f} | T={T:.2f}"
    )

    canvas.delete("all")


    scale = 120
    ox = canvas.winfo_width() // 2
    oy = canvas.winfo_height() // 2
    fps = 60
    dt = 1/fps
    frames = int(tmax*fps)
    r = 30

    times, positions, velocities, accelerations = [], [], [], []
    kinetic_energy, potential_energy, total_energy = [], [], []

    
    for i in range(frames):
        if not running:
            break

        t = i*dt  # current time

        # damped motion equations
        x = x0 * np.exp(-y*t) * np.cos(omega_d*t)  # displacement
        v = -x0 * np.exp(-y*t) * (y*np.cos(omega_d*t) + omega_d*np.sin(omega_d*t))  # velocity
        a = -2*y*v - omega0**2 * x  # acceleration
        ke = 0.5 * m * v**2  # kinetic energy
        pe = 0.5 * k * x**2  # potential energy
        te = ke + pe          # total energy

        
        times.append(t)
        positions.append(x)
        velocities.append(v)
        accelerations.append(a)
        kinetic_energy.append(ke)
        potential_energy.append(pe)
        total_energy.append(te)


        x_pix = ox + x*scale
        canvas.delete("all")

        # draw spring
        spring_points = []
        num_coils = 10
        spring_length = x_pix - ox 
        for j in range(num_coils*2 + 1):
            dx = ox + j*spring_length/(num_coils*2)
            dy = oy + ((-1)**j)*14  # zigzag up and down
            spring_points.append((dx, dy)) 

        for j in range(len(spring_points)-1):  # draw lines between spring points
            canvas.create_line(
                spring_points[j][0], spring_points[j][1],
                spring_points[j+1][0], spring_points[j+1][1],
                fill="blue", width=3
            )

        # draw mass
        r = 30
        canvas.create_oval(
            x_pix-r, oy-r, x_pix+r, oy+r,
            fill="white", outline="blue", width=5
        )

        # draw title text
        canvas.create_text(
            canvas.winfo_width()//2, 40,
            text="Damped Harmonic Oscillator",
            fill="white",
            font=("Comic Sans MS", 25, "bold")
        )

        canvas.update()
        time.sleep(dt)

    # store simulation results in a global dictionary for plotting and saving
    data_dict = {
        "Time (s)": times,
        "Position (m)": positions,
        "Velocity (m/s)": velocities,
        "Acceleration (m/s²)": accelerations,
        "Kinetic Energy (J)": kinetic_energy,
        "Potential Energy (J)": potential_energy,
        "Total Energy (J)": total_energy
    }

    avg_energy = np.mean(total_energy)
    label_energy.config(text=f"Avg Total Energy = {avg_energy:.2f} j")

def stop_simulation():
    global running
    running = False

def plot_data():
    """
    plot the simulation results after running:
    - motion: position, velocity, and acceleration vs time
    - energies: kinetic, potential, and total energy vs time
    """
    if not data_dict: 
        return

    plt.figure(figsize=(10,6))

    # motion plot
    plt.subplot(3,1,1) 
    plt.plot(data_dict["Time (s)"], data_dict["Position (m)"], label="position")
    plt.plot(data_dict["Time (s)"], data_dict["Velocity (m/s)"], label="velocity")
    plt.plot(data_dict["Time (s)"], data_dict["Acceleration (m/s²)"], label="acceleration")
    plt.legend()
    plt.title("damped motion")

    # energy plot
    plt.subplot(3,1,2)
    plt.plot(data_dict["Time (s)"], data_dict["Kinetic Energy (J)"], label="kinetic")
    plt.plot(data_dict["Time (s)"], data_dict["Potential Energy (J)"], label="potential")
    plt.plot(data_dict["Time (s)"], data_dict["Total Energy (J)"], label="total")
    plt.legend()
    plt.title("energies (decay due to damping)")

    plt.tight_layout() 
    plt.show() 

# save data to csv
def save_data():
    if not data_dict:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if not file_path:
        return

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        header = list(data_dict.keys())
        writer.writerow(header)
        for i in range(len(data_dict["Time (s)"])):
            row = [data_dict[key][i] for key in header]
            writer.writerow(row)

# GUI
root = tk.Tk()
root.title("Damped SHM Simulator")
root.configure(bg="black")
root.geometry("950x500")

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="black", foreground="white", font=("Comic Sans MS", 14))
style.configure("TButton", font=("Comic Sans MS", 14, "bold"))
#......
scroll_canvas = tk.Canvas(root, width=325, bg="black", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
scroll_canvas.pack(side=tk.LEFT, fill=tk.Y)
scroll_canvas.configure(yscrollcommand=scrollbar.set) 
#......

# left panel
left_frame = ttk.Frame(scroll_canvas, padding=10)
scroll_canvas.create_window((0, 0), window=left_frame, anchor="nw")
left_frame.bind(
    "<Configure>",
    lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
)



ttk.Label(left_frame, text="Mass (kg)").pack(pady=14)
entry_m = ttk.Entry(left_frame); entry_m.pack(); entry_m.insert(0, "1")

ttk.Label(left_frame, text="Spring k (N/m)").pack(pady=14)
entry_k = ttk.Entry(left_frame); entry_k.pack(); entry_k.insert(0, "10")

ttk.Label(left_frame, text="Initial Displacement (m)").pack(pady=14)
entry_x = ttk.Entry(left_frame); entry_x.pack(); entry_x.insert(0, "1")

ttk.Label(left_frame, text="Simulation Time (s)").pack(pady=14)
entry_t = ttk.Entry(left_frame); entry_t.pack(); entry_t.insert(0, "10")

ttk.Label(left_frame, text="Damping b (kg/s)").pack(pady=14)
entry_b = ttk.Entry(left_frame); entry_b.pack(); entry_b.insert(0, "0.1")


button_frame = ttk.Frame(left_frame)
button_frame.pack(pady=16)


ttk.Button(button_frame, text="Start", command=simulate).pack(side=tk.LEFT, padx=4)
ttk.Button(button_frame, text="Stop", command=stop_simulation).pack(side=tk.LEFT, padx=4)
ttk.Button(left_frame, text="Plot Data", command=plot_data).pack(pady=4)

# labels for results
label_result = ttk.Label(left_frame, text="", font=("Comic Sans MS", 14, "bold"))
label_result.pack(pady=5)
label_energy = ttk.Label(left_frame, text="", font=("Comic Sans MS", 14, "bold"))
label_energy.pack(pady=5)

# save data button
ttk.Frame(left_frame, height=30).pack()
ttk.Label(left_frame, text="Save your simulation data\n        after running:", font=("Comic Sans MS", 14, "italic")).pack(pady=5)
ttk.Button(left_frame, text="Save Data", command=save_data).pack(pady=5)
ttk.Frame(left_frame, height=20).pack()


canvas_frame = ttk.Frame(root)
canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

canvas = tk.Canvas(canvas_frame, width=600, height=400, bg="black")
canvas.pack(expand=True, fill=tk.BOTH, padx=10)

root.mainloop()
