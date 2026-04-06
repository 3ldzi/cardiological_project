import pandas as pd

def filter_by_quality(df, threshold):
    # zamiana wartości na liczbowe, *** → NaN
    q = pd.to_numeric(df["QI-ICG"], errors="coerce")

    # dodajemy kolumnę z konwersją
    df = df.copy()
    df["QI-ICG"] = q

    # filtrujemy tylko te wiersze, gdzie QI-ICG >= threshold
    df = df[df["QI-ICG"] >= threshold]

    return df
