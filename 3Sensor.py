#!/usr/bin/env python
# coding: utf-8

# In[2]:


import csv
import random
import time
import threading

# Thresholds
NORMAL_HUMIDITY_MIN = 30
NORMAL_HUMIDITY_MAX = 35

xcor = 5
ycor = 5

Time = 0
Temperature = 20
Humidity = 30
fieldnames = ["Time", "Temperature", "Humidity"]
anomaly_fieldnames = ["Time", "Xcor", "Ycor", "Humidity"]

print("\rType 'f' to stop the loop, 'a' to run simulation")

# Initialize CSV files
with open('sensor3.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

with open('changes.csv', 'w') as changes_file:
    changes_writer = csv.DictWriter(changes_file, fieldnames=anomaly_fieldnames)
    changes_writer.writeheader()

stop_loop = False
low_temp_mode = False
low_temp_rounds = 0
low_humidity_mode = False
low_humidity_rounds = 0

def log_anomaly(time, xcor, ycor, humidity):
    with open('changes.csv', 'a') as changes_file:
        changes_writer = csv.DictWriter(changes_file, fieldnames=anomaly_fieldnames)
        anomaly_info = {
            "Time": time,
            "Xcor": xcor,
            "Ycor": ycor,
            "Humidity": humidity
        }
        changes_writer.writerow(anomaly_info)
        print(f"\nAnomaly logged: Time: {time}, Xcor: {xcor}, Ycor: {ycor} Humidity: {humidity}")

def loop_function():
    global Time, Temperature, Humidity, stop_loop, low_temp_mode, low_temp_rounds, low_humidity_mode, low_humidity_rounds
    while not stop_loop:
        if low_temp_mode and low_temp_rounds < 1:
            Temperature = random.randint(15, 18)
            low_temp_rounds += 1
        else:
            Temperature = random.randint(20, 23)
            low_temp_mode = False
            low_temp_rounds = 0

        if low_humidity_mode and low_humidity_rounds < 1:
            Humidity = random.randint(40, 45)
            low_humidity_rounds += 1
        else:
            Humidity = random.randint(30, 35)
            low_humidity_mode = False 
            low_humidity_rounds = 0

        # Log to sensor.csv
        with open('sensor3.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "Time": Time,
                "Temperature": Temperature,
                "Humidity": Humidity
            }
            csv_writer.writerow(info)

        # Check for anomalies
        if Humidity < NORMAL_HUMIDITY_MIN or Humidity > NORMAL_HUMIDITY_MAX:
            log_anomaly(Time, xcor, ycor, Humidity)

        print(f"\rTime: {Time}  Temperature: {Temperature}  Humidity: {Humidity}", end="")

        Time += 1
        time.sleep(1)

def check_input():
    global stop_loop, low_temp_mode, low_humidity_mode
    while True:
        content = input()
        if content == 'f':
            stop_loop = True
            break
        elif content == 'a' and not low_temp_mode and not low_humidity_mode:
            low_temp_mode = True
            low_humidity_mode = True

# Start the simulation loop
loop_thread = threading.Thread(target=loop_function)
loop_thread.start()

# Monitor user input
check_input()

loop_thread.join()

print("\nLoop has been stopped.")


# In[ ]:




