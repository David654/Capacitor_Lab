import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class Graph:
    def __init__(self, directory, save_directory):
        self.directory = directory
        self.save_directory = save_directory
        self.transform_data = lambda x, y: y

    def set_data_transform_func(self, func):
        self.transform_data = func

    def get_file_data(self, file_name, separator=','):
        """
        Reads and processes numerical data from a CSV file.

        This function loads data from a specified CSV file, removes blank lines,
        flattens the data into a one-dimensional array, replaces NaN values with 0,
        and returns the processed data along with the number of measurement pairs.

        :param str file_name:
            Name of the CSV file to be read.
        :param str separator:
            Delimiter used in the CSV file (default: ',').

        :return:
            A tuple containing:
            - A flattened NumPy array of the data.
            - The number of measurement pairs in the dataset.
        :rtype: tuple[np.ndarray, int]

        :raises FileNotFoundError:
            If the specified file does not exist in the directory.
        :raises pd.errors.EmptyDataError:
            If the file is empty or contains no valid data.
        """
        file_data = pd.read_csv(self.directory + file_name)

        data = pd.read_csv(self.directory + file_name, usecols=file_data.columns.values, skip_blank_lines=True,
                           sep=separator)
        data.dropna(how="all")
        data = data.values.flatten()

        data[np.isnan(data)] = 0

        return data, len(file_data.columns) // 2

    def plot(self, file_name, save_file_name, title="Graph", x_axis_name='x', y_axis_name='y', graph_size=5,
                   show_fit=True, polynom_degree=1):

        """
        Plots scatter graphs with optional linear fits from a data file.

        The function reads measurement data from a file, creates subplots for each dataset,
        and optionally fits a linear trend line to the data for each subplot.

        :param str file_name:
            Name of the file containing the measurement data.
        :param str title:
            Title of the graph (default: "Graph").
        :param str x_axis_name:
            Label for the x-axis (default: "x").
        :param str y_axis_name:
            Label for the y-axis (default: "y").
        :param float graph_size:
            Size of each subplot in inches (default: 5).
        :param bool show_fit:
            Whether to display a fit line for each dataset (default: True).
        :param int polynom_degree:
            Maximum degree of a fitting polynomial.

        :return:
            Displays a Matplotlib figure with multiple subplots.
        :rtype: None

        **Data Format Assumption**:
            - The file should contain numerical values.
            - Data is structured such that:
                - Odd-indexed columns represent x-values.
                - Even-indexed columns represent y-values.
        """

        data = self.get_file_data(file_name)

        figure, axis = plt.subplots(1, data[1], figsize=(graph_size * data[1], graph_size), constrained_layout=True)

        for i in range(data[1]):
            x = data[0][i * 2::2 * data[1]]
            y = data[0][i * 2 + 1::2 * data[1]]

            y = self.transform_data(x, y)

            axis[i].scatter(x, y, color='black', linewidth=0.1)
            axis[i].set_xlabel(x_axis_name)
            axis[i].set_ylabel(y_axis_name)
            axis[i].set_title('Measurement ' + str(i + 1))
            axis[i].set_axisbelow(True)
            axis[i].grid()

            if show_fit:
                x_fit = np.linspace(0, max(x), 100)
                y_fit = np.zeros(100)
                fit_coeff = np.zeros(polynom_degree + 1)

                if polynom_degree == 1:
                    linear_coeff = np.linalg.lstsq(x.reshape(-1, 1), y)[0][0]
                    fit_coeff[0] = linear_coeff

                else:
                    fit_coeff = np.polyfit(x, y, 2)

                for j in range(0, polynom_degree + 1):
                    print(fit_coeff[-j - 1])
                    y_fit += fit_coeff[-j - 1] * x_fit ** j

                axis[i].plot(x_fit, y_fit, color='red', linewidth=2)
                print(f'Slope {i + 1}: {fit_coeff}')

        plt.suptitle(title, fontweight='bold')
        # plt.savefig(self.save_directory + save_file_name + '.eps', dpi=600)
        plt.show()


graph = Graph('E:/Works/Lab Reports/reports/capacitor/data/', 'E:/Works/Lab Reports/reports/capacitor/graphs/')

d = 0.01
e0 = 8.85418782e-12

graph.set_data_transform_func(lambda x, y: y * 0.01 * x ** 2 * np.pi * e0 / d * 10e9)
graph.plot('VR1_exp2.csv', 'exp_2', 'Charge density', x_axis_name='Distance from the center of the plate (cm)',
                 y_axis_name='Charge (nC)', polynom_degree=2)
