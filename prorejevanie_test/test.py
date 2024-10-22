#!/usr/bin/env python

import random
import matplotlib.pyplot as plt
import numpy as np
from alg import SwingingDoor

class Tester:
    TOLERANCE = 2
    RND_MIN = -1
    RND_MAX = 1
    RANGEBIG = 4
    RANGESMALL = 100
    PICK = 20
    BLUETRUE = True

    def __init__(self, algorithm):
        self.algorithm = algorithm

    # --- Ступеньки
    def generate_data_1(self):
        data = []
        for i in range(self.RANGEBIG):
            for j in range(self.RANGESMALL):
                x = i * self.RANGESMALL + j
                y = -self.PICK if (j // (self.RANGESMALL // 2)) % 2 == 0 else self.PICK
                y += random.uniform(self.RND_MIN, self.RND_MAX)
                data.append((x, y))
        return data

    # --- Пила/
    def generate_data_2(self):
        data = []
        for i in range(self.RANGEBIG):
            for j in range(self.RANGESMALL):
                x = i * self.RANGESMALL + j
                if (j // (self.RANGESMALL // 2)) % 2 == 0:
                    y = -self.PICK + (j % (self.RANGESMALL // 2)) * (2 * self.PICK / (self.RANGESMALL // 2))
                else:
                    y = self.PICK - (j % (self.RANGESMALL // 2)) * (2 * self.PICK / (self.RANGESMALL // 2))
                y += random.uniform(self.RND_MIN, self.RND_MAX)
                data.append((x, y))
        return data

    def generate_data_3(self):
        data = []
        for i in range(self.RANGEBIG):
            for j in range(self.RANGESMALL):
                x = i * self.RANGESMALL + j
                if (j // 50) % 2 == 0:
                    y = (j % 50) * 0.8 - self.PICK  # Подъем
                else:
                    y = self.PICK - (j % 50) * 0.8  # Спад
                y += random.uniform(self.RND_MIN, self.RND_MAX)
                data.append((x, y))
        return data

    # --- Синусоида
    def generate_data_4(self):
        data = []
        total_points = self.RANGEBIG * self.RANGESMALL
        for x in range(total_points):
            # Generate a sine wave with two full periods
            y = self.PICK * np.sin(2 * np.pi * x / (total_points / 2))
            y += random.uniform(self.RND_MIN, self.RND_MAX)
            data.append((x, y))
        return data

    def test_algorithm(self, data, tolerance, test_name):
        instance = self.algorithm(tolerance)
        for x, y in data:
            instance.run(x, y)
        return instance.data


    def run_tests(self):
        # Create a figure with 4 subplots, one for each dataset
        fig, axs = plt.subplots(4, 1, figsize=(18, 20))  # Adjusted height

        # Generate data
        data_1 = self.generate_data_1()
        data_2 = self.generate_data_2()
        data_3 = self.generate_data_3()
        data_4 = self.generate_data_4()

        # Test algorithm and get filtered data
        filtered_data_1 = self.test_algorithm(data_1, self.TOLERANCE, "test_1")
        filtered_data_2 = self.test_algorithm(data_2, self.TOLERANCE, "test_2")
        filtered_data_3 = self.test_algorithm(data_3, self.TOLERANCE, "test_3")
        filtered_data_4 = self.test_algorithm(data_4, self.TOLERANCE, "test_4")

        # Plot each dataset in its own subplot
        for ax, original_data, filtered_data, label in zip(
            axs, 
            [data_1, data_2, data_3, data_4], 
            [filtered_data_1, filtered_data_2, filtered_data_3, filtered_data_4], 
            ["Ступеньки", "Пила 1", "Пила 2", "Синусоида"]
        ):
            # Original data as points
            x_orig, y_orig = zip(*original_data)
            ax.plot(x_orig, y_orig, 'bo', label=f'{label} Original Data', markersize=2)

            # Add a thin line between original data points if BLUETRUE is True
            if self.BLUETRUE:
                ax.plot(x_orig, y_orig, 'b-', linewidth=0.5, alpha=0.5)

            # Filtered data as a polyline with points at the vertices
            x_filt, y_filt = zip(*filtered_data)
            ax.plot(x_filt, y_filt, 'r-', linewidth=1, label=f'{label} Filtered Data')
            ax.plot(x_filt, y_filt, 'ro', markersize=4)  # Points at vertices

            # Calculate the moving average for the original data
            window_size = 5
            moving_avg = np.convolve(y_orig, np.ones(window_size)/window_size, mode='valid')

            # Extend the moving average to match the length of the original data
            moving_avg_full = np.concatenate((
                np.full(window_size//2, moving_avg[0]),
                moving_avg,
                np.full(window_size//2, moving_avg[-1])
            ))

            # Plot the tolerance corridor based on the moving average
            tolerance = self.TOLERANCE
            upper_bound = moving_avg_full + tolerance
            lower_bound = moving_avg_full - tolerance
            ax.fill_between(x_orig, lower_bound, upper_bound, color='gray', alpha=0.3, label='Tolerance Corridor')

            # Calculate the number of points and the ratio
            N_orig = len(original_data)
            N_filtered = len(filtered_data)
            ratio = N_orig / N_filtered if N_filtered != 0 else float('inf')

            # Add title and labels with reduced font size
            ax.set_title(f"{{Датасет: {label}}} -> Эффективность исходных и прореженных данных: "
                        f"{{Norg: {N_orig}; Nflt: {N_filtered}}}; отношение Norg/Nflt: {ratio:.2f}  "
                        f"{{tolerance: {tolerance}}};  {{RND_MIN: {self.RND_MIN}}};  {{RND_MAX: {self.RND_MAX}}}",
                        fontsize=10)
            ax.set_xlabel(' ', fontsize=8)
            ax.set_ylabel('Y', fontsize=8)
            ax.legend(fontsize=8)

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Save the figure to a file
        plt.savefig('comparison_plots.png')

        # Show the plots
        plt.show()



# Create an instance of Tester and run tests
if __name__ == "__main__":
    tester = Tester(SwingingDoor)
    tester.run_tests()
