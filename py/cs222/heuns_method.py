# QUIZ
#
# Implement Heun's Method in the function below,
# building off of the Forward Euler method as a
# base. The resulting diagram will show the
# errors in comparison.

import math
import numpy
import matplotlib.pyplot

total_time = 24. * 3600.  # s
g = 9.81  # m / s2
earth_mass = 5.97e24  # kg
gravitational_constant = 6.67e-11  # N m2 / kg2
radius = (gravitational_constant * earth_mass * total_time ** 2.
          / 4. / math.pi ** 2.) ** (1. / 3.)
speed = 2.0 * math.pi * radius / total_time

# These are used to keep track of the data we want to plot
h_array = []
euler_error_array = []
heuns_error_array = []


def acceleration(spaceship_position):
    vector_to_earth = - spaceship_position  # earth located at origin
    return gravitational_constant * earth_mass / numpy.linalg.norm(
        vector_to_earth) ** 3 * vector_to_earth


def heuns_method(num_steps):
    h = total_time / num_steps
    h_array.append(h)

    x = numpy.zeros([num_steps + 1, 2])  # m
    v = numpy.zeros([num_steps + 1, 2])  # m / s

    x[0, 0] = radius
    v[0, 1] = speed

    ###Original Euler Method
    for step in range(num_steps):
        x[step + 1] = x[step] + h * v[step]
        # v[step + 1] = v[step] + h * acceleration(x[step])
        # Symplectic Euler
        v[step + 1] = v[step] + h * acceleration(x[step + 1])

    error = numpy.linalg.norm(x[-1] - x[0])
    euler_error_array.append(error)
    ###End Original Euler Method

    ###Heun's Method
    for step in range(num_steps):
        init_acceleration = acceleration(x[step])
        # xE = x[step] + h * (v[step])
        vE = v[step] + h * init_acceleration
        x[step + 1] = x[step] + h * 0.5 * (v[step] + vE)
        # v[step + 1] = v[step] + h * 0.5 * (init_acceleration + acceleration(xE))
        ## Heun's Method variant
        v[step + 1] = v[step] + h * 0.5 * (
            init_acceleration + acceleration(x[step + 1]))

    error = numpy.linalg.norm(x[-1] - x[0])
    heuns_error_array.append(error)
    ###End Heun's Method

    return x, v, error


for num_steps in [50, 100, 200, 500, 1000]:
    x, v, error = heuns_method(num_steps)  # Check x, v, error


def plot_me():
    matplotlib.pyplot.scatter(h_array, euler_error_array, c='g')
    matplotlib.pyplot.text(h_array[0], euler_error_array[0], r'Euler Error')
    matplotlib.pyplot.scatter(h_array, heuns_error_array, c='b')
    matplotlib.pyplot.text(h_array[0], heuns_error_array[0], r'Heuns Error')
    matplotlib.pyplot.xlim(xmin=0.)
    matplotlib.pyplot.ylim(ymin=0.)
    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('Step size in s')
    axes.set_ylabel('Error in m')
    matplotlib.pyplot.show()


plot_me()