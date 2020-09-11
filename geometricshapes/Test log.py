import numpy as np
import matplotlib.pyplot as plt

min = 0.05
max = 0.15
areas = np.array([0.05**2,0.15**2])
single_area = areas[1]/4
areas_trasf = np.array([single_area* 1,single_area * 2, single_area * 3, single_area * 4])
param_size = np.sqrt(areas_trasf)
print (single_area)
print(areas_trasf)
print(param_size)

plt.figure(0)
plt.plot(range(0,4), areas_trasf)
plt.plot(range(0,4), param_size)
print("bo")



