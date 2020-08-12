# pycubicspline

[![Build Status](https://travis-ci.org/AtsushiSakai/pycubicspline.svg?branch=master)](https://travis-ci.org/AtsushiSakai/pycubicspline)

Simple python cubic spline library 

![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_1-2.png)

## Description

This is a simple cubic spline library for python.

You can calculate 1D or 2D Spline interpolation with it.

On the 2D Spline interpolation,

you can calculate not only 2D position (x,y), but also orientation(yaw angle) and curvature of the position.

This is useful for path planning on robotics.

## Install

Download this repository and just import pycubicspline.py

## Usage

See the test code in pycubicspline.py.

### 1D spline

This is an example of 1D spline interpolation.

```python
from pycubicspline import * 
import matplotlib.pyplot as plt

#input 
x = [-0.5, 0.0, 0.5, 1.0, 1.5]
y = [3.2, 2.7, 6, 5, 6.5]

#1D spline interpolation
spline = Spline(x, y)
rx = np.arange(-2.0, 4, 0.01)
ry = [spline.calc(i) for i in rx]

# show interpolation results
plt.plot(x, y, "xb")
plt.plot(rx, ry, "-r")
plt.grid(True)
plt.axis("equal")
plt.show()
```

You can see:

![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_1.png)

### 2D spline

On the 1D spline interpolation, input x must be increasing.

It is unuseful for 2D path planning of robotics.

　

You can use 2D spline class for path planning like this:

```python
import matplotlib.pyplot as plt
input_x = [-2.5, 0.0, 2.5, 5.0, 7.5, 3.0, -1.0]
input_y = [0.7, -6, 5, 6.5, 0.0, 5.0, -2.0]

x, y, yaw, k, travel = calc_2d_spline_interpolation(input_x, input_y, num=200)

plt.subplots(1)
plt.plot(input_x, input_y, "xb", label="input")
plt.plot(x, y, "-r", label="spline")
plt.grid(True)
plt.axis("equal")
plt.xlabel("x[m]")
plt.ylabel("y[m]")
plt.legend()

plt.subplots(1)
plt.plot(travel, [math.degrees(i_yaw) for i_yaw in yaw], "-r", label="yaw")
plt.grid(True)
plt.legend()
plt.xlabel("line length[m]")
plt.ylabel("yaw angle[deg]")

plt.subplots(1)
plt.plot(travel, k, "-r", label="curvature")
plt.grid(True)
plt.legend()
plt.xlabel("line length[m]")
plt.ylabel("curvature [1/m]")

plt.show()

```

You can get 2D spline path like:

![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_1-2.png)

The orientation(yaw) profile of the path,

and the curvature profile can be calculated:

![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_2.png)


![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_3.png)


## Requirement

- numpy

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[AtsushiSakai](https://github.com/AtsushiSakai)


