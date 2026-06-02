import numpy as np
import pandas as pd


def create_power_curve(df: pd.DataFrame,
                       power_column: str = "PowerOriginal",
                       time_column: str = "Duration") -> pd.DataFrame:
    """
    Berechnet eine Power Duration Curve.

    Parameters
    ----------
    df : pd.DataFrame
        Aktivitätsdaten.

    power_column : str
        Spalte mit Leistungswerten [W].

    time_column : str
        Spalte mit Zeitwerten [s].

    Returns
    -------
    pd.DataFrame
        duration_s : Dauer [s]
        power_w    : maximale Durchschnittsleistung [W]
    """

    power = df[power_column].to_numpy(dtype=float)
    time = df[time_column].to_numpy(dtype=float)

    sample_time_s = np.median(np.diff(time))
    n = len(power)

    cumulative = np.concatenate(([0.0], np.cumsum(power)))

    durations = []
    max_powers = []

    for window in range(1, n + 1):
        rolling_sum = cumulative[window:] - cumulative[:-window]
        max_avg_power = rolling_sum.max() / window
        durations.append(window * sample_time_s)
        max_powers.append(max_avg_power)

    return pd.DataFrame({
        "duration_s": durations,
        "power_w": max_powers
    })
