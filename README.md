# pycubicspline
Simple python cubic spline library 

![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_1-2.png)

## Description

This is a simple cubic spline library for python.

You can calculate 1D or 2D Spline interpolarion with it.

On the 2D Spline interpolarion,

you can calculate not only 2D position (x,y), but also orientation(yaw angle) and curvature of the position.

This is useful for path planning on robotics.

## Install

download this repository and import pycubicspline.py

## Usage

See the test code in pycubicspline.py.

### 1D spline

    import matplotlib.pyplot as plt
    x = [-0.5, 0.0, 0.5, 1.0, 1.5]
    y = [3.2, 2.7, 6, 5, 6.5]

    spline = Spline(x, y)
    rx = np.arange(-2.0, 4, 0.01)
    ry = [spline.calc(i) for i in rx]

    plt.plot(x, y, "xb")
    plt.plot(rx, ry, "-r")
    plt.grid(True)
    plt.axis("equal")
    plt.show()





![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_1.png)

### 2D spline

![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_1-2.png)


![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_2.png)

![1](https://github.com/AtsushiSakai/pycubicspline/blob/master/images/figure_3.png)


## Requirement

- numpy

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[AtsushiSakai](https://github.com/AtsushiSakai)


