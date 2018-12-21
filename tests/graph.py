# test new method to draw graphs
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0,4*np.pi,0.1)
y = np.sin(t)

rect = 0.05,0.05,0.9,0.85

fig1 = plt.figure(figsize = (20,10))
fig1.suptitle(" Drawn with add_axes", fontsize='x-large', fontweight = 'bold')
fig1ax1 = fig1.add_axes(rect)
fig1ax1.plot(t,y,label='sin(x)')
fig1ax1.set_xlabel("t {s}")
fig1ax1.set_ylabel("sin(t) {m}")
fig1ax1.legend(loc='upper right', shadow=True, fontsize='x-large')
fig1ax1.set_title(" Plotting sin(t) ")

#fig2 = plt.figure(figsize=(20,10))
#fig2.suptitle(" Drawn with add_subplot")
#fig2ax1 = fig2.add_subplot(1,1,1)
#fig2ax1.plot(t,y)

plt.show()