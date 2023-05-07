import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon


class Polynomial:
    def __init__(self, coefficients) -> None:
        self.coefs = coefficients
        self.poly = np.poly1d(coefficients)

    def FuncSolve(self, x):
        return self.poly(x)

    def LeftRsum(self, start, end, interval_len):
        sum = 0
        for i in np.arange(start, end, interval_len):
            sum += self.poly(i) * interval_len
        return sum

    def RightRsum(self, start, end, interval_len):
        sum = 0
        for i in np.arange(start + interval_len, end + interval_len, interval_len):
            sum += self.poly(i) * interval_len
        return sum

    def MidRsum(self, start, end, interval_len):
        sum = 0
        for i in np.arange(start, end, interval_len):
            sum += self.poly(i + (interval_len / 2)) * interval_len
        return sum

    def TrapRsum(self, start, end, interval_len):
        sum = 0
        coef = 0.5 * interval_len
        for i in np.arange(start, end, interval_len):
            sum += coef * (self.poly(i) + self.poly(i + interval_len))
        return sum

    def RiemannSums(self, interval_len):
        x = np.linspace(lower_lim, upper_lim)
        fig, ax1s = plt.subplots(2, 2)

        # Left Riemann Sum Plotting
        ax1s[0, 0].plot(x, func.FuncSolve(x))
        ax1s[0, 0].set_title(
            f"Left RS: {self.LeftRsum(lower_lim,upper_lim,interval_len)}"
        )
        for i in np.arange(lower_lim, upper_lim, interval_len):
            ax1s[0, 0].add_patch(
                Rectangle((i, 0), interval_len, func.FuncSolve(i), ec="blue", fc="none")
            )

        # Right Riemann Sum Plotting
        ax1s[0, 1].plot(x, func.FuncSolve(x), "tab:orange")
        ax1s[0, 1].set_title(
            f"Right RS: {self.RightRsum(lower_lim,upper_lim,interval_len)}"
        )
        for i in np.arange(lower_lim, upper_lim, interval_len):
            ax1s[0, 1].add_patch(
                Rectangle(
                    (i, 0),
                    interval_len,
                    func.FuncSolve(i + interval_len),
                    ec="orange",
                    fc="none",
                )
            )

        # Midpoint Riemann Sum Plotting
        ax1s[1, 0].plot(x, func.FuncSolve(x), "tab:green")
        ax1s[1, 0].set_title(f"Mid RS: {self.MidRsum(lower_lim,upper_lim,interval_len)}")
        for i in np.arange(lower_lim, upper_lim, interval_len):
            ax1s[1, 0].add_patch(
                Rectangle(
                    (i, 0),
                    interval_len,
                    func.FuncSolve(i + (interval_len / 2)),
                    ec="green",
                    fc="none",
                )
            )

        # Trapezoidal Riemann Sum Plotting
        ax1s[1, 1].plot(x, func.FuncSolve(x), "tab:red")
        ax1s[1, 1].set_title(
            f"Trap RS: {self.TrapRsum(lower_lim,upper_lim,interval_len)}"
        )
        for i in np.arange(lower_lim, upper_lim, interval_len):
            x = [i, i + interval_len, i + interval_len, i]
            y = [0, 0, func.FuncSolve(i + interval_len), func.FuncSolve(i)]
            ax1s[1, 1].add_patch(Polygon(xy=list(zip(x, y)), ec="red", fc="none"))

        for ax1 in ax1s.flat:
            ax1.set(xlabel="x-label", ylabel="y-label")
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax1 in ax1s.flat:
            ax1.label_outer()
        plt.show()


    def IntegrationAnimation(self, rule, start_il, end_il):
        interval_decimal_count = 0
        decimal_point_reached = False
        for digit in str(end_il):
            if digit == '.':
                decimal_point_reached = True
            if decimal_point_reached == True:
                interval_decimal_count += 1
        
        fig, ax1 = plt.subplots()
        x = np.linspace(lower_lim, upper_lim)
        ax1.set_title(
            f"{rule.capitalize()} Riemann Sum From Interval Width of {start_il} to {end_il}"
        )
        
        '''ax2.set_title(
            "Percent Error / Approximate Accuracy of Approximation"
        )'''

        patches = []
        if rule.lower() == "right":
            sum_type = self.RightRsum
            color = "orange"
            for i in np.arange(lower_lim, upper_lim, start_il):
                patches.append(
                    ax1.add_patch(
                        Rectangle(
                            (i, 0),
                            start_il,
                            func.FuncSolve(i + start_il),
                            ec="orange",
                            fc="none",
                        )
                    )
                )
        elif rule.lower() == "left":
            sum_type = self.LeftRsum
            color = "blue"
            for i in np.arange(lower_lim, upper_lim, start_il):
                patches.append(
                    ax1.add_patch(
                        Rectangle(
                            (i, 0), start_il, func.FuncSolve(i), ec="blue", fc="none"
                        )
                    )
                )
        elif rule.lower() == "mid":
            sum_type = self.MidRsum
            color = "green"
            for i in np.arange(lower_lim, upper_lim, start_il):
                patches.append(
                    ax1.add_patch(
                        Rectangle(
                            (i, 0),
                            start_il,
                            func.FuncSolve(i + (start_il / 2)),
                            ec="green",
                            fc="none",
                        )
                    )
                )
        elif rule.lower() == "trap":
            sum_type = self.TrapRsum
            color = "red"
            for i in np.arange(lower_lim, upper_lim, start_il):
                xtrap = [i, i + start_il, i + start_il, i]
                ytrap = [0, 0, func.FuncSolve(i + start_il), func.FuncSolve(i)]
                patches.append(
                    ax1.add_patch(
                        Polygon(xy=list(zip(xtrap, ytrap)), ec="red", fc="none")
                    )
                )

        ax1.plot(x, func.FuncSolve(x), f"k")

        sum_text = ax1.text(
            0.015,
            0.98,
            f"Approx. Area: {sum_type(lower_lim,upper_lim,start_il)}",
            ha="left",
            va="top",
            transform=ax1.transAxes,
            bbox={"facecolor": color, "alpha": 0.5, "pad": 5},
        )

        int_text = ax1.text(
            0.015,
            0.90,
            f"Subinterval Length: {round(start_il,5)}",
            ha="left",
            va="top",
            transform=ax1.transAxes,
            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 5},
        )

        def animate(i):
            interval = round(start_il - (end_il * i),interval_decimal_count)
            sum_text.set_text(f"Approx. Area: {sum_type(lower_lim,upper_lim,interval)}")
            int_text.set_text(f"Subinterval Length: {round(interval,5)}")
            # Clear subintervals from previous frame
            for patch in patches:
                patch.set(ec="none")

            if rule.lower() == "right":
                for i in np.arange(lower_lim, upper_lim, interval):
                    patches.append(
                        ax1.add_patch(
                            Rectangle(
                                (i, 0),
                                interval,
                                func.FuncSolve(i + interval),
                                ec="orange",
                                fc="none",
                            )
                        )
                    )
            elif rule.lower() == "left":
                for i in np.arange(lower_lim, upper_lim, interval):
                    patches.append(
                        ax1.add_patch(
                            Rectangle(
                                (i, 0),
                                interval,
                                func.FuncSolve(i),
                                ec="blue",
                                fc="none",
                            )
                        )
                    )
            elif rule.lower() == "mid":
                for i in np.arange(lower_lim, upper_lim, interval):
                    patches.append(
                        ax1.add_patch(
                            Rectangle(
                                (i, 0),
                                interval,
                                func.FuncSolve(i + (interval / 2)),
                                ec="green",
                                fc="none",
                            )
                        )
                    )
            elif rule.lower() == "trap":
                for i in np.arange(lower_lim, upper_lim, interval):
                    xtrap = [i, i + interval, i + interval, i]
                    ytrap = [0, 0, func.FuncSolve(i + interval), func.FuncSolve(i)]
                    patches.append(
                        ax1.add_patch(
                            Polygon(xy=list(zip(xtrap, ytrap)), ec="red", fc="none")
                        )
                    )

        n = int(start_il / end_il)
        ani = animation.FuncAnimation(
            fig, animate, interval=5000 / n, repeat=False, frames=n
        )

        plt.show()


# Set the coefficients
func = Polynomial([3,3,-2,1])
print(func.poly)

# Set boundaries (a and b)
lower_lim = -1
upper_lim = 1

# Graphs
func.RiemannSums(1)
func.IntegrationAnimation("right", 1, 0.01)