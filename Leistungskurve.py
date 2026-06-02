import numpy as np
import pandas as pd
from typing import Optional, Sequence, Union


def create_power_curve(
    data: Union[pd.DataFrame, pd.Series, np.ndarray, Sequence[float]],
    power_column: str = "PowerOriginal",
    time_column: str = "Duration",
    time: Optional[Union[pd.Series, np.ndarray, Sequence[float]]] = None,
) -> pd.DataFrame:
    """
    Berechnet eine Power Duration Curve.

    Parameters
    ----------
    data : DataFrame, Series, ndarray oder Sequenz
        Aktivitaetsdaten als DataFrame oder reine Leistungswerte [W].

    power_column : str
        Spalte mit Leistungswerten [W], wenn data ein DataFrame ist.

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