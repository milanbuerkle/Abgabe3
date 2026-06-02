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
        Spalte mit Zeitwerten [s] oder mit Sample-Dauern [s].

    Returns
    -------
    pd.DataFrame
        duration_s : Dauer [s]
        power_w    : maximale Durchschnittsleistung [W]
    """

    subset = df[[power_column, time_column]].dropna(subset=[power_column, time_column])
    power = subset[power_column].to_numpy(dtype=float)
    time = subset[time_column].to_numpy(dtype=float)

    if len(power) == 0:
        raise ValueError("Keine gültigen Daten für die Power Curve gefunden.")

    if np.all(np.diff(time) >= 0) and np.any(np.diff(time) > 0):
        sample_durations = np.diff(np.concatenate(([0.0], time)))
    else:
        sample_durations = time

    sample_durations = np.maximum(sample_durations, 0.0)
    energy = power * sample_durations
    cumulative_time = np.concatenate(([0.0], np.cumsum(sample_durations)))
    cumulative_energy = np.concatenate(([0.0], np.cumsum(energy)))

    n = len(power)
    durations = []
    max_powers = []

    for window in range(1, n + 1):
        window_times = cumulative_time[window:] - cumulative_time[:-window]
        window_energy = cumulative_energy[window:] - cumulative_energy[:-window]

        valid = window_times > 0.0
        if not np.any(valid):
            durations.append(0.0)
            max_powers.append(np.nan)
            continue

        average_powers = np.full_like(window_times, np.nan, dtype=float)
        average_powers[valid] = window_energy[valid] / window_times[valid]

        best_idx = np.nanargmax(average_powers)
        durations.append(window_times[best_idx])
        max_powers.append(average_powers[best_idx])

    return pd.DataFrame({
        "duration_s": durations,
        "power_w": max_powers
    })