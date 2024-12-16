#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(i):
    data = pd.read_csv('sensor1.csv')
    x = data['Time']
    y1 = data['Temperature']
    y2 = data['Humidity']

    plt.cla()

    plt.plot(x, y1, label='Temperature')
    plt.plot(x, y2, label='Humidity')

    plt.legend(loc='upper left')

    plt.xlabel('Time')
    plt.ylabel('Temperature/Humidity')
    plt.title('Sensor Readings')
    plt.ylim(10, 55)
    plt.gcf().set_size_inches(8, 7)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()


# In[ ]:




