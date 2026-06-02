import matplotlib.pyplot as plt
import pandas as pd


def plot_power_curve(power_curve_df: pd.DataFrame):

    plt.figure(figsize=(10, 6))

    plt.plot(
        power_curve_df["duration_s"],
        power_curve_df["power_w"]
    )

    plt.xscale("log")

    plt.xlabel("Zeit [s]")
    plt.ylabel("Leistung [W]")
    plt.title("Power Duration Curve")

    plt.grid(True)
    plt.tight_layout()

    return plt.gcf()