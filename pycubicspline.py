"""
Cubic Spline library on python

author Atsushi Sakai

"""
import bisect
import math

import numpy as np


class Spline:
    """
    Cubic Spline class
    """

    def __init__(self, x, y):
        self.b, self.c, self.d, self.w = [], [], [], []

        self.x = x
        self.y = y

        self.nx = len(x)  # dimension of x
        h = np.diff(x)

        # calc coefficient c
        self.a = [iy for iy in y]

        # calc coefficient c
        A = self.__calc_A(h)
        B = self.__calc_B(h)
        self.c = np.linalg.solve(A, B)

        # calc spline coefficient b and d
        for i in range(self.nx - 1):
            self.d.append((self.c[i + 1] - self.c[i]) / (3.0 * h[i]))
            tb = (self.a[i + 1] - self.a[i]) / h[i] - h[i] * \
                 (self.c[i + 1] + 2.0 * self.c[i]) / 3.0
            self.b.append(tb)

    def calc(self, t):
        """
        Calc position

        if t is outside of the input x, return None

        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = self.a[i] + self.b[i] * dx + self.c[i] * dx ** 2.0 + self.d[i] * dx ** 3.0

        return result

    def calc_d(self, t):
        """
        Calc first derivative

        if t is outside of the input x, return None
        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = self.b[i] + 2.0 * self.c[i] * dx + 3.0 * self.d[i] * dx ** 2.0
        return result

    def calc_dd(self, t):
        """
        Calc second derivative
        """

        if t < self.x[0]:
            return None
        elif t > self.x[-1]:
            return None

        i = self.__search_index(t)
        dx = t - self.x[i]
        result = 2.0 * self.c[i] + 6.0 * self.d[i] * dx
        return result

    def __search_index(self, x):
        return bisect.bisect(self.x, x) - 1

    def __calc_A(self, h):
        A = np.zeros((self.nx, self.nx))
        A[0, 0] = 1.0
        for i in range(self.nx - 1):
            if i != (self.nx - 2):
                A[i + 1, i + 1] = 2.0 * (h[i] + h[i + 1])
            A[i + 1, i] = h[i]
            A[i, i + 1] = h[i]

        A[0, 1] = 0.0
        A[self.nx - 1, self.nx - 2] = 0.0
        A[self.nx - 1, self.nx - 1] = 1.0
        #  print(A)
        return A

    def __calc_B(self, h):
        """
        calc matrix B for spline coefficient c
        """
        B = np.zeros(self.nx)
        for i in range(self.nx - 2):
            B[i + 1] = 3.0 * (self.a[i + 2] - self.a[i + 1]) / \
                       h[i + 1] - 3.0 * (self.a[i + 1] - self.a[i]) / h[i]
        #  print(B)
        return B

    def calc_curvature(self, t):
        j = int(math.floor(t))
        if j < 0:
            j = 0
        elif j >= len(self.a):
            j = len(self.a) - 1

        dt = t - j
        df = self.b[j] + 2.0 * self.c[j] * dt + 3.0 * self.d[j] * dt * dt
        ddf = 2.0 * self.c[j] + 6.0 * self.d[j] * dt
        k = ddf / ((1 + df ** 2) ** 1.5)
        return k


class Spline2D:
    """
    2D Cubic Spline class
    """

    def __init__(self, x, y):
        self.s = self.__calc_s(x, y)
        self.sx = Spline(self.s, x)
        self.sy = Spline(self.s, y)

    def __calc_s(self, x, y):
        dx = np.diff(x)
        dy = np.diff(y)
        self.ds = [math.sqrt(idx ** 2 + idy ** 2)
                   for (idx, idy) in zip(dx, dy)]
        s = [0.0]
        s.extend(np.cumsum(self.ds))
        return s

    def calc_position(self, s):
        """
        calc position
        """
        x = self.sx.calc(s)
        y = self.sy.calc(s)

        return x, y

    def calc_curvature(self, s):
        """
        calc curvature
        """
        dx = self.sx.calc_d(s)
        ddx = self.sx.calc_dd(s)
        dy = self.sy.calc_d(s)
        ddy = self.sy.calc_dd(s)
        k = (ddy * dx - ddx * dy) / (dx ** 2 + dy ** 2) ** 1.5
        return k

    def calc_yaw(self, s):
        """
        calc yaw
        """
        dx = self.sx.calc_d(s)
        dy = self.sy.calc_d(s)
        yaw = math.atan2(dy, dx)
        return yaw


def calc_2d_spline_interpolation(x, y, num=100):
    """
    Calc 2d spline course with interpolation

    :param x: interpolated x positions
    :param y: interpolated y positions
    :param num: number of path points
    :return:
        - x     : x positions
        - y     : y positions
        - yaw   : yaw angle list
        - k     : curvature list
        - s     : Path length from start point
    """
    sp = Spline2D(x, y)
    s = np.linspace(0, sp.s[-1], num+1)[:-1]

    r_x, r_y, r_yaw, r_k = [], [], [], []
    for i_s in s:
        ix, iy = sp.calc_position(i_s)
        r_x.append(ix)
        r_y.append(iy)
        r_yaw.append(sp.calc_yaw(i_s))
        r_k.append(sp.calc_curvature(i_s))

    travel = np.cumsum([np.hypot(dx, dy) for dx, dy in zip(np.diff(r_x), np.diff(r_y))]).tolist()
    travel = np.concatenate([[0.0], travel])

    return r_x, r_y, r_yaw, r_k, travel


def test_spline2d():
    print("Spline 2D test")
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


def test_spline():
    print("Spline test")
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


if __name__ == '__main__':
    test_spline()
    test_spline2d()
