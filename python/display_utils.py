"""Collection of utilities for plotting simulations."""

"""Line type definition for different plot elements.
   Colors obtained from ColorBrewery
   http://www.personal.psu.edu/cab38/ColorBrewer/ColorBrewer.html
   7 Qualitative classes
   http://colorbrewer2.org/?type=qualitative&scheme=Paired&n=7
"""
line_def = {
    'True': {
        'label': 'True',
        'marker': 'X',
        'markersize': 14,
        'linestyle': 'None',
        'color': '#a6cee3'
    },
    'Observer': {
        'label': 'Observer',
        'marker': 'o',
        'markersize': 14,
        'linestyle': 'None',
        'color': '#1f78b4'
    },
    'Numerical': {
        'label': 'Numerical',
        'marker': '^',
        'markersize': 12,
        'linestyle': 'None',
        'color': '#e31a1c'
    },
    'MeasuredPosition': {
        'label': 'Mesured Position',
        'marker': 'd',
        'markersize': 10,
        'linestyle': 'None',
        'color': '#33a02c'
    },
    'MeasuedAcceleration': {
        'label': 'Mesured Position',
        'marker': 'd',
        'markersize': 10,
        'linestyle': 'None',
        'color': '#fdbf6f'
    }
}

def __compute_axis_limit(lowerLeftCorner, upperRightCorner):
    delta_x = upperRightCorner.get_x() - lowerLeftCorner.get_x()
    gap_x = delta_x / 5

    delta_y = upperRightCorner.get_y() - lowerLeftCorner.get_y()
    gap_y = delta_y / 5
    out_data = {
        'x_lim_min': lowerLeftCorner.get_x() - gap_x,
        'x_lim_max': upperRightCorner.get_x() + gap_x,
        'y_lim_min': lowerLeftCorner.get_y() - gap_y,
        'y_lim_max': upperRightCorner.get_y() + gap_y
        }
    return out_data


def set_axes_limits(simulation, axes_list):
    minPosition, maxPosition = simulation.get_min_max_position()
    limits = __compute_axis_limit(minPosition, maxPosition)

    # Axis for plotting (x, y) position
    axes_list[0].set_xlim(limits['x_lim_min'], limits['x_lim_max'])
    axes_list[0].set_ylim(limits['y_lim_min'], limits['y_lim_max'])

    minSpeed, maxSpeed = simulation.get_min_max_speed()
    limits = __compute_axis_limit(minSpeed, maxSpeed)

    n_steps = simulation.get_n_time_steps()
    axes_list[1].set_xlim(-1, n_steps + 1)
    axes_list[1].set_ylim(limits['x_lim_min'], limits['x_lim_max'])

    axes_list[2].set_xlim(-1, n_steps + 1)
    axes_list[2].set_ylim(limits['y_lim_min'], limits['y_lim_max'])

def set_axes_labels(ax_x_y_plane, ax_x_speed, ax_y_speed):
    ax_x_y_plane.set_xlabel('x coordinate')
    ax_x_y_plane.set_ylabel('y coordinate')
    ax_x_y_plane.set_title('Position')

    ax_x_speed.set_title('Speed')
    ax_x_speed.set_ylabel('x coordinate')

    ax_y_speed.set_xlabel('Time stamp')
    ax_y_speed.set_ylabel('y coordinate')

def __plot_position_data(x, y, ax, line_style):
    """Plots (x,y) data on axis ax with line style line_style."""
    ax.plot(x, y, **line_style)

def plot_position_data(simulation, ax1, idx=None, plot_measured_position=False):
    true_state = simulation.get_state_as_np_array()
    estimated_state = simulation.get_estimated_state_as_np_array()
    state_shape = true_state.shape
    n_time_stamps = state_shape[0]
    if idx is None:
        idx = n_time_stamps
    x_data = true_state[:, 0]
    y_data = true_state[:, 2]
    line_style = line_def['True']
    __plot_position_data(x_data, y_data, ax1, line_style)

    x_data = estimated_state[:, 0]
    y_data = estimated_state[:, 2]
    line_style = line_def['Observer']
    __plot_position_data(x_data, y_data, ax1, line_style)

    if plot_measured_position:
        measured_position = simulation.convert_list_to_np_array(
            simulation.get_measured_position()
            )
        x_data = measured_position[:, 0]
        y_data = measured_position[:, 1]
        line_style = line_def['MeasuredPosition']
        __plot_position_data(x_data, y_data, ax1, line_style)


def __extract_speed_data(simulation, useXCoordinate=True):
    true_speed = simulation.get_speed()
    estimated_speed = simulation.get_estimated_speed()
    numerical_difference = simulation.get_speed_numerical_difference()
    n_time_stamps = simulation.get_n_time_steps()

    if useXCoordinate:
        speed_data_true = [true_speed[i].get_x() for i in range(n_time_stamps)]
        speed_data_estimation = [estimated_speed[i].get_x() for i in range(n_time_stamps)]
        speed_data_numeric = [numerical_difference[i].get_x() for i in range(n_time_stamps)]
    else:
        speed_data_true = [true_speed[i].get_y() for i in range(n_time_stamps)]
        speed_data_estimation = [estimated_speed[i].get_y() for i in range(n_time_stamps)]
        speed_data_numeric = [numerical_difference[i].get_y() for i in range(n_time_stamps)]

    return (speed_data_true, speed_data_estimation, speed_data_numeric)

def plot_speed_data_x(simulation, ax2):
    speed_data_true, speed_data_estimation, speed_data_numeric = \
        __extract_speed_data(simulation, useXCoordinate=True)
    n_time_stamps = simulation.get_n_time_steps()
    line_style = line_def['True']
    ax2.plot(range(n_time_stamps), speed_data_true, **line_style)
    line_style = line_def['Observer']
    ax2.plot(range(n_time_stamps), speed_data_estimation, **line_style)
    line_style = line_def['Numerical']
    ax2.plot(range(n_time_stamps), speed_data_numeric, **line_style)


def plot_speed_data_y(simulation, ax3):
    speed_data_true, speed_data_estimation, speed_data_numeric = \
        __extract_speed_data(simulation, useXCoordinate=False)
    n_time_stamps = simulation.get_n_time_steps()
    line_style = line_def['True']
    ax3.plot(range(n_time_stamps), speed_data_true, **line_style)
    line_style = line_def['Observer']
    ax3.plot(range(n_time_stamps), speed_data_estimation, **line_style)
    line_style = line_def['Numerical']
    ax3.plot(range(n_time_stamps), speed_data_numeric, **line_style)


def other():
    x_pos_max = max([max(x_val), max(x_estimated_val)])
    x_pos_min = min([min(x_val), min(x_estimated_val)])
    delta_x = x_pos_max - x_pos_min
    y_pos_max = max(y_val)
    y_pos_min = min(y_val)
    delta_y = y_pos_max - y_pos_min

    x_speed_max = max((max(x_speed), max(x_estimated_speed), max(x_numeric_speed)))
    x_speed_min = min((min(x_speed), min(x_estimated_speed), min(x_numeric_speed)))
    delta_x_speed = x_speed_max - x_speed_min
    y_speed_max = max((max(y_speed), max(y_estimated_speed), max(y_numeric_speed)))
    y_speed_min = min((min(y_speed), min(y_estimated_speed), min(y_numeric_speed)))
    delta_y_speed = y_speed_max - y_speed_min


    ax1.set_xlim([x_pos_min - delta_x/5, x_pos_max + delta_x/5])
    ax1.set_ylim([x_pos_min - delta_x/5, x_pos_max + delta_x/5])
    ax2.set_xlim([-1, n_samples + 1])
    ax2.set_ylim([x_speed_min - delta_x_speed/5, x_speed_max + delta_x_speed/5])
    ax3.set_ylim([y_speed_min - delta_y_speed/5, y_speed_max + delta_y_speed/5])
    ax3.set_xlim([-1, n_samples + 1])

    line1, = ax1.plot([], [], linestyle='None', marker='X',  markersize=14, label='True')
    line2, = ax1.plot([], [], linestyle='None', marker='o',  markersize=14, label='Observer')

    line4, = ax2.plot([], [], linestyle='None', marker='X',  markersize=14, label='True')
    line5, = ax2.plot([], [], linestyle='None', marker='o',  markersize=14, label='Observer')
    line6, = ax2.plot([], [], linestyle='None', marker='v',  markersize=12, label='Numerical')
    ax2.legend()
    ax2.set_title('Speed')
    ax2.set_ylabel('x coordinate')

    line7, = ax3.plot([], [], linestyle='None', marker='X',  markersize=14, label='True')
    line8, = ax3.plot([], [], linestyle='None', marker='o',  markersize=14, label='Observer')
    line9, = ax3.plot([], [], linestyle='None', marker='v',  markersize=12, label='Numerical')



#       fig.tight_layout()
def init():
    """initialize animation"""
    line1.set_data([], [])
    line2.set_data([], [])
    line4.set_data([], [])
    line5.set_data([], [])
    line6.set_data([], [])
    line7.set_data([], [])
    line8.set_data([], [])
    line9.set_data([], [])
    return line1, line2, line4, line5, line6, line7, line8, line9

def animate(i):
    """perform animation step"""
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line1.set_data(x_val[:i], y_val[:i])
    line2.set_data(x_estimated_val[:i], y_estimated_val[:i])

    line4.set_data(range(i), x_speed[:i])
    line5.set_data(range(i), x_estimated_speed[:i])
    line6.set_data(range(i), x_numeric_speed[:i])

    line7.set_data(range(i), y_speed[:i])
    line8.set_data(range(i), y_estimated_speed[:i])
    line9.set_data(range(i), y_numeric_speed[:i])

    return line1, line2, line4, line5, line6, line7, line8, line9


    anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_samples, interval=200, blit=True)

                               # call our new function to display the animation
    #display_animation(anim)
    anim.save('observer_ex_1.avi', fps=5, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])
    HTML(anim.to_html5_video())

def generate_base_figure(simulation, ax1, ax2, ax3,
                         plot_measured_position=False):
    """Generates figures for the simulation.

    Simulation is an object of type GenerateBaseSimulation
    ax1 shows (x,y) coordinate of true and estimated car position
    will be drawn
    ax2 shows the estimated x speed over time instants
    ax3 shows the estimated y speed over time instants
    """

    set_axes_limits(simulation, (ax1, ax2, ax3))
    set_axes_labels(ax1, ax2, ax3)
    plot_position_data(simulation, ax1, plot_measured_position=plot_measured_position)
    plot_speed_data_x(simulation, ax2)
    plot_speed_data_y(simulation, ax3)
