# damped-harmonic-oscillator-simulator
A simple Python-based simulation of a mass–spring system with an adjustable damping coefficient, featuring a Tkinter-based GUI.

## Features
- Simulate mass-spring motion with damping
- Control mass, spring constant, damping, and simulation time
- Real-time animation using Tkinter
- Plot graphs:
   - Position, velocity, acceleration vs time
   - Energies: kinetic, potential, total
- Save simulation data to a CSV file

## Equations
1. m*x'' + b*x' + k*x = 0       # mass/spring equation with damping
2. ω0 = sqrt(k/m)               # natural frequency
3. y = b/(2*m)                  # damping factor
4. ωd = sqrt(ω0^2 - y^2)       # damped angular frequency
5. T = 2*pi/ωd                  # damped period
6. x(t) = x0*exp(-y*t) * cos(ωd*t)                   # displacement over time
7. v(t) = -x0*exp(-y*t)*(y*cos(ωd*t) + ωd*sin(ωd*t)) # velocity over time
8. a(t) = -2*y*v - ω0^2*x                              # acceleration over time
9. ke = 0.5*m*v^2                                     # kinetic energy
10. pe = 0.5*k*x^2                                    # potential energy
11. te = ke + pe                                      # total energy
  
## How to Run
```bash
python DHO.py
