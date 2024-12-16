#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[ ]:





# # Direct Path

# In[48]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Load and clean the CSV file
csv_file = "changes.csv"
df = pd.read_csv(csv_file)
df_cleaned = df.dropna(how='all')  # Drops all rows that are completely empty

if len(df_cleaned) < 2:
    raise ValueError("The CSV file does not have enough rows (at least 2 rows after dropping empty ones).")

last_tf = df_cleaned['Time'].iloc[-1]
    
# Create the plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-7, 7)
ax.set_ylim(-7, 7)

# Define sensor points
sensors = {
    "Sensor 1": np.array([-5, 5]),
    "Sensor 2": np.array([0, 5]),
    "Sensor 3": np.array([5, 5]),
    "Sensor 4": np.array([-5, 0]),
    "Sensor 5": np.array([0, 0]),
    "Sensor 6": np.array([5, 0]),
    "Sensor 7": np.array([-5, -5]),
    "Sensor 8": np.array([0, -5]),
    "Sensor 9": np.array([5, -5]),
}

# Plot and label all sensor points
for label, coord in sensors.items():
    ax.plot(coord[0], coord[1], 'ko')  # Plot the sensor points
    ax.text(coord[0] + 0.2, coord[1] + 0.2, label, fontsize=9, color='blue')

# Labels and titles
ax.set_title("Water Moving Between Sensors")
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True)

# Define the vector for the animation
vector, = ax.plot([], [], 'bo-', label="Water Path", markersize=8)
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# Initialize the animation state
current_index = 0
initial_values = df_cleaned.iloc[current_index]
final_values = df_cleaned.iloc[current_index + 1]
ti = initial_values['Time']
xi = initial_values['Xcor']
yi = initial_values['Ycor']
tf = final_values['Time']
xf = final_values['Xcor']
yf = final_values['Ycor']

# Update function for the animation
def update(frame):
    global current_index, ti, xi, yi, tf, xf, yf

    # Update the current segment
    if frame > tf:  # If the animation reaches the end of the current segment
        current_index += 1
        if current_index + 1 >= len(df_cleaned):  # Stop if no more rows are available
            ani.event_source.stop()
            return vector, time_text
        # Update initial and final values for the next segment
        initial_values = df_cleaned.iloc[current_index]
        final_values = df_cleaned.iloc[current_index + 1]
        ti = initial_values['Time']
        xi = initial_values['Xcor']
        yi = initial_values['Ycor']
        tf = final_values['Time']
        xf = final_values['Xcor']
        yf = final_values['Ycor']

    # Calculate the parametric point for the current frame
    if frame <= ti:
        point = np.array([xi, yi])
    elif frame <= tf:
        pt = frame - ti
        x = xi + (xf - xi) * pt / (tf - ti)
        y = yi + (yf - yi) * pt / (tf - ti)
        point = np.array([x, y])
    else:
        point = np.array([xf, yf])

    # Update the vector and time text
    vector.set_data([xi, point[0]], [yi, point[1]])
    time_text.set_text(f"Time: {frame:.2f}s")
    return vector, time_text

# Create the animation
ani = animation.FuncAnimation(
    fig, update, frames=np.arange(ti - 1, last_tf + 1, 0.25), interval=250, blit=True, repeat=True
)

# Show the animation
plt.legend()
plt.show()


# # Probable path/ Cubic Spline 
# 

# In[54]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from scipy.interpolate import CubicSpline

# Load and clean the CSV file
csv_file = "changes.csv"
df = pd.read_csv(csv_file)
df_cleaned = df.dropna(how='all')  # Drops all rows that are completely empty

if len(df_cleaned) < 2:
    raise ValueError("The CSV file does not have enough rows (at least 2 rows after dropping empty ones).")

last_tf = df_cleaned['Time'].iloc[-1]

# Create the plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)

# Define sensor points
sensors = {
    "Sensor 1": np.array([-5, 5]),
    "Sensor 2": np.array([0, 5]),
    "Sensor 3": np.array([5, 5]),
    "Sensor 4": np.array([-5, 0]),
    "Sensor 5": np.array([0, 0]),
    "Sensor 6": np.array([5, 0]),
    "Sensor 7": np.array([-5, -5]),
    "Sensor 8": np.array([0, -5]),
    "Sensor 9": np.array([5, -5]),
}

# Plot and label all sensor points
for label, coord in sensors.items():
    ax.plot(coord[0], coord[1], 'ko')  # Plot the sensor points
    ax.text(coord[0] + 0.2, coord[1] + 0.2, label, fontsize=9, color='blue')

# Labels and titles
ax.set_title("Water Moving Between Sensors")
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True)

# Define the vector for the animation
vector, = ax.plot([], [], 'b-', label="Water Path")  # No markers
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# Generate time values for smoothing the path using cubic spline interpolation
time_points = df_cleaned['Time'].values
x_points = df_cleaned['Xcor'].values
y_points = df_cleaned['Ycor'].values

# Create cubic splines for x(t) and y(t)
spline_x = CubicSpline(time_points, x_points)
spline_y = CubicSpline(time_points, y_points)

# Store all the path points
all_x = []
all_y = []

# Initialize the animation state
current_index = 0
initial_values = df_cleaned.iloc[current_index]
final_values = df_cleaned.iloc[current_index + 1]
ti = initial_values['Time']
xi = initial_values['Xcor']
yi = initial_values['Ycor']
tf = final_values['Time']
xf = final_values['Xcor']
yf = final_values['Ycor']

# Update function for the animation
def update(frame):
    global current_index, ti, xi, yi, tf, xf, yf

    # Update the current segment if needed
    if frame > tf:  # If the animation reaches the end of the current segment
        current_index += 1
        if current_index + 1 >= len(df_cleaned):  # Stop if no more rows are available
            ani.event_source.stop()
            return vector, time_text
        # Update initial and final values for the next segment
        initial_values = df_cleaned.iloc[current_index]
        final_values = df_cleaned.iloc[current_index + 1]
        ti = initial_values['Time']
        xi = initial_values['Xcor']
        yi = initial_values['Ycor']
        tf = final_values['Time']
        xf = final_values['Xcor']
        yf = final_values['Ycor']

    # Calculate the parametric point for the current frame
    x_interp = spline_x(frame)
    y_interp = spline_y(frame)
    all_x.append(x_interp)
    all_y.append(y_interp)

    # Update the vector with all previous points
    vector.set_data(all_x, all_y)
    
    # Update the time text
    time_text.set_text(f"Time: {frame:.2f}s")
    return vector, time_text

# Create the animation
ani = animation.FuncAnimation(
    fig, update, frames=np.arange(ti - 1, last_tf + 1, 0.25), interval=250, blit=True, repeat=True
)

# Show the animation
plt.legend()
plt.show()



# In[ ]:




