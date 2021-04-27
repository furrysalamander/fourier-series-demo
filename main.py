# Mike Abbott - 2021
# github.com/furrysalamander
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
import scipy.integrate as integrate
import time


class FourierAnalysis:
    def __init__(self, func: callable, period: float):
        self.func = func
        self.period = period
        self.w = 2*np.pi/self.period
        self.iterations = 1

    def a_n(self, x):
        return (2 / self.period) * integrate.quad(lambda t: self.func(t)*np.cos(x*self.w*t), 0, self.period)[0]

    def b_n(self, x):
        return (2 / self.period) * integrate.quad(lambda t: self.func(t)*np.sin(x*self.w*t), 0, self.period)[0]

    def a_0(self):
        return (1 / self.period) * integrate.quad(self.func, 0, self.period)[0]

    def summation(self, func, start, stop):
        return sum([func(x) for x in range(start, stop + 1)])

    def A(self, x):
        return self.summation(lambda n: self.a_n(n)*np.cos(n*self.w*x), 1, self.iterations)

    def B(self, x):
        return self.summation(lambda n: self.b_n(n)*np.sin(n*self.w*x), 1, self.iterations)

    def compute(self, linspace):
        return self.a_0() + self.A(linspace) + self.B(linspace)

    def frequency_plot(self, x):
        return [np.sqrt(self.a_n(n) ** 2 + self.b_n(n)**2) for n in x]

    def a_plot(self, x):
        return [self.a_n(n) for n in x]

    def b_plot(self, x):
        return [self.b_n(n) for n in x]

def main():
    plt.ion()
    def f(x):
        return np.e**((x % np.pi)/2)

    def update_function(_):
        textbox.edit_modified(False)
        new_func = textbox.get("1.0", "end-1c")
        try:
            x = 1
            float(eval(new_func))
        except:
            pass
        else:
            f_transform.func = lambda x: eval(new_func)
            update_graph()

    def update_iterations(iterations):
        f_transform.iterations = int(iterations)
        update_graph()

    def update_period(_):
        period_box.edit_modified(False)
        try:
            new_period = eval(period_box.get("1.0", "end-1c"))
            print(new_period)
            f_transform.period = new_period
            update_graph()
        except:
            pass

    def update_graph():
        nonlocal t
        t = np.linspace(0, f_transform.period, 200)
        fourier_approximation.set_xdata(t)
        fourier_approximation.set_ydata(f_transform.compute(t))

        original_line.set_xdata(t)
        original_line.set_ydata(f_transform.func(t))

        a_plot.set_xdata(t)
        a_plot.set_ydata(f_transform.a_plot(t))

        b_plot.set_xdata(t)
        b_plot.set_ydata(f_transform.b_plot(t))

        A_plot.set_xdata(t)
        A_plot.set_ydata(f_transform.A(t))

        B_plot.set_xdata(t)
        B_plot.set_ydata(f_transform.B(t))

        figure.canvas.draw()
        figure.canvas.flush_events()
        ax.relim()
        ax.autoscale_view()

    f_transform = FourierAnalysis(f, np.pi)
    t = np.linspace(0, f_transform.period, 200)
    figure, ax = plt.subplots()
    figure.canvas.set_window_title('Fourier Series Demo')
    f_transform.iterations = 1
    fourier_approximation, = ax.plot(t, t*0, label='Fourier Approximation')
    original_line, = ax.plot(t, t*0, label='Original Function')
    a_plot, = ax.plot(t, t*0, label='a_n')
    b_plot, = ax.plot(t, t*0, label='b_n')
    A_plot, = ax.plot(t, t*0, label='A')
    B_plot, = ax.plot(t, t*0, label='B')
    plt.autoscale(True)
    figure.canvas.draw()
    figure.canvas.flush_events()
    ax.legend()
    ax.relim()
    ax.autoscale_view()

    textbox_frame = tk.Frame()
    textbox_label = tk.Label(textbox_frame, text="Equation:")
    textbox = tk.Text(textbox_frame, height=1)
    textbox.delete(1.0, "end")
    textbox.insert(1.0, "np.e**((x % np.pi)/2)")
    textbox_label.pack(side=tk.LEFT)
    textbox.pack(side=tk.LEFT)
    textbox_frame.pack()

    period_frame = tk.Frame()
    period_label = tk.Label(period_frame, text="Period:")
    period_box = tk.Text(period_frame, height=1)
    period_box.delete(1.0, "end")
    period_box.insert(1.0, "np.pi")
    period_label.pack(side=tk.LEFT)
    period_box.pack(side=tk.LEFT)
    period_frame.pack()

    textbox.bind("<<Modified>>", update_function)
    period_box.bind("<<Modified>>", update_period)

    tk.Label(text='For either box, input any valid python code.  The equation should use x as the variable for the x axis.\nNumpy has been imported as np, and you can reference it like you would normally (ie np.pi)\nDrag the slider below in order to adjust the number of iterations in the fourier series.').pack()

    slider = tk.Scale(from_=1, to=20, orient=tk.HORIZONTAL,
                      command=lambda iterations: update_iterations(iterations))
    slider.pack()

    update_graph()

    tk.mainloop()


if __name__ == "__main__":
    main()
