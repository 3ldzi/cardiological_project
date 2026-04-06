import numpy as np
import pandas as pd

def compute_statistics(df, column_name):
    # Zamiana *** i innych nienumerycznych wartości na NaN
    values = pd.to_numeric(df[column_name], errors="coerce")

    # Usunięcie NaN
    values = values.dropna()

    # Jeśli po filtracji nie ma danych — zwracamy NaN
    if len(values) == 0:
        return np.nan, np.nan, np.nan

    mean = np.mean(values)
    std = np.std(values)
    med = np.median(values)

    return mean, std, med
