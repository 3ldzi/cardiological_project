import os
import pandas as pd

def load_par_files(input_folder="input"):
    files = [f for f in os.listdir(input_folder) if f.endswith(".par")]
    data = {}

    for file in files:
        path = os.path.join(input_folder, file)

        try:
            df = pd.read_csv(
                path,
                sep=r"\s+",
                engine="python",
                header=0,       # <-- pierwsza linia to nagłówek
                skiprows=[1],   # <-- druga linia to jednostki, pomijamy
                on_bad_lines="skip"
            )
        except Exception as e:
            print(f"Błąd w pliku {file}: {e}")
            continue

        data[file] = df

    return data
